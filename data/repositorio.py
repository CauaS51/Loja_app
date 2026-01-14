# === data/repositorio.py ===
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import data.colors as colors
from crud import crud_produtos
from crud import crud_categorias  # módulo para categorias


class Repositorio:
    def __init__(self, app):
        self.app = app
        self.produtos = crud_produtos.listar_produtos()
        self.categorias = ["Sem Categoria"] + crud_categorias.listar_categorias()
        self.imagens_cache = {}
        self.produto_editando = None  # Guarda produto que está sendo editado
        self.carregar_imagens()
        self.abrir_repositorio()

    def carregar_imagens(self):
        for prod in self.produtos:
            img_path = prod.get("img")
            if img_path and os.path.isfile(img_path):
                try:
                    self.imagens_cache[prod["codigo"]] = ctk.CTkImage(
                        light_image=Image.open(img_path), size=(100, 100)
                    )
                except:
                    self.imagens_cache[prod["codigo"]] = None
            else:
                self.imagens_cache[prod["codigo"]] = None

    def abrir_repositorio(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Repositório")
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x", pady=(0,5))
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        # BOTÃO VOLTAR
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.voltar_menu
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # TÍTULO
        title_label = ctk.CTkLabel(
            header, text="📦 Repositório de Produtos",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=1, padx=(0,30), pady=20, sticky="w")

        # BOTÃO ALTERNAR TEMA
        def alternar_tema():
            colors.alternar_tema()
            self.abrir_repositorio()

        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        theme_button = ctk.CTkButton(
            header,
            text=icone_tema,
            width=40,
            height=40,
            corner_radius=12,
            fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"],
            font=ctk.CTkFont(size=25),
            command=alternar_tema
        )
        theme_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # === FRAME PRINCIPAL ===
        main_frame = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # === FRAME DE CADASTRO DE PRODUTO ===
        cadastro_frame = ctk.CTkFrame(main_frame, fg_color=cores["CARD_BG"], corner_radius=12, height=200)
        cadastro_frame.pack(fill="x", padx=10, pady=(10, 5))

        # Imagem do produto
        self.img_preview = ctk.CTkLabel(cadastro_frame, text="📦", font=ctk.CTkFont(size=70))
        self.img_preview.grid(row=0, column=0, rowspan=4, padx=20, pady=10)

        def escolher_imagem():
            path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
            if path:
                self.img_path = path
                try:
                    img = ctk.CTkImage(light_image=Image.open(path), size=(120, 120))
                    self.img_preview.configure(image=img, text="")
                    self.img_preview.image = img
                except:
                    self.img_preview.configure(text="📦", image=None)

        ctk.CTkButton(cadastro_frame, text="Escolher Imagem", command=escolher_imagem).grid(row=4, column=0, pady=5)

        # Nome e Preço
        ctk.CTkLabel(cadastro_frame, text="Nome:").grid(row=0, column=1, sticky="w")
        self.entry_nome = ctk.CTkEntry(cadastro_frame, width=250)
        self.entry_nome.grid(row=0, column=2, pady=5, padx=5)

        ctk.CTkLabel(cadastro_frame, text="Preço:").grid(row=1, column=1, sticky="w")
        self.entry_preco = ctk.CTkEntry(cadastro_frame, width=100)
        self.entry_preco.grid(row=1, column=2, pady=5, padx=5, sticky="w")

        ctk.CTkLabel(cadastro_frame, text="Categoria:").grid(row=2, column=1, sticky="w")
        self.combo_categoria_produto = ctk.CTkComboBox(cadastro_frame, values=self.categorias)
        self.combo_categoria_produto.set("Sem Categoria")
        self.combo_categoria_produto.grid(row=2, column=2, pady=5, padx=5, sticky="w")

        # === FUNÇÃO SALVAR OU ATUALIZAR PRODUTO ===
        def salvar_produto():
            nome = self.entry_nome.get().strip()
            preco = self.entry_preco.get().strip()
            categoria = self.combo_categoria_produto.get()
            img = getattr(self, "img_path", "")

            if not nome or not preco:
                messagebox.showerror("Erro", "Nome e preço são obrigatórios.")
                return
            try:
                preco_valor = float(preco)
            except:
                messagebox.showerror("Erro", "Preço inválido.")
                return

            if self.produto_editando:
                # Atualizar produto existente
                crud_produtos.atualizar_produto(
                    self.produto_editando["codigo"], nome, preco_valor, img, categoria
                )
                messagebox.showinfo("Sucesso", f"Produto '{nome}' atualizado!")
                self.produto_editando = None
            else:
                # Criar novo produto
                crud_produtos.cadastrar_produto(nome, preco_valor, img, categoria)
                messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado!")

            # Limpar campos
            self.entry_nome.delete(0, "end")
            self.entry_preco.delete(0, "end")
            self.img_preview.configure(image=None, text="📦")
            self.img_path = ""
            self.combo_categoria_produto.set("Sem Categoria")

            self.produtos = crud_produtos.listar_produtos()
            self.categorias = ["Sem Categoria"] + crud_categorias.listar_categorias()
            self.carregar_imagens()
            self.abrir_repositorio()

        ctk.CTkButton(cadastro_frame, text="💾 Salvar Produto", fg_color=cores["PRIMARY"],
                      command=salvar_produto).grid(row=4, column=1, pady=10)

        # BOTÃO NOVA CATEGORIA AO LADO DIREITO DE SALVAR PRODUTO
        def abrir_categorias():
            Categorias(self.app, repositorio=self)

        ctk.CTkButton(cadastro_frame, text="🗂 Nova Categoria", fg_color=cores["PRIMARY"],
                      command=abrir_categorias).grid(row=4, column=2, pady=10)

        # === FILTRO E PESQUISA ===
        filtro_frame = ctk.CTkFrame(main_frame, fg_color=cores["CARD_BG"], corner_radius=12)
        filtro_frame.pack(fill="x", padx=10, pady=(5, 5))

        ctk.CTkLabel(filtro_frame, text="Pesquisar:").grid(row=0, column=0, padx=5)
        self.entry_busca = ctk.CTkEntry(filtro_frame, width=200)
        self.entry_busca.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(filtro_frame, text="Filtrar Categoria:").grid(row=0, column=2, padx=5)
        self.combo_categoria = ctk.CTkComboBox(filtro_frame, values=["Todas"] + self.categorias)
        self.combo_categoria.set("Todas")
        self.combo_categoria.grid(row=0, column=3, padx=5)

        ctk.CTkButton(filtro_frame, text="🔍 Aplicar", command=self.filtrar_produtos).grid(row=0, column=4, padx=5)

        # === LISTA DE PRODUTOS ===
        self.lista_frame = ctk.CTkScrollableFrame(main_frame, fg_color=cores["BACKGROUND"])
        self.lista_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.atualizar_lista()

    # === FILTRO DE PRODUTOS ===
    def filtrar_produtos(self):
        busca = self.entry_busca.get().lower()
        categoria = self.combo_categoria.get()
        produtos_filtrados = []
        for p in self.produtos:
            if (busca in p["nome"].lower()) and (categoria == "Todas" or p.get("categoria") == categoria):
                produtos_filtrados.append(p)
        self.atualizar_lista(produtos_filtrados)

    # === ATUALIZAR LISTA ===
    def atualizar_lista(self, produtos=None):
        for w in self.lista_frame.winfo_children():
            w.destroy()
        if produtos is None:
            produtos = self.produtos

        cores = colors.get_colors()
        for index, prod in enumerate(produtos):
            card = ctk.CTkFrame(self.lista_frame, fg_color=cores["CARD_BG"], corner_radius=12, height=60)
            card.pack(fill="x", padx=10, pady=3)

            img = self.imagens_cache.get(prod["codigo"])
            if img:
                ctk.CTkLabel(card, image=img, text="").place(relx=0.02, rely=0.5, anchor="w")
            else:
                ctk.CTkLabel(card, text="📦", font=ctk.CTkFont(size=25)).place(relx=0.02, rely=0.5, anchor="w")

            ctk.CTkLabel(card, text=prod["nome"], font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=cores["TEXT_PRIMARY"]).place(relx=0.15, rely=0.35, anchor="w")
            ctk.CTkLabel(card, text=f"R$ {prod['preco']:.2f}", font=ctk.CTkFont(size=12),
                         text_color=cores["TEXT_SECONDARY"]).place(relx=0.15, rely=0.7, anchor="w")
            ctk.CTkLabel(card, text=f"Categoria: {prod.get('categoria', 'Sem Categoria')}",
                         font=ctk.CTkFont(size=10), text_color=cores["TEXT_SECONDARY"]).place(relx=0.7, rely=0.5, anchor="w")

            # Botão de editar
            btn_editar = ctk.CTkButton(card, text="✏️", width=40, height=25,
                                       command=lambda p=prod: self.editar_produto(p))
            btn_editar.place(relx=0.9, rely=0.5, anchor="e")

    # === EDITAR PRODUTO ===
    def editar_produto(self, produto):
        self.produto_editando = produto
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, produto["nome"])
        self.entry_preco.delete(0, "end")
        self.entry_preco.insert(0, str(produto["preco"]))
        self.img_path = produto.get("img", "")
        if self.img_path and os.path.isfile(self.img_path):
            img = ctk.CTkImage(light_image=Image.open(self.img_path), size=(120, 120))
            self.img_preview.configure(image=img, text="")
            self.img_preview.image = img
        else:
            self.img_preview.configure(image=None, text="📦")
        # Corrigir erro do CTkComboBox ao setar valor
        if produto.get("categoria") in self.categorias:
            self.combo_categoria_produto.set(produto.get("categoria"))
        else:
            self.combo_categoria_produto.set("Sem Categoria")

    # === FUNÇÃO VOLTAR MENU ===
    def voltar_menu(self):
        from data import menu
        import data.sessao as sessao
        if getattr(sessao, "usuario", None) is None and getattr(sessao, "perfil", None) is None:
            from loja import mostrar_login
            mostrar_login(self.app)
        else:
            menu.mostrar_menu(self.app, usuario=sessao.usuario, perfil=sessao.perfil)


# === CLASSE CATEGORIAS ===
class Categorias:
    def __init__(self, app, repositorio: Repositorio):
        self.app = app
        self.repositorio = repositorio
        self.abrir_categorias()

    def abrir_categorias(self):
        for w in self.app.winfo_children():
            w.destroy()

        cores = colors.get_colors()
        self.app.title("Categorias")

        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        # BOTÃO VOLTAR
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.repositorio.abrir_repositorio
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # TÍTULO
        title_label = ctk.CTkLabel(header, text="🗂 Categorias", font=ctk.CTkFont("Segoe UI", 26, "bold"), text_color="white")
        title_label.grid(row=0, column=1, padx=(0,30), pady=20, sticky="w")

        main_frame = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Nova categoria
        ctk.CTkLabel(main_frame, text="Nova Categoria:").pack(pady=(10,5))
        self.entry_nova_categoria = ctk.CTkEntry(main_frame, width=200)
        self.entry_nova_categoria.pack(pady=5)

        def adicionar_categoria():
            nome = self.entry_nova_categoria.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Informe o nome da categoria")
                return
            crud_categorias.cadastrar_categoria(nome)
            messagebox.showinfo("Sucesso", f"Categoria '{nome}' adicionada!")
            self.repositorio.categorias = ["Sem Categoria"] + crud_categorias.listar_categorias()
            self.entry_nova_categoria.delete(0, "end")
            self.repositorio.abrir_repositorio()

        ctk.CTkButton(main_frame, text="➕ Adicionar Categoria", command=adicionar_categoria).pack(pady=10)

        # Lista de categorias
        categorias = crud_categorias.listar_categorias()
        for cat in categorias:
            ctk.CTkLabel(main_frame, text=cat, font=ctk.CTkFont(size=14)).pack(pady=3)


def abrir_repositorio(app):
    Repositorio(app)
