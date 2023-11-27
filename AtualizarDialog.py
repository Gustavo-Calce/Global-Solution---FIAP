import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Paciente import Paciente
from CadastrarDialog import CadastrarDialog

class AtualizarDialog:
    def __init__(self, root, paciente, callback):
        self.top = tk.Toplevel(root)
        self.top.title("Atualizar Paciente")

        self.paciente = paciente
        self.callback = callback

        self.data_hora_registro_label = tk.Label(
            self.top, text=f"Data/Hora do Registro: {paciente.data_hora_registro}"
        )
        self.data_hora_registro_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.atualizar_data_hora_button = tk.Button(
            self.top, text="Atualizar Data/Hora do Registro", command=self.atualizar_data_hora_registro
        )
        self.atualizar_data_hora_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.idade_label = tk.Label(self.top, text="Nova Idade:")
        self.idade_label.grid(row=2, column=0, padx=5, pady=5)
        self.idade_entry = tk.Entry(self.top)
        self.idade_entry.grid(row=2, column=1, padx=5, pady=5)

        # Remova o campo de entrada para o sexo
        # self.sexo_label = tk.Label(self.top, text="Novo Sexo:")
        # self.sexo_label.grid(row=3, column=0, padx=5, pady=5)
        # self.sexo_entry = tk.Entry(self.top)
        # self.sexo_entry.grid(row=3, column=1, padx=5, pady=5)

        self.hipertensa_label = tk.Label(self.top, text="Hipertensa (Sim/Não):")
        self.hipertensa_label.grid(row=3, column=0, padx=5, pady=5)
        self.hipertensa_entry = tk.Entry(self.top)
        self.hipertensa_entry.grid(row=3, column=1, padx=5, pady=5)

        self.doenca_contagiosa_label = tk.Label(self.top, text="Doença Contagiosa (Sim/Não):")
        self.doenca_contagiosa_label.grid(row=4, column=0, padx=5, pady=5)
        self.doenca_contagiosa_entry = tk.Entry(self.top)
        self.doenca_contagiosa_entry.grid(row=4, column=1, padx=5, pady=5)

        self.alergias_label = tk.Label(self.top, text="Alergias:")
        self.alergias_label.grid(row=5, column=0, padx=5, pady=5)
        self.alergias_entry = tk.Entry(self.top)
        self.alergias_entry.grid(row=5, column=1, padx=5, pady=5)

        self.sintomas_label = tk.Label(self.top, text="Sintomas:")
        self.sintomas_label.grid(row=6, column=0, padx=5, pady=5)
        self.sintomas_entry = tk.Entry(self.top)
        self.sintomas_entry.grid(row=6, column=1, padx=5, pady=5)

        self.atualizar_button = tk.Button(self.top, text="Atualizar", command=self.atualizar)
        self.atualizar_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.paciente_atualizado = None

    def atualizar(self):
        nova_idade = int(self.idade_entry.get()) if self.idade_entry.get() else self.paciente.idade
        # Remova a obtenção do novo sexo
        # novo_sexo = self.sexo_entry.get() if self.sexo_entry.get() else self.paciente.sexo
        nova_hipertensa = self.hipertensa_entry.get().lower() == 'sim' if self.hipertensa_entry.get() else self.paciente.hipertensa
        nova_doenca_contagiosa = self.doenca_contagiosa_entry.get().lower() == 'sim' if self.doenca_contagiosa_entry.get() else self.paciente.doenca_contagiosa
        novas_alergias = self.alergias_entry.get() if self.alergias_entry.get() else self.paciente.alergias
        novos_sintomas = self.sintomas_entry.get() if self.sintomas_entry.get() else self.paciente.sintomas

        # Passe o sexo existente
        paciente_atualizado = Paciente(
            self.paciente.nome, self.paciente.sobrenome, nova_idade, self.paciente.sexo,
            nova_hipertensa, nova_doenca_contagiosa, novas_alergias, novos_sintomas
        )

        self.callback()
        self.top.destroy()

    def atualizar_data_hora_registro(self):
        nova_data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.paciente.data_hora_registro = nova_data_hora
        self.data_hora_registro_label.config(text=f"Data/Hora do Registro: {nova_data_hora}")
