import sys
sys.dont_write_bytecode = True #ignorar pycache

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import data.colors as colors
from data.colors import *
from data import loja
import data.cadastro as cadastro
import data.sessao as sessao
import os
import shutil

# === MODO CLARO PADRÃO ===
ctk.set_appearance_mode("light")

# === CONFIGURAÇÃO INICIAL ===
def mostrar_login(app):
    for w in app.winfo_children():
        w.destroy()
    
    ctk.set_default_color_theme("blue")
    
    screen_w = app.winfo_screenwidth()
    escala = screen_w / 1600 
    
    app.title("Custom-PDV") 
    app.geometry(f"{int(screen_w*0.7)}x{int(app.winfo_screenheight()*0.7)}")
    app.minsize(800, 600)
    app.grid_rowconfigure(0, weight=1)
    
    app.grid_columnconfigure(0, weight=1, uniform="group1")  
    app.grid_columnconfigure(1, weight=1, uniform="group1")  

    cores = get_colors()

    # === FRAME ESQUERDA ===
    frame_left = ctk.CTkFrame(app, corner_radius=0, fg_color=cores["BACKGROUND"])
    frame_left.grid(row=0, column=0, sticky="nsew")
    frame_left.grid_rowconfigure(0, weight=1)
    frame_left.grid_rowconfigure(1, weight=2)
    frame_left.grid_rowconfigure(2, weight=1)
    frame_left.grid_columnconfigure(0, weight=1)

    login_container = ctk.CTkFrame(frame_left, fg_color="transparent")
    login_container.place(relx=0.5, rely=0.5, anchor="center")

    # TÍTULOS COM FONTE ESCALÁVEL
    ctk.CTkLabel(login_container, text="🏬 CUSTOM PDV", font=("Comfortaa", int(40 * escala), "bold"),
                 text_color=cores["TEXT_PRIMARY"]).pack(pady=(int(30*escala), int(30*escala)))
    
    ctk.CTkLabel(login_container, text="BEM VINDO!", font=("Comfortaa", int(40 * escala), "bold"),
                 text_color=cores["TEXT_PRIMARY"]).pack(pady=(0,10), padx=(0, int(60*escala)))
    
    ctk.CTkLabel(login_container, text="Gerencie sua loja de forma prática e rápida",
                 font=("Arial", int(16 * escala), "bold"), text_color=cores["TEXT_PRIMARY"]).pack(pady=(0,20), padx=(30,0))

    # CAMPOS ESCALÁVEIS
    entry_w = int(300 * escala)
    entry_h = int(45 * escala)
    
    entry_user = ctk.CTkEntry(login_container, placeholder_text="👤 Usuário", font=("Arial", int(14*escala), "bold"),
                              placeholder_text_color=cores["TEXT_PRIMARY"], width=entry_w, height=entry_h, corner_radius=10)
    entry_user.pack(pady=8)
    
    # CONTAINER DA SENHA PARA O OLHINHO
    pass_container = ctk.CTkFrame(login_container, fg_color="transparent")
    pass_container.pack(pady=8)

    entry_pass = ctk.CTkEntry(pass_container, placeholder_text="🔒 Senha", font=("Arial", int(14*escala), "bold"),
                              placeholder_text_color=cores["TEXT_PRIMARY"], show="*", width=entry_w, height=entry_h, corner_radius=10)
    entry_pass.pack()

    # FUNÇÃO PARA ALTERNAR VISIBILIDADE
    img_eye = ctk.CTkImage(
    light_image=Image.open("assets/icons/eye_off.png"),
    dark_image=Image.open("assets/icons/eye_off_dark.png"),
    size=(20, 20)
    )

    img_eye_off = ctk.CTkImage(
        light_image=Image.open("assets/icons/eye.png"),
        dark_image=Image.open("assets/icons/eye_dark.png"),
        size=(20, 20)
    )

    def alternar_senha():
        if entry_pass.cget("show") == "*":
            entry_pass.configure(show="")
            btn_olho.configure(image=img_eye)
        else:
            entry_pass.configure(show="*")
            btn_olho.configure(image=img_eye_off)

    btn_olho = ctk.CTkButton(
    pass_container,
    image=img_eye_off,
    text="",
    width=30,
    height=30,
    fg_color="transparent",
    hover_color=cores["HOVER"],
    command=alternar_senha
)
    
    btn_olho.place(relx=1.0, rely=0.5, x=-10, anchor="e")

    def esqueci_senha():
        print("A opção 'Esqueci minha senha' foi clicada!")
    
    ctk.CTkButton(login_container, text="Esqueceu sua senha?", fg_color="transparent",
                  hover_color=cores["HOVER"], font=("Segoe UI", int(13*escala), "bold"),
                  text_color=cores["TEXT_PRIMARY"], command=esqueci_senha).pack(pady=(5,15), padx=(0, int(175*escala)))

    # FUNÇÃO LOGIN
    from data.conexao import conectar
    from data.hash import verificar_senha
    def on_login(event=None):
        login_input = entry_user.get().strip().lower()
        pwd_input  = entry_pass.get().strip()

        if not login_input or not pwd_input:
            messagebox.showwarning("Atenção", "Informe usuário e senha.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT ID_Conta, Nome, Login, Senha FROM Contas WHERE Login = %s"
            cursor.execute(query, (login_input,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and verificar_senha(pwd_input, user["Senha"]):
                sessao.usuario_id = user["ID_Conta"]
                sessao.nome = user["Nome"]
                sessao.usuario = user["Login"]
                messagebox.showinfo("Sucesso", f"Bem-vindo, {sessao.nome}!")
                for w in app.winfo_children(): w.destroy()
                loja.mostrar_lojas(app)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        except Exception as e:
            messagebox.showerror("Erro", "Não foi possível conectar ao servidor.")

    # BOTÕES ESCALÁVEIS
    ctk.CTkButton(login_container, text="Entrar", font=("Arial", int(15*escala), "bold"),
                  width=entry_w, height=entry_h, corner_radius=10,
                  fg_color=cores["PRIMARY"], hover_color=cores["HOVER"], command=on_login).pack(pady=8)
    app.bind('<Return>', on_login)

    def abrir_cadastro():
        cadastro.abrir_cadastro(app)
    
    ctk.CTkButton(login_container, text="Cadastre-se", font=("Arial", int(15*escala), "bold"),
                  width=entry_w, height=entry_h, corner_radius=10,
                  fg_color="transparent", hover_color=cores["HOVER"],
                  border_width=2, border_color=cores["PRIMARY"], text_color=cores["PRIMARY"],
                  command=abrir_cadastro).pack(pady=8)

    # === FRAME DIREITA ===
    frame_right = ctk.CTkFrame(app, corner_radius=0, fg_color=cores["PRIMARY"])
    frame_right.grid(row=0, column=1, sticky="nsew")
    frame_right.grid_columnconfigure(0, weight=1)

    def alternar_tema():
        app.focus_force()
        colors.alternar_tema()
        mostrar_login(app)

    icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
    theme_button = ctk.CTkButton(frame_right, text=icone_tema, width=30, height=40, corner_radius=12, 
                                 fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"], 
                                 text_color=cores["TEXT_PRIMARY"], font=ctk.CTkFont(size=int(25*escala)), command=alternar_tema)
    theme_button.place(relx=0.95, rely=0.05, anchor="ne")

    # LOGO ESCALÁVEL
    logo_size = int(400 * escala)
    img_path = "assets/logo_loja_dark.png" if ctk.get_appearance_mode() == "Dark" else "assets/logo_loja.png"
    logo_image = ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=(logo_size, int(logo_size * 0.95)))
    
    logo_label = ctk.CTkLabel(frame_right, image=logo_image, text="")
    logo_label.place(relx=0.5, rely=0.5, anchor="center")

    # RODAPÉ ESCALÁVEL
    frame_footer = ctk.CTkFrame(frame_right, corner_radius=0, fg_color=cores["PRIMARY"], height=int(100*escala))
    frame_footer.place(relx=0.5, rely=0.9, anchor="center", relwidth=1)

    links_frame = ctk.CTkFrame(frame_footer, fg_color="transparent")
    links_frame.pack(pady=(10,10))

    def abrir_info_auxiliar(app, titulo, texto_h1):
        win = ctk.CTkToplevel(app)
        win.title(titulo)
        win.geometry(f"900x600")
        win.transient(app)
        win.grab_set()
        ctk.CTkLabel(win, text=texto_h1, font=("Arial", 20, "bold")).pack(pady=20)

    links = [("Políticas", "Políticas de Privacidade"), ("Suporte", "Central de Suporte"), ("Ajuda", "Central de Ajuda")]

    for i, (text, info) in enumerate(links):
        btn = ctk.CTkButton(links_frame, text=text, font=("Arial", int(13*escala), "bold"), width=0, height=0,
                            fg_color="transparent", hover_color=cores["HOVER"], text_color="#FFFFFF",
                            command=lambda t=text, inf=info: abrir_info_auxiliar(app, t, inf))
        btn.pack(side="left", padx=5)
        if i < len(links) - 1:
            ctk.CTkLabel(links_frame, text="|", text_color="#FFFFFF", font=("Arial", int(12*escala))).pack(side="left", padx=1)

    ctk.CTkLabel(frame_footer, text=f"📞 (91)98765-4321   🌐 www.custompdv.com",
                 text_color="#FFFFFF", font=("Arial", int(14*escala), "bold")).pack(pady=(0,10))

def excluir_tema_cache(app):
    import data.colors as colors
    colors.resetar_tema()
    if os.path.exists("cache_temas"): shutil.rmtree("cache_temas")
    app.destroy()

if __name__ == "__main__":
    app = ctk.CTk()
    app.after(0, lambda: app.state('zoomed'))
    app.protocol("WM_DELETE_WINDOW", lambda: excluir_tema_cache(app))
    mostrar_login(app)
    app.mainloop()