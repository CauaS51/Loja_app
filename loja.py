import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import data.menu as menu
import data.cadastro as cadastro
import data.feedbacks as feedbacks

# === CONFIGURAÇÃO INICIAL ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# === JANELA PRINCIPAL ===
app = ctk.CTk()
app.geometry("1200x700")
app.minsize(900, 500)
app.title("Menu Inicial")

# === CONFIGURAÇÃO GRID PRINCIPAL ===
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# === FRAME ESQUERDA (LOGIN) ===
frame_left = ctk.CTkFrame(app, corner_radius=0, fg_color="#F5F5F5")
frame_left.grid(row=0, column=0, sticky="nsew")
frame_left.grid_rowconfigure(0, weight=1)
frame_left.grid_rowconfigure(1, weight=2)
frame_left.grid_rowconfigure(2, weight=1)
frame_left.grid_columnconfigure(0, weight=1)

# CONTAINER CENTRAL
login_container = ctk.CTkFrame(frame_left, fg_color="transparent")
login_container.grid(row=1, column=0, sticky="nsew")

# LABELS
ctk.CTkLabel(login_container, text="SUPERMERCADO", font=("Comfortaa", 35, "bold"),
             text_color="#3A3A3A").pack(pady=(40,50), padx=(0,0))

ctk.CTkLabel(login_container, text="BEM VINDO!", font=("Comfortaa", 40, "bold"),
             text_color="#3A3A3A").pack(pady=(0,10), padx=(0,60))

ctk.CTkLabel(login_container, text="Gerencie sua loja de forma prática e rápida",
             font=("Arial", 16,"bold"), text_color="#3A3A3A").pack(pady=(0,10), padx=(40,10))

# ENTRYS 
entry_user = ctk.CTkEntry(login_container, placeholder_text="👤 Usuário", font=("Arial", 14,"bold"),
                          placeholder_text_color="#3A3A3A", width=300, height=45, corner_radius=10)
entry_user.pack(pady=8)

entry_pass = ctk.CTkEntry(login_container, placeholder_text="🔒 Senha", font=("Arial", 14,"bold"),
                          placeholder_text_color="#3A3A3A", show="*", width=300, height=45, corner_radius=10)
entry_pass.pack(pady=8)

# BOTÃO ESQUECI MINHA SENHA
def esqueci_senha():
    print("A opção 'Esqueci minha senha' foi clicada!")

ctk.CTkButton(login_container, text="Esqueceu sua senha?", fg_color="transparent",
               hover_color="#E8E8E8", font=("Segoe UI", 13,"bold"),
               text_color="#3A3A3A", command=esqueci_senha).pack(pady=(5,15), padx=(10,180))

# FUNCÃO LOGIN
def on_login():
    user = entry_user.get().strip()
    pwd  = entry_pass.get().strip()
    if not user or not pwd:
        messagebox.showwarning("Atenção", "Informe usuário e senha.")
        return
    # Chama menu passando a mesma janela
    menu.mostrar_menu(app)

# BOTÃO LOGIN
ctk.CTkButton(login_container, text="Entrar", font=("Arial", 15, "bold"),
              width=300, height=45, corner_radius=10,
              fg_color="#E98C41", hover_color="#E2B539", command=on_login).pack(pady=8)

# BOTÃO CADASTRO
def abrir_cadastro():
    cadastro.abrir_cadastro(app)

ctk.CTkButton(login_container, text="Cadastre-se", font=("Arial", 15, "bold"),
              width=300, height=45, corner_radius=10,
              fg_color="transparent", hover_color="#E2B539",
              border_width=2, border_color="#E98C41", text_color="#E98C41",
              command=abrir_cadastro).pack(pady=8)

# === FRAME DIREITA (LOGO) ===
frame_right = ctk.CTkFrame(app, corner_radius=0, fg_color="#E98C41")
frame_right.grid(row=0, column=1, sticky="nsew")
frame_right.grid_rowconfigure(0, weight=0)
frame_right.grid_rowconfigure(1, weight=1)
frame_right.grid_rowconfigure(2, weight=0)
frame_right.grid_columnconfigure(0, weight=1)

# BOTÃO CONFIGURAÇÕES
ctk.CTkButton(frame_right, text="⚙️", font=("Arial", 20, "bold"),
              width=40, height=40, corner_radius=10,
              fg_color="white", hover_color="#818181",
              border_width=2, border_color="#3A3A3A", text_color="#3A3A3A").grid(row=0, column=0, sticky="ne", padx=20, pady=20)

# LOGO
logo_image = ctk.CTkImage(light_image=Image.open("images/logo_loja.png"),
                          dark_image=Image.open("images/logo_loja.png"),
                          size=(400, 330))
ctk.CTkLabel(frame_right, image=logo_image, text="").grid(row=1, column=0, sticky="nsew")







# === RODAPÉ ===
frame_footer = ctk.CTkFrame(frame_right, corner_radius=0, fg_color="#E98C41", height=80)
frame_footer.grid(row=2, column=0, sticky="ew")
frame_footer.grid_propagate(False)

# Configura o grid do rodapé para centralizar
frame_footer.grid_columnconfigure(0, weight=1)  # espaço à esquerda
frame_footer.grid_columnconfigure(1, weight=0)  # conteúdo central
frame_footer.grid_columnconfigure(2, weight=1)  # espaço à direita

# === LINKS (linha 0, centralizado) ===
links_frame = ctk.CTkFrame(frame_footer, fg_color="transparent")
links_frame.grid(row=0, column=1, pady=(10, 0))

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

# Botões link com underline e separadores "|"
links = [("Política de Privacidade", abrir_politica),
         ("Suporte", abrir_suporte),
         ("Comentários", abrir_comentarios)]

for i, (text, cmd) in enumerate(links):
    btn = ctk.CTkButton(links_frame, text=text, font=("Arial",13,"bold"),
                         fg_color="transparent", hover_color="#E98C41",
                         text_color="#FFFFFF", command=cmd)
    btn.pack(side="left", padx=(0,0))
    
    # Efeito underline ao passar o mouse
    def hover_underline(widget, base_font=("Arial", 13, "bold")):
        widget.bind("<Enter>", lambda e: widget.configure(font=(base_font[0], base_font[1], "underline", "bold")))
        widget.bind("<Leave>", lambda e: widget.configure(font=base_font))
    
    hover_underline(btn)
    
    # Adiciona separador "|" se não for o último botão
    if i < len(links) - 1:
        sep = ctk.CTkLabel(links_frame, text="|", text_color="#FFFFFF", font=("Arial", 13))
        sep.pack(side="left", padx=2)

# === CONTATO (linha 1, centralizado) ===
info_frame = ctk.CTkFrame(frame_footer, fg_color="transparent")
info_frame.grid(row=1, column=1, pady=(5,10))

# 📞 Telefone
phone_icon = ctk.CTkLabel(info_frame, text="📞", text_color="#FFFFFF", font=("Arial", 22, "bold"))
phone_icon.grid(row=0, column=0, padx=(0,5))

phone_text = ctk.CTkLabel(info_frame, text="(91) 98765-4321", text_color="#FFFFFF", font=("Arial", 13, "bold"))
phone_text.grid(row=0, column=1, padx=(0,20))

# 🌐 Site
web_icon = ctk.CTkLabel(info_frame, text="🌐", text_color="#FFFFFF", font=("Arial", 22, "bold"))
web_icon.grid(row=0, column=2, padx=(0,5))

web_text = ctk.CTkLabel(info_frame, text="www.projetoloja.com", text_color="#FFFFFF", font=("Arial", 13, "bold"))
web_text.grid(row=0, column=3)


# === EXECUTA O APP ===
app.mainloop()