import tkinter as tk
import time
import threading
from tkinter import ttk, messagebox, filedialog
import json
import csv
import paho.mqtt.client as mqtt
from Paciente import Paciente

class DetalhesDialog:
    def __init__(self, root, paciente):
        self.top = tk.Toplevel(root)
        self.top.title("Detalhes do Paciente")

        self.data_hora_registro_label = tk.Label(self.top, text="Data/Hora do Registro:")
        self.data_hora_registro_label.grid(row=0, column=0, padx=5, pady=5)

        self.data_hora_registro_valor_label = tk.Label(self.top, text=paciente.data_hora_registro)
        self.data_hora_registro_valor_label.grid(row=0, column=1, padx=5, pady=5)

        self.paciente = paciente
        self.dados_mqtt = {"temperatura": [], "oxigenacao": [], "batimentos": []}
        self.mqtt_client = mqtt.Client()

        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("46.17.108.113", 1883, 60)
        self.mqtt_client.subscribe("/TEF/Hosp108/attrs/t")
        self.mqtt_client.subscribe("/TEF/Hosp108/attrs/o")
        self.mqtt_client.subscribe("/TEF/Hosp108/attrs/h")

        detalhes = self.obter_detalhes_paciente()
        self.detalhes_label = tk.Label(self.top, text=detalhes, justify=tk.LEFT)
        self.detalhes_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.obter_dados_button = tk.Button(self.top, text="Obter Dados MQTT", command=self.obter_dados_mqtt)
        self.obter_dados_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Adicione uma variável de controle para o status
        self.status_label = tk.Label(self.top, text="", justify=tk.LEFT)
        self.status_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Adicione um botão para exportar para CSV
        self.botao_exportar_csv = tk.Button(self.top, text="Exportar para CSV", command=self.exportar_csv)
        self.botao_exportar_csv.grid(row=4, column=0, columnspan=2, pady=10)

    def obter_dados_mqtt(self):
        # Limpa os dados anteriores
        self.dados_mqtt = {"temperatura": [], "oxigenacao": [], "batimentos": []}

        # Inicia a leitura dos dados MQTT em uma nova thread
        threading.Thread(target=self.realizar_leitura_mqtt).start()

    def realizar_leitura_mqtt(self):
        # Inicia a leitura dos dados MQTT por 10 segundos
        self.atualizar_status("Obtendo dados...")
        self.mqtt_client.loop_start()
        time.sleep(10)
        self.mqtt_client.loop_stop()
        self.atualizar_status("Dados obtidos com sucesso.")

        # Calcula as médias e atualiza a interface
        self.atualizar_detalhes_paciente()

    def obter_detalhes_paciente(self):
        temperatura_media = self.calcular_media('temperatura')
        oxigenacao_media = self.calcular_media('oxigenacao')
        batimentos_media = self.calcular_media('batimentos')

        detalhes = (
            f"Nome: {self.paciente.nome} {self.paciente.sobrenome}\n"
            f"Idade: {self.paciente.idade}\n"
            f"Sexo: {self.paciente.sexo}\n"
            f"Hipertensa: {'Sim' if self.paciente.hipertensa else 'Não'}\n"
            f"Doença Contagiosa: {'Sim' if self.paciente.doenca_contagiosa else 'Não'}\n"
            f"Alergias: {'Sim' if self.paciente.alergias else 'Não'}\n"
            f"Sintomas: {self.paciente.sintomas}\n"
            f"Temperatura: {temperatura_media}°C\n"
            f"Oxigenação: {oxigenacao_media}%\n"
            f"Batimentos Cardíacos: {batimentos_media} bpm\n"
        )
        return detalhes

    def calcular_media(self, tipo_dado):
        registros = self.dados_mqtt[tipo_dado]
        if registros:
            return sum(registros) / len(registros)
        return "N/A"

    def on_message(self, client, userdata, msg):
        try:
            valor = float(msg.payload.decode())
        except ValueError:
            return  # Ignorar se não for possível converter para float

        if msg.topic == "/TEF/Hosp108/attrs/o":
            self.dados_mqtt['oxigenacao'].append(valor)
        elif msg.topic == "/TEF/Hosp108/attrs/h":
            self.dados_mqtt['batimentos'].append(valor)
        elif msg.topic == "/TEF/Hosp108/attrs/t":
            self.dados_mqtt['temperatura'].append(valor)

        detalhes_atualizados = self.obter_detalhes_paciente()
        self.atualizar_detalhes_paciente_gui(detalhes_atualizados)

    def atualizar_detalhes_paciente(self):
        detalhes_atualizados = self.obter_detalhes_paciente()
        self.atualizar_detalhes_paciente_gui(detalhes_atualizados)

    def atualizar_detalhes_paciente_gui(self, detalhes_atualizados):
        # Agende a atualização da interface gráfica na thread principal
        self.top.after(0, self.detalhes_label.config, {"text": detalhes_atualizados})

    def atualizar_status(self, mensagem):
        # Atualiza o texto na interface
        self.status_label.config(text=mensagem)
        self.top.update_idletasks()

    def exportar_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Nome", "Sobrenome", "Idade", "Sexo", "Hipertensa", "Doença Contagiosa",
                                 "Alergias", "Sintomas", "Data/Hora do Registro"])
                writer.writerow([self.paciente.nome, self.paciente.sobrenome, self.paciente.idade,
                                 self.paciente.sexo, self.paciente.hipertensa, self.paciente.doenca_contagiosa,
                                 self.paciente.alergias, self.paciente.sintomas, self.paciente.data_hora_registro])
