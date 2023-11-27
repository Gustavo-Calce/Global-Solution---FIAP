import tkinter as tk
from tkinter import messagebox
import hashlib

class Login:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success

        self.root.title("Login")
        self.root.geometry("350x200")

        self.label_username = tk.Label(root, text="Nome de Usuário:")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(root)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(root, text="Senha:")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(pady=5)

        # Adicione um fundo diferente ao botão de login
        self.login_button = tk.Button(root, text="Login", command=self.login, bg="lightblue")
        self.login_button.pack(pady=10)

        # Adicione um efeito de destaque ao passar o mouse sobre o botão
        self.login_button.bind("<Enter>", self.on_enter)
        self.login_button.bind("<Leave>", self.on_leave)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.authenticate(username, password):
            self.on_login_success()
            self.close_login_window()  # Fechar a janela de login
        else:
            messagebox.showerror("Erro de Autenticação", "Nome de usuário ou senha incorretos.")

    def authenticate(self, username, password):
        stored_password_hash = self.get_stored_password_hash(username)
        entered_password_hash = self.hash_password(password)

        return stored_password_hash == entered_password_hash

    def get_stored_password_hash(self, username):
        stored_password = {"admin": "5f4dcc3b5aa765d61d8327deb882cf99"}  # Senha padrão: "password"
        return stored_password.get(username, "")

    def hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def on_enter(self, e):
        self.login_button.config(bg="lightcyan")

    def on_leave(self, e):
        self.login_button.config(bg="lightblue")

    def close_login_window(self):
        self.root.destroy()

def on_login_success(login_window):
    login_window.close_login_window()
    root = tk.Tk()
    hospital_app = HospitalApp(root)
    root.mainloop()

class HospitalApp:
    def __init__(self, root):
        self.root = root

        self.show_login_screen()

    def show_login_screen(self):
        login_screen = Login(self.root, lambda: on_login_success(login_screen))

    def initialize_app(self):
        self.root.title("Cadastro de Pacientes em Hospitais")
        self.root.geometry("650x450")

if __name__ == "__main__":
    root = tk.Tk()

    # Mostrar a tela de login
    login_screen = Login(root, lambda: on_login_success(login_screen))
    root.mainloop()
