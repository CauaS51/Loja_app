# === data/repositorio.py ===
import customtkinter as ctk
from PIL import Image
import data.colors as colors
from data.colors import *
import data.sessao as sessao

# === CLASSE PRINCIPAL DO REPOSITÓRIO ===
class Repositorio:
    def __init__(self, app):
        self.app = app
        self.categorias = [
            {"nome": "Hortifruti", "img": "🥦"},
            {"nome": "Açougue", "img": "🥩"},
            {"nome": "Peixaria", "img": "🐟"},
            {"nome": "Padaria", "img": "🥖"},
            {"nome": "Laticínios", "img": "🥛"},
            {"nome": "Mercearia", "img": "🍚"},
            {"nome": "Temperos", "img": "🧂"},
            {"nome": "Bebidas", "img": "🥤"},
            {"nome": "Biscoitos & Snacks", "img": "🍪"},
            {"nome": "Doces & Chocolates", "img": "🍫"},
            {"nome": "Congelados", "img": "🧊"},
            {"nome": "Limpeza", "img": "🧼"},
            {"nome": "Higiene Pessoal", "img": "🧴"},
            {"nome": "Bebês", "img": "👶"},
            {"nome": "Pet Shop", "img": "🐶"},
            {"nome": "Utilidades Domésticas", "img": "📦"},
        ]
        self.imagens_cache = {}
        self.carregar_imagens()
        self.abrir_repositorio()

    # === CARREGAR IMAGENS ===
    def carregar_imagens(self):
        for cat in self.categorias:
            img = cat["img"]
            if isinstance(img, str) and img.endswith((".png", ".jpg", ".jpeg")):
                try:
                    self.imagens_cache[cat["nome"]] = ctk.CTkImage(
                        light_image=Image.open(img),
                        size=(80, 80)
                    )
                except:
                    self.imagens_cache[cat["nome"]] = None
            else:
                # emoji ou texto
                self.imagens_cache[cat["nome"]] = None

    # === ABRIR TELA PRINCIPAL ===
    def abrir_repositorio(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Repositório")
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40,
            font=ctk.CTkFont(size=20), corner_radius=12,
            text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.voltar_menu
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        title_label = ctk.CTkLabel(
            header, text="📦 Repositório",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=1, padx=(0,30), pady=20, sticky="w")

        def alternar_tema():
            colors.alternar_tema()
            self.abrir_repositorio()

        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        theme_button = ctk.CTkButton(
            header, text=icone_tema, width=40, height=40,
            corner_radius=12, fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"], font=ctk.CTkFont(size=25),
            command=alternar_tema
        )
        theme_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # === CONTEÚDO PRINCIPAL ===
        main_frame = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color=cores["BACKGROUND"])
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        num_colunas = 2
        for index, cat in enumerate(self.categorias):
            row = index // num_colunas
            col = index % num_colunas

            card = ctk.CTkFrame(scroll_frame, fg_color=cores["CARD_BG"], corner_radius=12, height=120)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            scroll_frame.grid_columnconfigure(col, weight=1)

            img = self.imagens_cache.get(cat["nome"])
            if img:
                ctk.CTkLabel(card, image=img, text="").place(relx=0.05, rely=0.5, anchor="w")
            else:
                # Se for emoji, exibe o próprio emoji
                ctk.CTkLabel(card, text=cat["img"], font=ctk.CTkFont(size=30)).place(relx=0.05, rely=0.5, anchor="w")

            ctk.CTkLabel(card, text=cat["nome"], font=ctk.CTkFont(size=18, weight="bold"),
                         text_color=cores["TEXT_PRIMARY"]).place(relx=0.25, rely=0.5, anchor="w")

            ctk.CTkButton(
                card, text="🔍 Ver Produtos",
                fg_color=cores["PRIMARY"], hover_color=cores["HOVER"], text_color="white",
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda nome=cat["nome"]: self.abrir_categoria(nome)
            ).place(relx=0.9, rely=0.5, anchor="e")

    # === ABRIR CATEGORIA ===
    def abrir_categoria(self, categoria_nome):
        CategoriaProdutos(self.app, categoria_nome)

    # === VOLTAR MENU ===
    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app, usuario=sessao.usuario, perfil=sessao.perfil)

# === CLASSE DE PRODUTOS DE UMA CATEGORIA ===
class CategoriaProdutos:
    def __init__(self, app, categoria_nome):
        self.app = app
        self.categoria_nome = categoria_nome
        # self.produtos = Produto.listar_produtos_por_categoria(categoria_nome)
        self.imagens_cache = {}
        self.carregar_imagens()
        self.abrir_tela()

    def carregar_imagens(self):
        # Se você tiver arquivos de imagens dos produtos, carregue aqui
        for prod in getattr(self, "produtos", []):
            try:
                self.imagens_cache[prod.id] = ctk.CTkImage(
                    light_image=Image.open(prod.imagem),
                    size=(80, 80)
                )
            except:
                self.imagens_cache[prod.id] = None

    def abrir_tela(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title(f"{self.categoria_nome}")
        cores = colors.get_colors()

        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)

        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40,
            font=ctk.CTkFont(size=20), corner_radius=12,
            text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.voltar
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        title_label = ctk.CTkLabel(
            header, text=f"📦 {self.categoria_nome}",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=1, padx=(0,30), pady=20, sticky="w")

        main_frame = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color=cores["BACKGROUND"])
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        num_colunas = 2
        for index, prod in enumerate(getattr(self, "produtos", [])):
            row = index // num_colunas
            col = index % num_colunas

            card = ctk.CTkFrame(scroll_frame, fg_color=cores["CARD_BG"], corner_radius=12, height=150)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            scroll_frame.grid_columnconfigure(col, weight=1)

            img = self.imagens_cache.get(prod.id)
            if img:
                ctk.CTkLabel(card, image=img, text="").place(relx=0.05, rely=0.5, anchor="w")
            else:
                ctk.CTkLabel(card, text="📦", font=ctk.CTkFont(size=30)).place(relx=0.05, rely=0.5, anchor="w")

            ctk.CTkLabel(card, text=prod.nome, font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=cores["TEXT_PRIMARY"]).place(relx=0.25, rely=0.25, anchor="w")
            ctk.CTkLabel(card, text=f"R$ {prod.preco:.2f}", font=ctk.CTkFont(size=14),
                         text_color=cores["TEXT_SECONDARY"]).place(relx=0.25, rely=0.55, anchor="w")

    def voltar(self):
        Repositorio(self.app)

# === FUNÇÃO DE ACESSO PELO MENU ===
def abrir_repositorio(app):
    Repositorio(app)
