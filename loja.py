import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from data.colors import *
import data.menu as menu
import data.cadastro as cadastro


# === CONFIGURAÇÃO INICIAL ===
def mostrar_login(app):
    for w in app.winfo_children():
        w.destroy()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # CONFIGURAÇÃO GRID PRINCIPAL
    app.title("Sistema Supermercado") 
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)  # lado esquerdo maior
    app.grid_columnconfigure(1, weight=1)  # lado direito menor

    # === FRAME ESQUERDA (LOGIN) ===
    frame_left = ctk.CTkFrame(app, corner_radius=0, fg_color="#F5F5F5")
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
                 text_color="#3A3A3A").pack(pady=(50,50))
    ctk.CTkLabel(login_container, text="BEM VINDO!", font=("Comfortaa", 40, "bold"),
                 text_color="#3A3A3A").pack(pady=(0,10), padx=(0,60))
    ctk.CTkLabel(login_container, text="Gerencie sua loja de forma prática e rápida",
                 font=("Arial", 16,"bold"), text_color="#3A3A3A").pack(pady=(0,10), padx=(30,0))

    # CAMPOS
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
                  text_color="#3A3A3A", command=esqueci_senha).pack(pady=(5,15), padx=(0,175))

    # --- FUNÇÃO LOGIN ---
    def on_login():
        user = entry_user.get().strip()
        pwd  = entry_pass.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Atenção", "Informe usuário e senha.")
            return
    
    # --- USUÁRIOS FIXOS PARA TESTE ---
        elif user == "DEV" and pwd != "123":
            menu.mostrar_menu(app, usuario="DEV", perfil="Desenvolvedor")
        
        elif user == "Cauã" and pwd == "123":
            menu.mostrar_menu(app, usuario="Cauã", perfil="Desenvolvedor")

        elif user == "Isaac" and pwd == "123":
            menu.mostrar_menu(app, usuario="Isaac", perfil="Desenvolvedor")
        
        elif user == "Lucas" and pwd == "123":
            menu.mostrar_menu(app, usuario="Lucas", perfil="Desenvolvedor")

        elif user == "Romulo" and pwd == "123":
            menu.mostrar_menu(app, usuario="Romulo", perfil="Desenvolvedor")
        
        elif user == "Caixa" and pwd == "123":
            menu.mostrar_menu(app, usuario="Caixa", perfil="Caixa")
        
        elif user == "Reposição" and pwd == "123":
            menu.mostrar_menu(app, usuario="Reposição", perfil="Reposição")
        
        elif user == "Admin" and pwd == "123":
            menu.mostrar_menu(app, usuario="Admin", perfil="Administração")       

        else:
            menu.mostrar_menu(app, usuario=user, perfil="Caixa")

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
    frame_right.grid_rowconfigure(0, weight=1)  # espaço acima do logo
    frame_right.grid_rowconfigure(1, weight=1)  # logo
    frame_right.grid_rowconfigure(2, weight=1)  # espaço abaixo do logo
    frame_right.grid_columnconfigure(0, weight=1)

    logo_image = ctk.CTkImage(light_image=Image.open("images/logo_loja.png"),
                              dark_image=Image.open("images/logo_loja.png"),
                              size=(400, 330))
    ctk.CTkLabel(frame_right, image=logo_image, text="").grid(row=1, column=0)

    # RODAPÉ
    frame_footer = ctk.CTkFrame(frame_right, corner_radius=0, fg_color="#E98C41", height=80)
    frame_footer.grid(row=2, column=0, sticky="ew")
    frame_footer.grid_propagate(False)

    links_frame = ctk.CTkFrame(frame_footer, fg_color="transparent")
    links_frame.pack(pady=(20,20))


    # LINKS DO RODAPÉ
    def abrir_politica():
        win = ctk.CTkToplevel(app)
        win.title("Política de Privacidade")
        ctk.CTkLabel(win, text="Política de Privacidade", font=("Arial", 20, "bold")).pack(pady=20)

    def abrir_suporte():
        win = ctk.CTkToplevel(app)
        win.title("Suporte")
        ctk.CTkLabel(win, text="Suporte", font=("Arial", 20, "bold")).pack(pady=20)

    def abrir_ajuda():
        win = ctk.CTkToplevel(app)
        win.title("Suporte")
        ctk.CTkLabel(win, text="Suporte", font=("Arial", 20, "bold")).pack(pady=20)

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
