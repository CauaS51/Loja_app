# Código a ser implementado

# import customtkinter as ctk
# from tkinter import messagebox

# # === FUNÇÃO: EXIBIR TELA DE INFORMAÇÕES DO USUÁRIO ===
# def mostrar_info_usuario(app):
#     for w in app.winfo_children():
#         w.destroy()
#     app.title("👤 Informações do Usuário")

# ctk.CTkLabel(
#         None,
#         text="👤 Informações do Usuário",
#         text_color=None,                                                #Editar cores
#         font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")     
#     ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

# # Frame de informações do usuário
# FRAME = ctk.CTkFrame( None,fg_color=None, corner_radius=12)             #Editar cores
# FRAME.pack(fill="x", pady=(0, 20))

# ctk.CTkLabel(
#     FRAME,
#     text="Dados Pessoais",
#     text_color=None,                                                    #Editar cores
#     font=ctk.CTkFont(size=18, weight="bold")
# ).pack(anchor="w", padx=20, pady=(15, 10))

# user_info = [
#     ("👤 Nome:", "Maria Silva Santos"),
#     ("📧 E-mail:", "maria.silva@email.com"),
#     ("📞 Telefone:", "(11) 98765-4321"),
#     ("📍 Endereço:", "Rua das Flores, 123 - São Paulo/SP")
# ]

# for label, value in user_info:
#     row = ctk.CTkFrame(FRAME, fg_color="transparent")
#     row.pack(fill="x", padx=20, pady=5)
#     ctk.CTkLabel(row, text=label, text_color=None, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
#     ctk.CTkLabel(row, text=value, text_color=None, font=ctk.CTkFont(size=14)).pack(side="left", padx=(10, 0))
