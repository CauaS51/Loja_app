import customtkinter as ctk
from tkinter import messagebox
import data.colors as colors
from data.colors import get_colors
import data.caixa as caixa
import data.repositorio as repositorio
import data.relatorios as relatorios
import data.cadastro as cadastro
import data.sessao as sessao
from PIL import Image, ImageOps
import os
import io  # Adicionado para processar os bytes da imagem
from crud.crud_lojas import buscar_dados_visuais
import json

# === PERFIS: DEFINIÇÃO DE PERMISSÕES ===
PROFILES = {
    "Administrador": {"Caixa": True, "Repositório": True, "Relatórios": True, "Cadastros": True},
    "Caixa": {"Caixa": True, "Repositório": False, "Relatórios": False, "Cadastros": False},
    "Repositor": {"Caixa": False, "Repositório": True, "Relatórios": False, "Cadastros": False},
    "Gestor de Dados": {"Caixa": False, "Repositório": False, "Relatórios": True, "Cadastros": True}
}

# ==== CARD ====
class Card(ctk.CTkFrame):
    def __init__(self, master, title, color, icon_text, command=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.base_color = color
        self.hover_color = self._lighter_color(color, 0.1)
        self.configure(fg_color=self.base_color, corner_radius=15)
        self.title = title
        self.command = command
        self.is_locked = True

        self.icon = ctk.CTkLabel(self, text=icon_text, font=("Segoe UI", 28, "bold"), text_color="white", bg_color=color)
        self.icon.grid(row=0, column=0, padx=(20,10), pady=20, sticky="w")

        self.lbl = ctk.CTkLabel(self, text=title, font=("Segoe UI", 20, "bold"), text_color="white", bg_color=color)
        self.lbl.grid(row=0, column=1, sticky="w", padx=(0,10))

        for widget in [self, self.icon, self.lbl]:
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self._on_hover)
            widget.bind("<Leave>", self._on_leave)

        self.overlay = ctk.CTkFrame(self, fg_color="#3b3b3b", corner_radius=15)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.lock_label = ctk.CTkLabel(self.overlay, text="🔒 Bloqueado", font=("Segoe UI", 14, "bold"), text_color="white")
        self.lock_label.place(relx=0.5, rely=0.5, anchor="center")

    def _on_click(self, event=None):
        if self.is_locked:
            messagebox.showwarning("Acesso negado", f"A opção '{self.title}' está bloqueada.")
        elif callable(self.command):
            self.command(self.title)

    def _on_hover(self, event=None):
        if not self.is_locked:
            self.configure(fg_color=self.hover_color)
            self.icon.configure(bg_color=self.hover_color)
            self.lbl.configure(bg_color=self.hover_color)

    def _on_leave(self, event=None):
        self.configure(fg_color=self.base_color)
        self.icon.configure(bg_color=self.base_color)
        self.lbl.configure(bg_color=self.base_color)

    def set_locked(self, locked=True):
        self.is_locked = locked
        self.overlay.lift() if locked else self.overlay.lower()

    def _lighter_color(self, hex_color, factor=0.1):
        hex_color = hex_color.lstrip("#")
        rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        rgb = [min(int(c + (255 - c) * factor), 255) for c in rgb]
        return "#%02x%02x%02x" % tuple(rgb)
    
# ==== AUX ====
def aplicar_permissoes(cards, profile_name):
    perms = PROFILES.get(profile_name, {})
    for key, card in cards.items():
        card.set_locked(not perms.get(key, False))

def abrir_caixa(app): caixa.mostrar_menu(app)
def abrir_cadastros(app): cadastro.listar_funcionarios(app)
def mostrar_relatorios(app): relatorios.mostrar_relatorios(app)
def abrir_repositorio(app): repositorio.abrir_repositorio(app)

def mostrar_menu(app, usuario, perfil, cores_atualizadas=None):
    app.update_idletasks()
    app.update()
    for w in app.winfo_children():
        w.destroy()
    app.after(10, lambda: _construir_menu(app, usuario, perfil, cores_atualizadas))

def _construir_menu(app, usuario, perfil, cores_atualizadas=None):
    app.title("Menu Inicial")

    # ===== TEMA DA LOJA =====
    tema_loja = getattr(sessao, 'tema_loja', None)
    if not tema_loja and getattr(sessao, 'loja_id', None):
        dados_visuais = buscar_dados_visuais(sessao.loja_id)
        if dados_visuais:
            tema_json = dados_visuais.get("Tema_JSON")
            if tema_json:
                colors.aplicar_tema_customizado(tema_json)
                try:
                    sessao.tema_loja = json.loads(tema_json)
                except:
                    sessao.tema_loja = None
            sessao.logo_path = dados_visuais.get("img") # Contém os BYTES do banco
            sessao.nome_loja = dados_visuais.get("nome", "SUPERMERCADO")

    cores = cores_atualizadas or get_colors()
    nome_loja_atual = getattr(sessao, 'nome_loja', "SUPERMERCADO")

    # ===== HEADER =====
    header = ctk.CTkFrame(app, fg_color=cores["BACKGROUND_2"], corner_radius=15)
    header.pack(fill="x", padx=20, pady=20)

    def alternar_tema():
        colors.alternar_tema()
        mostrar_menu(app, usuario, perfil)

    icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
    ctk.CTkButton(header, text=icone_tema, width=40, height=40, corner_radius=12,
                  fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
                  text_color=cores["TEXT_PRIMARY"], font=("Segoe UI", 20),
                  command=alternar_tema).pack(side="left", padx=10)

    logo_frame = ctk.CTkFrame(header, fg_color=cores["BACKGROUND_2"], corner_radius=5)
    logo_frame.pack(side="left", padx=20)

    # --- LÓGICA DE CARREGAMENTO DA LOGO (BYTES) ---
    img_data = getattr(sessao, 'logo_path', None)
    logo_exibida = False

    if img_data:
        try:
            # Se forem bytes, usamos io.BytesIO. Se for string (caminho), usamos direto.
            if isinstance(img_data, bytes):
                img_pil = Image.open(io.BytesIO(img_data))
            elif isinstance(img_data, str) and os.path.exists(img_data):
                img_pil = Image.open(img_data)
            else:
                raise ValueError("Formato não suportado")

            img_fit = ImageOps.fit(img_pil, (60, 60), Image.Resampling.LANCZOS)
            logo_img = ctk.CTkImage(light_image=img_fit, dark_image=img_fit, size=(60, 60))
            ctk.CTkLabel(logo_frame, image=logo_img, text="").pack(side="left", padx=5)
            logo_exibida = True
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")

    # Fallback se a imagem não carregar
    if not logo_exibida:
        ctk.CTkLabel(logo_frame, text="🏬", font=("Segoe UI", 40)).pack(side="left", padx=5)

    ctk.CTkLabel(logo_frame, text=nome_loja_atual.upper(), font=("Segoe UI", 18, "bold"),
                 text_color=cores["TEXT_PRIMARY"]).pack(side="left", padx=10)

    # USER INFO
    user_frame = ctk.CTkFrame(header, fg_color="transparent")
    user_frame.pack(side="right", padx=30)

    ctk.CTkLabel(user_frame, text=usuario, font=("Segoe UI", 14),
                 text_color=cores["TEXT_PRIMARY"]).pack(side="left", padx=(0, 10))
    ctk.CTkLabel(user_frame, text=perfil, font=("Segoe UI", 14, "bold"),
                 text_color=cores["SECONDARY"]).pack(side="left", padx=(0, 20))

    def fechar_loja():
        sessao.funcionario_id = None
        sessao.perfil = None
        sessao.loja_id = None
        sessao.nome_loja = None
        sessao.logo_path = None
        sessao.tema_loja = None
        colors.resetar_tema()
        from data.loja import mostrar_lojas
        mostrar_lojas(app)

    ctk.CTkButton(user_frame, text="Fechar Loja", command=fechar_loja, width=60,
                  fg_color="#E74C3C", hover_color="#C0392B").pack(side="left")

    # CONTEÚDO 
    container = ctk.CTkFrame(app, fg_color=cores["BACKGROUND"], corner_radius=10)
    container.pack(expand=True, fill="both", padx=20, pady=10)

    welcome_msg_frame = ctk.CTkFrame(container, fg_color="transparent")
    welcome_msg_frame.pack(pady=(40, 20))

    ctk.CTkLabel(welcome_msg_frame, text="Bem-Vindo, ",
                 font=("Segoe UI", 22), text_color=cores["TEXT_PRIMARY"]).pack(side="left")
    ctk.CTkLabel(welcome_msg_frame, text=usuario,
                 font=("Segoe UI", 22, "bold"), text_color=cores["PRIMARY"]).pack(side="left")

    cards_grid = ctk.CTkFrame(container, fg_color="transparent")
    cards_grid.pack(expand=True, fill="both", padx=50, pady=20)
    cards_grid.grid_columnconfigure((0,1), weight=1)
    cards_grid.grid_rowconfigure((0,1), weight=1)

    cards = {
        "Caixa": Card(cards_grid, "Caixa", cores["CARD_CAIXA"], "🛒", command=lambda _: abrir_caixa(app)),
        "Repositório": Card(cards_grid, "Repositório", cores["CARD_ESTOQUE"], "📦", command=lambda _: abrir_repositorio(app)),
        "Relatórios": Card(cards_grid, "Relatórios", cores["CARD_RELATORIOS"], "📊", command=lambda _: mostrar_relatorios(app)),
        "Cadastros": Card(cards_grid, "Cadastros", cores["CARD_CADASTROS"], "👥", command=lambda _: abrir_cadastros(app))
    }

    cards["Caixa"].grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
    cards["Repositório"].grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
    cards["Relatórios"].grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
    cards["Cadastros"].grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

    aplicar_permissoes(cards, perfil)
    app.update_idletasks()