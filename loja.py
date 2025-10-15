import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import data.colors as colors
from data.colors import *
import data.menu as menu
import data.cadastro as cadastro
import data.sessao as sessao

# === CONFIGURAÇÃO INICIAL ===
def mostrar_login(app):
    for w in app.winfo_children():
        w.destroy()
    
    ctk.set_default_color_theme("blue")

    # CONFIGURAÇÃO GRID PRINCIPAL
    app.title("Sistema Supermercado") 
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)  # lado esquerdo maior
    app.grid_columnconfigure(1, weight=1)  # lado direito menor

    # CORES
    cores = get_colors()

    # === FRAME ESQUERDA ===
    frame_left = ctk.CTkFrame(app, corner_radius=0, fg_color=cores["BACKGROUND"])
    frame_left.grid(row=0, column=0, sticky="nsew")
    frame_left.grid_rowconfigure(0, weight=1)
    frame_left.grid_rowconfigure(1, weight=2)
    frame_left.grid_rowconfigure(2, weight=1)
    frame_left.grid_columnconfigure(0, weight=1)

    # CONTAINER LOGIN
    login_container = ctk.CTkFrame(frame_left, fg_color="transparent")
    login_container.grid(row=1, column=0, sticky="nsew")

    # TÍTULOS
    ctk.CTkLabel(login_container, text="🏬 SUPERMERCADO", font=("Comfortaa", 35, "bold"),
                 text_color=cores["TEXT_PRIMARY"]).pack(pady=(50,50))
    ctk.CTkLabel(login_container, text="BEM VINDO!", font=("Comfortaa", 40, "bold"),
                 text_color=cores["TEXT_PRIMARY"]).pack(pady=(0,10), padx=(0,60))
    ctk.CTkLabel(login_container, text="Gerencie sua loja de forma prática e rápida",
                 font=("Arial", 16,"bold"), text_color=cores["TEXT_PRIMARY"]).pack(pady=(0,10), padx=(30,0))

    # CAMPOS
    entry_user = ctk.CTkEntry(login_container, placeholder_text="👤 Usuário", font=("Arial", 14,"bold"),
                              placeholder_text_color=cores["TEXT_PRIMARY"], width=300, height=45, corner_radius=10)
    entry_user.pack(pady=8)
    entry_pass = ctk.CTkEntry(login_container, placeholder_text="🔒 Senha", font=("Arial", 14,"bold"),
                              placeholder_text_color=cores["TEXT_PRIMARY"], show="*", width=300, height=45, corner_radius=10)
    entry_pass.pack(pady=8)

    # BOTÃO ESQUECI MINHA SENHA
    def esqueci_senha():
        print("A opção 'Esqueci minha senha' foi clicada!")
    ctk.CTkButton(login_container, text="Esqueceu sua senha?", fg_color="transparent",
                  hover_color="#E8E8E8", font=("Segoe UI", 13,"bold"),
                  text_color=cores["TEXT_PRIMARY"], command=esqueci_senha).pack(pady=(5,15), padx=(0,175))

    # --- FUNÇÃO LOGIN ---
    def on_login():
        user = entry_user.get().strip()
        pwd  = entry_pass.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Atenção", "Informe usuário e senha.")
            return
    
    # VERIFICA SE O USUÁRIO ESTÁ CADASTRADO
        if user in sessao.USUARIOS_FIXOS:
            info = sessao.USUARIOS_FIXOS[user]
            if pwd == info["senha"]:
                # Salva o usuário atual na sessão
                sessao.usuario = user
                sessao.perfil = info["perfil"]

                menu.mostrar_menu(app, usuario=user, perfil=info["perfil"])
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            # Usuário não encontrado → padrão “Caixa”
            messagebox.showerror("Erro","Usuário não Cadastrado")
    
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

    # === FRAME DIREITA ===
    frame_right = ctk.CTkFrame(app, corner_radius=0, fg_color="#E98C41")
    frame_right.grid(row=0, column=1, sticky="nsew")
    frame_right.grid_rowconfigure(0, weight=1)  # espaço acima do logo
    frame_right.grid_rowconfigure(1, weight=1)  # logo
    frame_right.grid_rowconfigure(2, weight=1)  # espaço abaixo do logo
    frame_right.grid_columnconfigure(0, weight=1)

    # === FUNÇÃO PARA ALTERNAR ENTRE MODO CLARO/ESCURO ===
    def alternar_tema():
        colors.alternar_tema()
        mostrar_login(app)

    # === BOTÃO ALTERNAR TEMA ===
    icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "☀️"
    theme_button = ctk.CTkButton(
        frame_right, 
        text=icone_tema, 
        width=30, 
        height=40,
        corner_radius=12, 
        fg_color=cores["ENTRY_BG"],
        hover_color=cores["HOVER"], 
        text_color=cores["TEXT_PRIMARY"],
        font=ctk.CTkFont(size=20), 
        command=alternar_tema
        )
    theme_button.grid(row=0, column=0, padx=20, pady=20, sticky="ne") 

    # LOGO
    logo_image = ctk.CTkImage(light_image=Image.open("images/logo_loja.png"),
                              dark_image=Image.open("images/logo_loja.png"),
                              size=(400, 330))
    ctk.CTkLabel(frame_right, image=logo_image, text="").grid(row=1, column=0)

    # === RODAPÉ ===
    frame_footer = ctk.CTkFrame(frame_right, corner_radius=0, fg_color="#E98C41", height=80)
    frame_footer.grid(row=2, column=0, sticky="ew")
    frame_footer.grid_propagate(False)

    links_frame = ctk.CTkFrame(frame_footer, fg_color="transparent")
    links_frame.pack(pady=(20,20))


    # LINKS DO RODAPÉ
    def abrir_politica():
        win = ctk.CTkToplevel(app)
        win.title("Políticas de Privacidade")
        ctk.CTkLabel(win, text="Política de Privacidade", font=("Arial", 20, "bold")).pack(pady=20)
        largura, altura =900, 600
        win.geometry(f"{largura}x{altura}")
        win.transient(app)  
        win.grab_set()
        app_x = app.winfo_x()
        app_y = app.winfo_y()
        app_largura = app.winfo_width()
        app_altura = app.winfo_height()
        x = app_x + (app_largura // 2) - (largura // 2)
        y = app_y + (app_altura // 2) - (altura // 2)
        win.geometry(f"{largura}x{altura}+{x}+{y}")

    def abrir_suporte():
        win = ctk.CTkToplevel(app)
        win.title("Suporte")
        ctk.CTkLabel(win, text="Suporte", font=("Arial", 20, "bold")).pack(pady=20)
        largura, altura =900, 600
        win.geometry(f"{largura}x{altura}")
        win.transient(app)  
        win.grab_set()
        app_x = app.winfo_x()
        app_y = app.winfo_y()
        app_largura = app.winfo_width()
        app_altura = app.winfo_height()
        x = app_x + (app_largura // 2) - (largura // 2)
        y = app_y + (app_altura // 2) - (altura // 2)
        win.geometry(f"{largura}x{altura}+{x}+{y}")

    def abrir_ajuda():
        win = ctk.CTkToplevel(app)
        win.title("Ajuda")
        ctk.CTkLabel(win, text="Suporte", font=("Arial", 20, "bold")).pack(pady=20)
        largura, altura =900, 600
        win.geometry(f"{largura}x{altura}")  
        win.transient(app)  
        win.grab_set()
        app_x = app.winfo_x()
        app_y = app.winfo_y()
        app_largura = app.winfo_width()
        app_altura = app.winfo_height()
        x = app_x + (app_largura // 2) - (largura // 2)
        y = app_y + (app_altura // 2) - (altura // 2)
        win.geometry(f"{largura}x{altura}+{x}+{y}")

    links = [("Políticas", abrir_politica),
             ("Suporte", abrir_suporte),
             ("Ajuda", abrir_ajuda)]

    for i, (text, cmd) in enumerate(links):
        btn = ctk.CTkButton(links_frame, text=text, font=("Arial", 13,"bold"),
                            width=0, height=0, corner_radius=0,
                            fg_color="transparent", hover_color="#E98C41",
                            text_color="#FFFFFF", command=cmd)
        btn.pack(side="left", padx=5)


        def hover_underline(widget, base_font=("Arial", 13, "bold")):
            widget.bind("<Enter>", lambda e: widget.configure(font=(base_font[0], base_font[1], "underline", "bold")))
            widget.bind("<Leave>", lambda e: widget.configure(font=base_font))
        hover_underline(btn)

        if i < len(links) - 1:
            sep = ctk.CTkLabel(links_frame, text="|", text_color="#FFFFFF", font=("Arial", 12))
            sep.pack(side="left", padx=1)

    # RODAPÉ INFORMAÇÕES DE CONTATO
    ctk.CTkLabel(frame_footer, text="\n📞 (91)98765-4321   🌐 www.projetoloja.com",
                 text_color="#FFFFFF", font=("Arial", 14, "bold")).pack(expand=True, pady=(0,50))

# === MAIN ===
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1200x700")
    app.minsize(900, 500)
    mostrar_login(app)
    app.mainloop()