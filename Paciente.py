from datetime import datetime
class Paciente:
    def __init__(self, nome, sobrenome, cpf, idade, sexo, hipertensa, doenca_contagiosa, alergias, sintomas,
                 descricao_doenca_contagiosa=None,detalhes_dialog=None, descricao_alergias=None, consultas=None, data_hora_registro=None):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.idade = idade
        self.sexo = sexo
        self.hipertensa = hipertensa
        self.doenca_contagiosa = doenca_contagiosa
        self.alergias = alergias
        self.sintomas = sintomas
        self.descricao_doenca_contagiosa = descricao_doenca_contagiosa
        self.descricao_alergias = descricao_alergias
        self.detalhes_dialog = None
        self.consultas = consultas if consultas is not None else []
        self.data_hora_registro = data_hora_registro or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def registrar_consulta(self, medico, especialidade):
        data_hora_consulta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        consulta = {
            'medico': medico,
            'especialidade': especialidade,
            'data_hora': data_hora_consulta
        }
        self.consultas.append(consulta)
        # Manter apenas as últimas 3 consultas
        self.consultas = self.consultas[-3:]

    def obter_relatorio(self):
        relatorio = f"Relatório Médico para {self.nome} {self.sobrenome}:\n"
        relatorio += "\nÚltimas Consultas:\n"
        for consulta in self.consultas:
            relatorio += f"Data/Hora: {consulta['data_hora']}, Médico: {consulta['medico']}, " \
                          f"Especialidade: {consulta['especialidade']}\n"
        return relatorio

    def __str__(self):
        return f"{self.nome} {self.sobrenome}, {self.idade} anos, Sexo: {self.sexo}, " \
               f"Hipertensa: {self.hipertensa}, Doença Contagiosa: {self.doenca_contagiosa}, " \
               f"Alergias: {self.alergias}, Sintomas: {self.sintomas}, " \
               f"Descrição de Doenças Contagiosas: {self.descricao_doenca_contagiosa}, " \
               f"Descrição de Alergias: {self.descricao_alergias}, " \
               f"Data/Hora do Registro: {self.data_hora_registro}"
               
    def definir_detalhes_dialog(self, detalhes_dialog):
        self.detalhes_dialog = detalhes_dialog