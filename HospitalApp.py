import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import json
import csv
import paho.mqtt.client as mqtt
from Paciente import Paciente
from CadastrarDialog import CadastrarDialog
from AtualizarDialog import AtualizarDialog
from DetalhesDialog import DetalhesDialog
import logging
from Login import Login

MQTT_BROKER = "46.17.108.113"
MQTT_PORT = 1883
MQTT_TOPICS = ["/TEF/Hosp108/attrs/o", "/TEF/Hosp108/attrs/h", "/TEF/Hosp108/attrs/t"]

class HospitalApp:
    def __init__(self, root, usuario_autenticado=False):
        self.root = root
        self.root.title("Cadastro de Pacientes em Hospitais")
        self.root.geometry("600x400")

        self.pacientes = []
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Pacientes Cadastrados")
        self.label.pack()

        self.listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, width=50)
        self.listbox.pack()

        self.cadastrar_button = tk.Button(self.frame, text="Cadastrar Paciente", command=self.cadastrar_paciente)
        self.cadastrar_button.pack(pady=5)

        self.atualizar_button = tk.Button(self.frame, text="Atualizar Paciente", command=self.atualizar_paciente)
        self.atualizar_button.pack(pady=5)

        self.detalhes_button = tk.Button(self.frame, text="Ver Detalhes", command=self.exibir_dados_paciente)
        self.detalhes_button.pack(pady=5)

        self.excluir_button = tk.Button(self.frame, text="Excluir Paciente", command=self.excluir_paciente)
        self.excluir_button.pack(pady=5)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()

        self.detalhes_dialog = None
        self.carregar_pacientes()
        self.atualizar_lista()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            for topic in MQTT_TOPICS:
                client.subscribe(topic)
        else:
            logging.error("Falha na conexão com o MQTT broker, código de resultado: %s", rc)

    def on_message(self, client, userdata, msg):
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        if self.detalhes_dialog:
            self.detalhes_dialog.atualizar_dados_detalhes_paciente(msg.topic, msg.payload.decode())

    def carregar_pacientes(self):
        try:
            with open('pacientes.json', 'r') as arquivo:
                pacientes_json = json.load(arquivo)
                self.pacientes = [Paciente(**paciente) for paciente in pacientes_json]
        except FileNotFoundError:
            self.pacientes = []
        except Exception as e:
            logging.exception("Erro ao carregar dados do arquivo JSON: %s", e)
            messagebox.showerror("Erro", "Erro ao carregar dados do arquivo JSON. Consulte o log para mais informações.")

    def salvar_pacientes(self):
        try:
            with open('pacientes.json', 'w') as arquivo:
                pacientes_json = [paciente.__dict__ for paciente in self.pacientes]
                json.dump(pacientes_json, arquivo, indent=2)
        except Exception as e:
            logging.exception("Erro ao salvar dados em JSON: %s", e)
            messagebox.showerror("Erro", "Erro ao salvar dados em JSON. Consulte o log para mais informações.")

    def atualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for i, paciente in enumerate(self.pacientes, 1):
            self.listbox.insert(tk.END, f"{i}. {paciente.nome} {paciente.sobrenome}")

    def cadastrar_paciente(self):
        cadastrar_dialog = CadastrarDialog(self.root, self.atualizar_lista, self)
        self.root.wait_window(cadastrar_dialog.top)
        if cadastrar_dialog.paciente_cadastrado:
            cadastrar_dialog.paciente_cadastrado.data_hora_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.pacientes.append(cadastrar_dialog.paciente_cadastrado)
            self.atualizar_lista()
            self.salvar_pacientes()

    def atualizar_paciente(self):
        if not self.listbox.curselection():
            messagebox.showwarning("Aviso", "Selecione um paciente para atualizar.")
            return

        indice_selecionado = self.listbox.curselection()[0]
        paciente_selecionado = self.pacientes[indice_selecionado]

        atualizar_dialog = AtualizarDialog(self.root, paciente_selecionado, self.atualizar_lista)
        self.root.wait_window(atualizar_dialog.top)
        if atualizar_dialog.paciente_atualizado:
            self.pacientes[indice_selecionado] = atualizar_dialog.paciente_atualizado
            self.atualizar_lista()
            self.salvar_pacientes()

    def exibir_dados_paciente(self):
        if not self.listbox.curselection():
            messagebox.showwarning("Aviso", "Selecione um paciente para exibir os dados.")
            return

        indice_selecionado = self.listbox.curselection()[0]
        paciente_selecionado = self.pacientes[indice_selecionado]

        self.detalhes_dialog = DetalhesDialog(self.root, paciente_selecionado)
        self.root.wait_window(self.detalhes_dialog.top)

    def excluir_paciente(self):
        if not self.listbox.curselection():
            messagebox.showwarning("Aviso", "Selecione um paciente para excluir.")
            return

        indice_selecionado = self.listbox.curselection()[0]
        paciente_selecionado = self.pacientes[indice_selecionado]

        confirmacao = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja excluir o paciente {paciente_selecionado.nome} {paciente_selecionado.sobrenome}?"
        )
        
        if confirmacao:
            del self.pacientes[indice_selecionado]
            self.atualizar_lista()
            self.salvar_pacientes()

    def criar_botao_exportar_csv(self):
        exportar_csv_button = tk.Button(self.frame, text="Exportar CSV", command=self.exportar_csv)
        exportar_csv_button.pack(pady=5)

    def exportar_csv(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Nome", "Sobrenome", "Idade", "Sexo", "Hipertensa", "Doença Contagiosa",
                                     "Alergias", "Sintomas", "Data/Hora do Registro"])
                    for paciente in self.pacientes:
                        writer.writerow([paciente.nome, paciente.sobrenome, paciente.idade, paciente.sexo,
                                         paciente.hipertensa, paciente.doenca_contagiosa, paciente.alergias,
                                         paciente.sintomas, paciente.data_hora_registro])
        except Exception as e:
            logging.exception("Erro ao exportar para CSV: %s", e)
            messagebox.showerror("Erro", "Ocorreu um erro ao exportar para CSV. Consulte o log para mais informações.")

def on_login_success(root):
    # Fechar a tela de login
    root.destroy()

    # Criar a instância do HospitalApp
    root = tk.Tk()
    hospital_app = HospitalApp(root, usuario_autenticado=True)  
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()

    # Mostrar a tela de login
    login_screen = Login(root, lambda: on_login_success(root))  # Usando lambda para passar o argumento 'root'

    root.mainloop()
