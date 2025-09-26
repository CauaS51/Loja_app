import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import menu
import cadastro
import feedbacks

# === CONFIGURAÇÃO INICIAL ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# === JANELA PRINCIPAL ===
app = ctk.CTk()
app.geometry("1200x700")
app.minsize(900, 500)  # tamanho mínimo para manter responsividade
app.title("Menu Inicial")

# CONFIGURAÇÃO GRID PRINCIPAL
app.grid_rowconfigure(0, weight=1)   # linha 0 expande
app.grid_columnconfigure(0, weight=1)  # coluna esquerda
app.grid_columnconfigure(1, weight=1)  # coluna direita

# === FRAME ESQUERDA (LOGIN) ===
frame_left = ctk.CTkFrame(app, corner_radius=0, fg_color="#F5F5F5")
frame_left.grid(row=0, column=0, sticky="nsew")

# CONFIGURA GRID INTERNO DO FRAME_LEFT
frame_left.grid_rowconfigure(0, weight=1)
frame_left.grid_rowconfigure(1, weight=2)
frame_left.grid_rowconfigure(2, weight=1)
frame_left.grid_columnconfigure(0, weight=1)

# CONTAINER CENTRAL (para centralizar tudo)
login_container = ctk.CTkFrame(frame_left, fg_color="transparent")
login_container.grid(row=1, column=0, sticky="nsew")

# NOME LOJA
label_name = ctk.CTkLabel(login_container, text="SUPERMERCADO", font=("Comfortaa", 35, "bold"), 
                          text_color="#3A3A3A",
                          anchor="w")
label_name.pack(pady=(40,50),padx=(0,0))

# TÍTULO
label_title = ctk.CTkLabel(login_container, text="BEM VINDO!", font=("Comfortaa", 40, "bold"), 
                           text_color="#3A3A3A",
                           anchor="w")
label_title.pack(pady=(0,10),padx=(0,60))

# SUBTÍTULO
label_subtitle = ctk.CTkLabel(login_container, text="Gerencie sua loja de forma prática e rápida ", font=("Arial", 16,"bold"), 
                              text_color="#3A3A3A",
                              anchor="w")
label_subtitle.pack(pady=(0,10),padx=(40,10))

# CAMPO USUÁRIO
entry_user = ctk.CTkEntry(login_container, placeholder_text="👤 Usuário", font=("Arial", 14,"bold"),
                          placeholder_text_color="#3A3A3A",
                          width=300, height=45, corner_radius=10)
entry_user.pack(pady=8)

# CAMPO SENHA
entry_pass = ctk.CTkEntry(login_container, placeholder_text="🔒 Senha", font=("Arial", 14,"bold"),
                          placeholder_text_color="#3A3A3A",
                          show="*", width=300, height=45, corner_radius=10)
entry_pass.pack(pady=8)

# BOTÃO ESQUECI MINHA SENHA
def esqueci_senha():
    print("A opção 'Esqueci minha senha' foi clicada!")

btn_forgot_pass = ctk.CTkButton(master=login_container,
                                text="Esqueceu sua senha?",
                                fg_color="transparent",
                                hover_color="#E8E8E8",
                                font=("Segoe UI", 13,"bold"),
                                text_color="#3A3A3A",
                                command=esqueci_senha,
                                anchor="w"
)
btn_forgot_pass.pack(pady=(5, 15), padx=(10,180))

# === FUNÇÃO: VALIDAÇÃO DO LOGIN ===
def on_login():
    user = entry_user.get().strip()
    pwd  = entry_pass.get().strip()
    if not user or not pwd:
        messagebox.showwarning("Atenção", "Informe usuário e senha.")
        return
    app.destroy()
    menu.mostrar_menu()

# BOTÃO DE LOGIN
btn_login = ctk.CTkButton(login_container, text="Entrar", font=("Arial", 15, "bold"),
                          width=300, height=45, 
                          corner_radius=10,
                          fg_color="#E98C41", hover_color="#E2B539", command=on_login)
btn_login.pack(pady=8)

# === FUNÇÃO: ABRIR CADASTRO ===
def abrir_cadastro():
    cadastro.abrir_cadastro()

# BOTÃO DE CADASTRO
btn_register = ctk.CTkButton(login_container, text="Cadastre-se", font=("Arial", 15, "bold"),
                             width=300, height=45, 
                             corner_radius=10,
                             fg_color="transparent", hover_color="#E2B539",
                             border_width=2, border_color="#E98C41", text_color="#E98C41", command=abrir_cadastro)
btn_register.pack(pady=8)

# === FRAME DIREITA (LOGO) ===
frame_right = ctk.CTkFrame(app, corner_radius=0, fg_color="#E98C41")
frame_right.grid(row=0, column=1, sticky="nsew")

frame_right.grid_rowconfigure(0, weight=0)  # config
frame_right.grid_rowconfigure(1, weight=1)  # logo
frame_right.grid_rowconfigure(2, weight=0)  # footer
frame_right.grid_columnconfigure(0, weight=1)

# BOTÃO DE CONFIGURAÇÕES
btn_config = ctk.CTkButton(frame_right, text="⚙️", font=("Arial", 15, "bold"),
                           width=40, height=40, corner_radius=10,
                           fg_color="white", hover_color="#818181",
                           border_width=2, border_color="#3A3A3A", text_color="#3A3A3A")
btn_config.grid(row=0, column=0, sticky="ne", padx=20, pady=20)

# LOGO (IMAGEM)
logo_image = ctk.CTkImage(light_image=Image.open("images/logo_loja.png"),
                          dark_image=Image.open("images/logo_loja.png"),
                          size=(400, 330))

logo_label = ctk.CTkLabel(frame_right, image=logo_image, text="")
logo_label.grid(row=1, column=0, sticky="nsew")

# === RODAPÉ (dentro do frame_right) ===
frame_footer = ctk.CTkFrame(frame_right, corner_radius=0, fg_color="#E98C41", height=80)
frame_footer.grid(row=2, column=0, sticky="ew")
frame_footer.grid_propagate(False)

# Container para os links
links_frame = ctk.CTkFrame(frame_footer, fg_color="transparent")
links_frame.pack(pady=(20,20))

# Funções para cada botão
def abrir_politica():
    win = ctk.CTkToplevel(app)
    win.title("Política de Privacidade")
    ctk.CTkLabel(win, text="Política de Privacidade", font=("Arial", 20, "bold")).pack(pady=20)

def abrir_suporte():
    win = ctk.CTkToplevel(app)
    win.title("Suporte")
    ctk.CTkLabel(win, text="Suporte", font=("Arial", 20, "bold")).pack(pady=20)

def abrir_comentarios():
    feedbacks.coletar_satisfacao()

# Botões estilo link
def hover_underline(widget, base_font=("Arial", 14, "bold")):
    widget.bind("<Enter>", lambda e: widget.configure(font=(base_font[0], base_font[1], "underline", "bold")))
    widget.bind("<Leave>", lambda e: widget.configure(font=base_font))

btn_politica = ctk.CTkButton(links_frame, text="Política de Privacidade", font=("Arial", 14, "bold"),
                              fg_color="transparent", hover_color="#E98C41",
                              text_color="#FFFFFF", command=abrir_politica)
btn_politica.pack(side="left")


ctk.CTkLabel(links_frame, text="|", text_color="#FFFFFF", font=("Arial", 12)).pack(side="left", padx=1)


btn_suporte = ctk.CTkButton(links_frame, text="Suporte", font=("Arial", 14, "bold"),
                              fg_color="transparent", hover_color="#E98C41",
                              text_color="#FFFFFF", command=abrir_suporte)
btn_suporte.pack(side="left")


ctk.CTkLabel(links_frame, text="|", text_color="#FFFFFF", font=("Arial", 12)).pack(side="left", padx=1)


btn_comentarios = ctk.CTkButton(links_frame, text="Comentários", font=("Arial", 14, "bold"),
                              fg_color="transparent", hover_color="#E98C41",
                              text_color="#FFFFFF", command=abrir_comentarios)
btn_comentarios.pack(side="left")

hover_underline(btn_politica)
hover_underline(btn_suporte)
hover_underline(btn_comentarios)

footer_label = ctk.CTkLabel(frame_footer,
                            text="\n📞 (91)98765-4321   🌐 www.projetoloja.com",
                            text_color="#FFFFFF", font=("Arial", 14, "bold"))
footer_label.pack(expand=True, pady=5)

# === EXECUTA O APP ===
app.mainloop()