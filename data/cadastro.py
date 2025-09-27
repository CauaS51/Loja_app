import customtkinter as ctk
from tkinter import messagebox

# === FUNÇÃO: CADASTRO ===
def abrir_cadastro():
    cadastro_win = ctk.CTkInputDialog()
    cadastro_win.title("Cadastro de Usuário")
    cadastro_win.geometry("900x600")
    
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
    
    ctk.CTkButton(
        cadastro_win,
        text="Cadastrar",
        width=200, height=40,
        fg_color="#E98C41",
        hover_color="#E98C41",
        command=lambda: messagebox.showinfo("Sucesso", f"Usuário '{entry_user_cad.get()}' cadastrado!")
    ).pack(pady=20) 
    
    cadastro_win.mainloop()