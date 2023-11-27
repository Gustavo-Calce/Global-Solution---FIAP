import tkinter as tk
from tkinter import messagebox
from Login import Login
from HospitalApp import HospitalApp

def on_login_success():
    root = tk.Tk()
    hospital_app = HospitalApp(root, usuario_autenticado=True)  
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()

    # Mostrar a tela de login
    login_screen = Login(root, on_login_success)

    root.mainloop()