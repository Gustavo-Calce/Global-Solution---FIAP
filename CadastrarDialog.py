import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Paciente import Paciente
class CadastrarDialog:
    def __init__(self, root, callback, hospital_app_instance):
        self.top = tk.Toplevel(root)
        self.top.title("Cadastrar Paciente")

        self.data_hora_label = tk.Label(self.top, text="Data/Hora do Registro:")
        self.data_hora_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.data_hora_registro_label = tk.Label(self.top, text="")
        self.data_hora_registro_label.grid(row=0, column=2, padx=5, pady=5)
        self.data_hora_registro_label.config(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        self.nome_label = tk.Label(self.top, text="Nome:")
        self.nome_label.grid(row=1, column=0, padx=5, pady=5)
        self.nome_entry = tk.Entry(self.top)
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5)

        self.sobrenome_label = tk.Label(self.top, text="Sobrenome:")
        self.sobrenome_label.grid(row=2, column=0, padx=5, pady=5)
        self.sobrenome_entry = tk.Entry(self.top)
        self.sobrenome_entry.grid(row=2, column=1, padx=5, pady=5)

        self.cpf_label = tk.Label(self.top, text="CPF:")
        self.cpf_label.grid(row=3, column=0, padx=5, pady=5)
        self.cpf_entry = tk.Entry(self.top)
        self.cpf_entry.grid(row=3, column=1, padx=5, pady=5)

        self.idade_label = tk.Label(self.top, text="Idade:")
        self.idade_label.grid(row=4, column=0, padx=5, pady=5)
        self.idade_entry = tk.Entry(self.top)
        self.idade_entry.grid(row=4, column=1, padx=5, pady=5)

        self.sexo_label = tk.Label(self.top, text="Sexo:")
        self.sexo_label.grid(row=5, column=0, padx=5, pady=5)
        self.sexo_var = tk.StringVar()
        self.sexo_var.set("Masculino")  # Valor padrão
        self.sexo_button = tk.Button(self.top, textvariable=self.sexo_var, command=self.toggle_sexo)
        self.sexo_button.grid(row=5, column=1, padx=5, pady=5)
        self.sexo_value_label = tk.Label(self.top, text="")
        self.sexo_value_label.grid(row=6, column=1, padx=5, pady=5)

        self.hipertensa_label = tk.Label(self.top, text="Hipertensa:")
        self.hipertensa_label.grid(row=6, column=0, padx=5, pady=5)
        self.hipertensa_var = tk.StringVar()
        self.hipertensa_var.set("Não")  # Valor padrão
        self.hipertensa_button = tk.Button(self.top, textvariable=self.hipertensa_var, command=self.toggle_hipertensa)
        self.hipertensa_button.grid(row=6, column=1, padx=5, pady=5)

        self.doenca_contagiosa_label = tk.Label(self.top, text="Doença Contagiosa:")
        self.doenca_contagiosa_label.grid(row=7, column=0, padx=5, pady=5)
        self.doenca_contagiosa_var = tk.StringVar()
        self.doenca_contagiosa_var.set("Não")  # Valor padrão
        self.doenca_contagiosa_button = tk.Button(self.top, textvariable=self.doenca_contagiosa_var, command=self.toggle_doenca_contagiosa)
        self.doenca_contagiosa_button.grid(row=7, column=1, padx=5, pady=5)

        self.doenca_contagiosa_descricao_label = tk.Label(self.top, text="Descrição de Doenças Contagiosas:")
        self.doenca_contagiosa_descricao_label.grid(row=8, column=0, padx=5, pady=5)
        self.doenca_contagiosa_descricao_entry = tk.Entry(self.top)
        self.doenca_contagiosa_descricao_entry.grid(row=8, column=1, padx=5, pady=5)

        self.alergias_label = tk.Label(self.top, text="Alergias:")
        self.alergias_label.grid(row=9, column=0, padx=5, pady=5)
        self.alergias_var = tk.StringVar()
        self.alergias_var.set("Não")  # Valor padrão
        self.alergias_button = tk.Button(self.top, textvariable=self.alergias_var, command=self.toggle_alergias)
        self.alergias_button.grid(row=9, column=1, padx=5, pady=5)

        self.alergias_descricao_label = tk.Label(self.top, text="Descrição de Alergias:")
        self.alergias_descricao_label.grid(row=10, column=0, padx=5, pady=5)
        self.alergias_descricao_entry = tk.Entry(self.top)
        self.alergias_descricao_entry.grid(row=10, column=1, padx=5, pady=5)

        self.sintomas_label = tk.Label(self.top, text="Sintomas:")
        self.sintomas_label.grid(row=11, column=0, padx=5, pady=5)
        self.sintomas_entry = tk.Entry(self.top)
        self.sintomas_entry.grid(row=11, column=1, padx=5, pady=5)

        self.cadastrar_button = tk.Button(self.top, text="Cadastrar", command=self.cadastrar)
        self.cadastrar_button.grid(row=12, column=0, columnspan=2, pady=10)

        self.paciente_cadastrado = None
        self.callback_function = callback
        self.hospital_app_instance = hospital_app_instance
        
        self.sexo_value_label = tk.Label(self.top, text=self.sexo_var.get())
        self.sexo_value_label.grid(row=5, column=2, padx=5, pady=5)
        
        self.hipertensa_value_label = tk.Label(self.top, text=self.hipertensa_var.get())
        self.hipertensa_value_label.grid(row=6, column=2, padx=5, pady=5)
        
        self.doenca_contagiosa_value_label = tk.Label(self.top, text=self.doenca_contagiosa_var.get())
        self.doenca_contagiosa_value_label.grid(row=7, column=2, padx=5, pady=5)
        
        self.alergias_value_label = tk.Label(self.top, text=self.alergias_var.get())
        self.alergias_value_label.grid(row=9, column=2, padx=5, pady=5)


    def toggle_sexo(self):
        if self.sexo_var.get() == "Masculino":
            self.sexo_var.set("Feminino")
        else:
            self.sexo_var.set("Masculino")
        self.sexo_value_label.config(text=self.sexo_var.get())

    def toggle_hipertensa(self):
        if self.hipertensa_var.get() == "Sim":
            self.hipertensa_var.set("Não")
        else:
            self.hipertensa_var.set("Sim")
        self.hipertensa_value_label.config(text=self.hipertensa_var.get())

    def toggle_doenca_contagiosa(self):
        if self.doenca_contagiosa_var.get() == "Sim":
            self.doenca_contagiosa_var.set("Não")
            self.doenca_contagiosa_descricao_entry.config(state=tk.DISABLED)
        else:
            self.doenca_contagiosa_var.set("Sim")
            self.doenca_contagiosa_descricao_entry.config(state=tk.NORMAL)
        self.doenca_contagiosa_value_label.config(text=self.doenca_contagiosa_var.get())

    def toggle_alergias(self):
        if self.alergias_var.get() == "Sim":
            self.alergias_var.set("Não")
            self.alergias_descricao_entry.config(state=tk.DISABLED)
        else:
            self.alergias_var.set("Sim")
            self.alergias_descricao_entry.config(state=tk.NORMAL)
        self.alergias_value_label.config(text=self.alergias_var.get())

    def cadastrar(self):
        data_hora_registro = self.data_hora_registro_label.cget("text") 
        nome = self.nome_entry.get()
        sobrenome = self.sobrenome_entry.get()
        cpf = self.cpf_entry.get()
        idade = int(self.idade_entry.get())
        sexo = self.sexo_var.get()
        hipertensa = self.hipertensa_var.get().lower() == 'sim'
        doenca_contagiosa = self.doenca_contagiosa_var.get().lower() == 'sim'
        descricao_doenca_contagiosa = self.doenca_contagiosa_descricao_entry.get() if doenca_contagiosa else None
        alergias = self.alergias_var.get().lower() == 'sim'
        descricao_alergias = self.alergias_descricao_entry.get() if alergias else None
        sintomas = self.sintomas_entry.get()

        paciente = Paciente(
            nome, sobrenome, cpf, idade, sexo, hipertensa, doenca_contagiosa,
            alergias, sintomas, descricao_doenca_contagiosa, descricao_alergias
        )

        medico = "Dr. Exemplo"  # Substituir pelo nome real do médico
        especialidade = "Clínico Geral"  # Substituir pela especialidade real

        paciente.registrar_consulta(medico, especialidade)

        # Validar o CPF
        if not self.validar_cpf(cpf):
            messagebox.showerror("Erro de Validação", "CPF inválido. Tente outro CPF.")
            return

        # Verificar se o paciente já existe
        paciente_existente = None
        for paciente in self.hospital_app_instance.pacientes:
            if paciente.cpf == cpf:
                paciente_existente = paciente
                break

        if paciente_existente:
        # Atualizar as informações do paciente existente
            paciente_existente.__dict__.update({
                'nome': nome,
                'sobrenome': sobrenome,
                'idade': idade,
                'sexo': sexo,
                'hipertensa': hipertensa,
                'doenca_contagiosa': doenca_contagiosa,
                'descricao_doenca_contagiosa': descricao_doenca_contagiosa,
                'alergias': alergias,
                'descricao_alergias': descricao_alergias,
                'sintomas': sintomas
            })
        else:
        # Criar um novo paciente
            paciente = Paciente(
            nome, sobrenome, cpf, idade, self.sexo_var.get(),
            self.hipertensa_var.get().lower() == 'sim',
            self.doenca_contagiosa_var.get().lower() == 'sim',
            descricao_doenca_contagiosa, 
            self.alergias_var.get().lower() == 'sim',
            descricao_alergias, sintomas
        )
            self.hospital_app_instance.pacientes.append(paciente)

    # Atualizar a lista e chamar a função de callback
        self.hospital_app_instance.atualizar_lista()
        self.hospital_app_instance.salvar_pacientes()  # Salvar pacientes após a atualização
        self.callback_function()
        self.top.destroy()


    def validar_cpf(self, cpf):
        # Retira apenas os dígitos do CPF, ignorando os caracteres especiais
        numeros = [int(digito) for digito in cpf if digito.isdigit()]

        if len(numeros) != 11:
            return False

        soma_produtos = sum(a * b for a, b in zip(numeros[0:9], range(10, 1, -1)))
        digito_esperado = (soma_produtos * 10) % 11 % 10
        if numeros[9] != digito_esperado:
            return False

        soma_produtos1 = sum(a * b for a, b in zip(numeros[0:10], range(11, 1, -1)))
        digito_esperado1 = (soma_produtos1 * 10) % 11 % 10
        if numeros[10] != digito_esperado1:
            return False

        return True