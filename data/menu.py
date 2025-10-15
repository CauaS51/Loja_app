import customtkinter as ctk
from tkinter import messagebox
import data.colors as colors
from data.colors import *
import data.sessao as sessao
import loja
import data.caixa as caixa
import data.cadastro as cadastro

# === PERFIS ===
PROFILES = {
    "Desenvolvedor": {"Caixa": True, "Repositório": True, "Relatórios": True, "Cadastros": True},
    "Caixa": {"Caixa": True, "Repositório": False, "Relatórios": False, "Cadastros": False},
    "Reposição": {"Caixa": False, "Repositório": True, "Relatórios": False, "Cadastros": False},
    "Administração": {"Caixa": False, "Repositório": False, "Relatórios": True, "Cadastros": True}
}

# --- CARD REUTILIZÁVEL ---
class Card(ctk.CTkFrame):
    def __init__(self, master, title, color, icon_text, command=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color=color, corner_radius=15)
        self.title = title
        self.command = command
        self.is_locked = True

        # ÍCONE
        self.icon = ctk.CTkLabel(self, text=icon_text, font=("Segoe UI", 28, "bold"), text_color="#E98C41", bg_color=color)
        self.icon.grid(row=0, column=0, padx=(20,10), pady=20, sticky="w")

        # TÍTULO
        self.lbl = ctk.CTkLabel(self, text=title, font=("Segoe UI", 20, "bold"), text_color="white", bg_color=color)
        self.lbl.grid(row=0, column=1, sticky="w", padx=(0,10))

        # BIND CLIQUE
        self.bind("<Button-1>", self._on_click)
        self.icon.bind("<Button-1>", self._on_click)
        self.lbl.bind("<Button-1>", self._on_click)

        # OVERLAY DE BLOQUEIO
        self.overlay = ctk.CTkFrame(self, fg_color="#3b3b3b", corner_radius=15)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.lock_label = ctk.CTkLabel(self.overlay, text="🔒 Bloqueado", font=("Segoe UI", 14, "bold"), text_color="white")
        self.lock_label.place(relx=0.5, rely=0.5, anchor="center")

    def _on_click(self, event=None):
        if self.is_locked:
            messagebox.showwarning("Acesso negado", f"A opção '{self.title}' está bloqueada.")
        elif callable(self.command):
            self.command(self.title)

    def set_locked(self, locked=True):
        self.is_locked = locked
        if locked:
            self.overlay.lift()
            self.icon.configure(text_color="#e6e6e6")
            self.lbl.configure(text_color="#e6e6e6")
        else:
            self.overlay.lower()
            self.icon.configure(text_color="white")
            self.lbl.configure(text_color="white")

# --- FUNÇÕES AUXILIARES ---
def aplicar_permissoes(cards, profile_name):
    perms = PROFILES.get(profile_name, {})
    for key, card in cards.items():
        allowed = perms.get(key, False)
        card.set_locked(not allowed)

# --- FUNÇÕES DE ABERTURA DE MÓDULOS ---
def abrir_caixa(app):
    caixa.mostrar_menu(app)

def abrir_cadastros(app):
    cadastro.abrir_cadastro(app)

def abrir_modulo(app, module_name):
    win = ctk.CTkToplevel(app)
    win.title(module_name)
    win.geometry("600x420")
    win.transient(app)
    win.grab_set()

    ctk.CTkLabel(win, text=f"Módulo {module_name}", font=("Segoe UI", 18, "bold")).pack(pady=24)
    ctk.CTkLabel(win, text="Função em Desenvolvimento", font=("Segoe UI", 12), justify="center").pack(pady=8)
    ctk.CTkButton(win, text="Fechar", command=win.destroy).pack(side="bottom", pady=18)

# === FUNÇÃO PRINCIPAL PARA MOSTRAR O MENU ===
def mostrar_menu(app, usuario, perfil):
    for w in app.winfo_children():
        w.destroy()

    ctk.set_default_color_theme("blue")

    app.geometry("1200x700")
    app.minsize(900, 500)
    app.title("Menu Inicial")

    # Variável do perfil selecionado
    current_profile = ctk.StringVar(value=perfil)

    # === HEADER ===
    header = ctk.CTkFrame(app, fg_color=BACKGROUND_COLOR, corner_radius=15)
    header.pack(fill="x", padx=20, pady=20)

    # LOGO
    logo_frame = ctk.CTkFrame(header, fg_color=BACKGROUND_COLOR, corner_radius=0)
    logo_frame.pack(side="left")
    ctk.CTkLabel(logo_frame, text="🏬", font=("Segoe UI", 30), text_color=PRIMARY_COLOR, fg_color=BACKGROUND_COLOR).pack(side="left")
    ctk.CTkLabel(logo_frame, text="SUPERMERCADO", font=("Segoe UI", 20, "bold"), text_color=TEXT_COLOR, fg_color=BACKGROUND_COLOR).pack(side="left", padx=(8,0))

    # USUÁRIO E PERFIL
    user_frame = ctk.CTkFrame(header, fg_color=BACKGROUND_COLOR, corner_radius=0)
    user_frame.pack(side="right")
    ctk.CTkLabel(user_frame, text=usuario, font=("Segoe UI", 12), text_color=TEXT_COLOR, fg_color=BACKGROUND_COLOR).pack(side="left", padx=(0,10))
    
    profile_combo = ctk.CTkLabel(user_frame, text=perfil, font=("Segoe UI", 12, "bold"), text_color=PRIMARY_COLOR, fg_color=BACKGROUND_COLOR)
    profile_combo.pack(side="left", padx=(0,10))

    # --- LOGOUT ---
    def logout():
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            sessao.usuario = None
            sessao.perfil = None
            loja.mostrar_login(app)
    ctk.CTkButton(user_frame, text="Sair", command=logout, width=70).pack(padx=10,side="left")

    # === ÁREA PRINCIPAL ===
    container = ctk.CTkFrame(app, fg_color=BACKGROUND_COLOR, corner_radius=0)
    container.pack(expand=True, fill="both", padx=20, pady=10)

    welcome_frame = ctk.CTkFrame(container, fg_color="white", corner_radius=10)
    welcome_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # TÍTULO
    ctk.CTkLabel(welcome_frame, text=f"Bem-vindo, {usuario}!", font=("Segoe UI", 32, "bold")).pack(pady=(20,0))
    ctk.CTkLabel(welcome_frame, text="Escolha uma das opções:", font=("Segoe UI", 14)).pack(pady=(0,20))

    # === CARDS ===
    cards_frame = ctk.CTkFrame(welcome_frame, fg_color="white", corner_radius=0)
    cards_frame.pack(expand=True, fill="both", padx=20, pady=10)
    cards_frame.grid_columnconfigure((0,1), weight=1)
    cards_frame.grid_rowconfigure((0,1), weight=1)

    # Criando os cards
    card_caixa = Card(cards_frame, "Caixa", CARD_CAIXA_COLOR, "🛒", command=lambda name="Caixa": abrir_caixa(app))
    card_caixa.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    card_estoque = Card(cards_frame, "Repositório", CARD_ESTOQUE_COLOR,"📦", command=lambda name="Repositório": abrir_modulo(app, name))
    card_estoque.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    
    card_relatorios = Card(cards_frame, "Relatórios", CARD_RELATORIOS_COLOR, "📊", command=lambda name="Relatórios": abrir_modulo(app, name))
    card_relatorios.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
    
    card_cadastros = Card(cards_frame, "Cadastros", CARD_CADASTROS_COLOR, "👥", command=lambda name="Cadastros": abrir_cadastros(app))
    card_cadastros.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    cards = {
        "Caixa": card_caixa,
        "Repositório": card_estoque,
        "Relatórios": card_relatorios,
        "Cadastros": card_cadastros
    }

    # Bloqueia todos inicialmente
    for card in cards.values():
        card.set_locked(True)

    # Atualiza permissões ao selecionar perfil
    profile_combo.bind("<<ComboboxSelected>>", lambda e: aplicar_permissoes(cards, current_profile.get()))

    # Aplica permissões iniciais
    aplicar_permissoes(cards, current_profile.get())