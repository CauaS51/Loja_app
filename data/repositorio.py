# === data/repositorio.py ===
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import data.colors as colors
from crud import crud_produtos

# === CLASSE PRINCIPAL DO REPOSITÓRIO ===
class Repositorio:
    def __init__(self, app):
        self.app = app
        # Categorias iniciais
        self.categorias = [
            {"nome": "Hortifruti", "img": "🥦"},
            {"nome": "Açougue", "img": "🥩"},
            {"nome": "Eletrônicos", "img": "📱"},
            {"nome": "Padaria", "img": "🥖"},
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
                ctk.CTkLabel(card, text=cat["img"], font=ctk.CTkFont(size=30)).place(relx=0.05, rely=0.5, anchor="w")

            ctk.CTkLabel(card, text=cat["nome"], font=ctk.CTkFont(size=18, weight="bold"),
                         text_color=cores["TEXT_PRIMARY"]).place(relx=0.25, rely=0.5, anchor="w")

            ctk.CTkButton(
                card, text="🔍 Ver Produtos",
                fg_color=cores["PRIMARY"], hover_color=cores["HOVER"], text_color="white",
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda nome=cat["nome"]: self.abrir_categoria(nome)
            ).place(relx=0.9, rely=0.5, anchor="e")

        # === BOTÃO PARA ADICIONAR NOVA CATEGORIA ===
        ctk.CTkButton(main_frame, text="➕ Nova Categoria",
                      fg_color=cores["PRIMARY"], hover_color=cores["HOVER"],
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self.nova_categoria).pack(pady=10)

    # === ADICIONAR NOVA CATEGORIA ===
    def nova_categoria(self):
        def salvar_categoria():
            nome = entry_nome.get().strip()
            emoji = entry_emoji.get().strip() or "📦"
            if nome:
                self.categorias.append({"nome": nome, "img": emoji})
                popup.destroy()
                self.carregar_imagens()
                self.abrir_repositorio()
            else:
                messagebox.showerror("Erro", "Nome da categoria é obrigatório.")

        popup = ctk.CTkToplevel(self.app)
        popup.title("Nova Categoria")
        popup.geometry("300x200")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text="Nome da Categoria:").pack(pady=10)
        entry_nome = ctk.CTkEntry(popup, width=200)
        entry_nome.pack(pady=5)
        ctk.CTkLabel(popup, text="Emoji/Icone (opcional):").pack(pady=10)
        entry_emoji = ctk.CTkEntry(popup, width=100)
        entry_emoji.pack(pady=5)
        ctk.CTkButton(popup, text="Salvar", command=salvar_categoria).pack(pady=15)

    # === ABRIR CATEGORIA ===
    def abrir_categoria(self, categoria_nome):
        CategoriaProdutos(self.app, categoria_nome)

    # === VOLTAR MENU ===
    def voltar_menu(self):
        from data import menu
        from data import sessao
        menu.mostrar_menu(self.app, usuario=sessao.usuario, perfil=sessao.perfil)


# === CLASSE DE PRODUTOS DE UMA CATEGORIA ===
class CategoriaProdutos:
    def __init__(self, app, categoria_nome):
        self.app = app
        self.categoria_nome = categoria_nome
        self.produtos = crud_produtos.listar_produtos()
        self.imagens_cache = {}
        self.carregar_imagens()
        self.abrir_tela()

    def carregar_imagens(self):
        for prod in self.produtos:
            img_path = getattr(prod, "img", None)
            if img_path and os.path.isfile(img_path):
                try:
                    self.imagens_cache[prod["codigo"]] = ctk.CTkImage(
                        light_image=Image.open(img_path), size=(80, 80)
                    )
                except:
                    self.imagens_cache[prod["codigo"]] = None
            else:
                self.imagens_cache[prod["codigo"]] = None

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

        # === BOTÃO ADICIONAR PRODUTO ===
        ctk.CTkButton(main_frame, text="➕ Adicionar Produto",
                      fg_color=cores["PRIMARY"], hover_color=cores["HOVER"],
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self.novo_produto).pack(pady=10)

        # === LISTA DE PRODUTOS ===
        scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color=cores["BACKGROUND"])
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        num_colunas = 2
        produtos_filtrados = [p for p in self.produtos if p.get("categoria") == self.categoria_nome]

        for index, prod in enumerate(produtos_filtrados):
            row = index // num_colunas
            col = index % num_colunas

            card = ctk.CTkFrame(scroll_frame, fg_color=cores["CARD_BG"], corner_radius=12, height=150)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            scroll_frame.grid_columnconfigure(col, weight=1)

            img = self.imagens_cache.get(prod["codigo"])
            if img:
                ctk.CTkLabel(card, image=img, text="").place(relx=0.05, rely=0.5, anchor="w")
            else:
                ctk.CTkLabel(card, text="📦", font=ctk.CTkFont(size=30)).place(relx=0.05, rely=0.5, anchor="w")

            ctk.CTkLabel(card, text=prod["nome"], font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=cores["TEXT_PRIMARY"]).place(relx=0.25, rely=0.25, anchor="w")
            ctk.CTkLabel(card, text=f"R$ {prod['preco']:.2f}", font=ctk.CTkFont(size=14),
                         text_color=cores["TEXT_SECONDARY"]).place(relx=0.25, rely=0.55, anchor="w")

    # === ADICIONAR NOVO PRODUTO ===
    def novo_produto(self):
        def escolher_imagem():
            path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
            entry_img.delete(0, ctk.END)
            entry_img.insert(0, path)

        def salvar_produto():
            nome = entry_nome.get().strip()
            preco = entry_preco.get().strip()
            img = entry_img.get().strip()
            if not nome or not preco:
                messagebox.showerror("Erro", "Nome e preço são obrigatórios.")
                return
            try:
                preco_valor = float(preco)
            except:
                messagebox.showerror("Erro", "Preço inválido.")
                return

            # Salvar no banco
            crud_produtos.cadastrar_produto(nome, preco_valor, img)
            popup.destroy()
            self.produtos = crud_produtos.listar_produtos()
            self.carregar_imagens()
            self.abrir_tela()

        popup = ctk.CTkToplevel(self.app)
        popup.title("Novo Produto")
        popup.geometry("350x300")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text="Nome do Produto:").pack(pady=5)
        entry_nome = ctk.CTkEntry(popup, width=250)
        entry_nome.pack(pady=5)

        ctk.CTkLabel(popup, text="Preço:").pack(pady=5)
        entry_preco = ctk.CTkEntry(popup, width=150)
        entry_preco.pack(pady=5)

        ctk.CTkLabel(popup, text="Imagem (opcional):").pack(pady=5)
        entry_img = ctk.CTkEntry(popup, width=250)
        entry_img.pack(pady=5)
        ctk.CTkButton(popup, text="Escolher arquivo", command=escolher_imagem).pack(pady=5)

        ctk.CTkButton(popup, text="Salvar", command=salvar_produto).pack(pady=15)

    # === VOLTAR PARA REPOSITÓRIO ===
    def voltar(self):
        Repositorio(self.app)


# === FUNÇÃO DE ACESSO PELO MENU ===
def abrir_repositorio(app):
    Repositorio(app)
