import customtkinter as ctk
from tkinter import messagebox

# === FUNÇÃO: CADASTRO ===
def abrir_cadastro(app):
    cadastro_win = ctk.CTkToplevel()
    cadastro_win.title("Cadastro de Usuário")
    largura, altura =900, 600
    cadastro_win.geometry(f"{largura}x{altura}")

    # Faz a janela ficar acima da janela principal
    cadastro_win.transient(app)  # "app" é a janela principal
    cadastro_win.grab_set()      # impede interações com a janela principal até fechar a de cadastro

    # CENTRALIZA A JANELA DE CADASTRO SOBRE A JANELA PRINCIPAL
    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app_largura = app.winfo_width()
    app_altura = app.winfo_height()

    x = app_x + (app_largura // 2) - (largura // 2)
    y = app_y + (app_altura // 2) - (altura // 2)
    cadastro_win.geometry(f"{largura}x{altura}+{x}+{y}")
    
    ctk.CTkLabel(cadastro_win, text="Cadastro", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)
    entry_nome_cad = ctk.CTkEntry(cadastro_win, placeholder_text="Nome completo", width=300, height=40)
    entry_nome_cad.pack(pady=10)

    entry_user_cad = ctk.CTkEntry(cadastro_win, placeholder_text="Usuário", width=300, height=40)
    entry_user_cad.pack(pady=10)

    entry_email = ctk.CTkEntry(cadastro_win, placeholder_text="Email", show="*", width=300, height=40)
    entry_email.pack(pady=10)
    
    entry_confirm_email = ctk.CTkEntry(cadastro_win, placeholder_text="Confirmar Email", show="*", width=300, height=40)
    entry_confirm_email.pack(pady=10)

    entry_pass_cad = ctk.CTkEntry(cadastro_win, placeholder_text="Senha", show="*", width=300, height=40)
    entry_pass_cad.pack(pady=10)
    
    entry_confirm_pass_cad = ctk.CTkEntry(cadastro_win, placeholder_text="Confirmar Senha", show="*", width=300, height=40)
    entry_confirm_pass_cad.pack(pady=10)
    

    def fechar_cadastro():
        cadastro_win.destroy()  

    ctk.CTkButton(
        cadastro_win,
        text="Cadastrar",
        width=200, height=40,
        fg_color="#E98C41",
        hover_color="#E98C41",
        command=lambda: messagebox.showinfo("Sucesso", f"Usuário '{entry_user_cad.get()}' cadastrado!") and fechar_cadastro()
).pack(pady=20)