import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import data.colors as colors
from crud import crud_produtos
from crud import crud_categorias

class Repositorio:
    def __init__(self, app):
        self.app = app
        self.produtos = crud_produtos.listar_produtos()
        self.categorias = ["Sem Categoria"] + crud_categorias.listar_categorias()
        self.imagens_cache = {}
        self.produto_editando = None
        self.img_path = ""
        self.carregar_imagens()
        self.abrir_repositorio()

    def carregar_imagens(self):
        for prod in self.produtos:
            img_path = prod.get("img")
            if img_path and os.path.isfile(img_path):
                try:
                    self.imagens_cache[prod["codigo"]] = ctk.CTkImage(
                        light_image=Image.open(img_path), size=(60, 60)
                    )
                except:
                    self.imagens_cache[prod["codigo"]] = None
            else:
                self.imagens_cache[prod["codigo"]] = None

    def abrir_repositorio(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Sistema PDV - Repositório")
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x", pady=(0, 0))
        header.grid_columnconfigure(1, weight=1)

        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"], command=self.voltar_menu
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        title_label = ctk.CTkLabel(
            header, text="📦 Repositório de Produtos", text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=1, padx=(0, 30), pady=20, sticky="w")

        def alternar_tema():
            colors.alternar_tema()
            self.abrir_repositorio()

        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        theme_button = ctk.CTkButton(
            header, text=icone_tema, width=40, height=40, corner_radius=12,
            fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"], font=ctk.CTkFont(size=25), command=alternar_tema
        )
        theme_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # === FRAME PRINCIPAL ===
        main_container = ctk.CTkFrame(self.app, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        main_container.grid_columnconfigure(0, weight=1)  # Cadastro
        main_container.grid_columnconfigure(1, weight=2)  # Lista
        main_container.grid_rowconfigure(0, weight=1)

        # === COLUNA ESQUERDA ===
        cadastro_frame = ctk.CTkFrame(main_container, fg_color=cores["CARD_BG"], corner_radius=15)
        cadastro_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        cadastro_frame.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(cadastro_frame, text="Gestão de Produto",
                    font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=(15, 10))

        # Container da imagem
        img_container = ctk.CTkFrame(cadastro_frame, width=150, height=150, fg_color=cores["BACKGROUND"])
        img_container.grid(row=1, column=0, pady=(0, 5))
        img_container.grid_propagate(False)

        self.img_preview = ctk.CTkLabel(img_container, text="📷", font=ctk.CTkFont(size=50))
        self.img_preview.pack(expand=True, fill="both")

        def escolher_imagem():
            path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
            if path:
                self.img_path = path
                img = ctk.CTkImage(light_image=Image.open(path), size=(140, 140))
                self.img_preview.configure(image=img, text="")
                self.img_preview.img = img  # manter referência

        ctk.CTkButton(cadastro_frame, text="Selecionar Foto", command=escolher_imagem,
                    fg_color=cores["ENTRY_BG"], text_color=cores["TEXT_PRIMARY"], height=35).grid(
            row=2, column=0, pady=(0, 10), padx=30, sticky="ew"
        )

        # Campo Nome
        ctk.CTkLabel(cadastro_frame, text="Nome do Produto:", anchor="w").grid(
            row=3, column=0, sticky="w", padx=30, pady=(2, 0)
        )
        self.entry_nome = ctk.CTkEntry(cadastro_frame, height=30)
        self.entry_nome.grid(row=4, column=0, sticky="ew", padx=30, pady=(0, 5))

        # === FRAME PARA COLOCAR PREÇO E ESTOQUE LADO A LADO ===
        frame_linha2 = ctk.CTkFrame(cadastro_frame, fg_color="transparent")
        frame_linha2.grid(row=5, column=0, sticky="ew", padx=30, pady=(0, 5))
        frame_linha2.grid_columnconfigure(0, weight=1)
        frame_linha2.grid_columnconfigure(1, weight=1)

        # Preço
        ctk.CTkLabel(frame_linha2, text="Preço Unitário (R$):", anchor="w").grid(row=0, column=0, sticky="w")
        self.entry_preco = ctk.CTkEntry(frame_linha2, height=30)
        self.entry_preco.grid(row=1, column=0, sticky="ew", pady=(0,5), padx=(0,5))  # padding à direita

        # Estoque
        ctk.CTkLabel(frame_linha2, text="Quantidade em Estoque:", anchor="w").grid(row=0, column=1, sticky="w")
        self.entry_estoque = ctk.CTkEntry(frame_linha2, height=30)
        self.entry_estoque.grid(row=1, column=1, sticky="ew", pady=(0,5), padx=(5,0))  # padding à esquerda

        # Código de barras
        ctk.CTkLabel(cadastro_frame, text="Código de Barras:", anchor="w").grid(
            row=6, column=0, sticky="w", padx=30, pady=(2, 0)
        )
        self.entry_cod_barras = ctk.CTkEntry(cadastro_frame, height=30)
        self.entry_cod_barras.grid(row=7, column=0, sticky="ew", padx=30, pady=(0,5))

        vcmd = (self.app.register(self.validar_cod_barras), '%P')
        self.entry_cod_barras.configure(validate="key", validatecommand=vcmd)
        self.entry_cod_barras.bind("<FocusOut>", self.formatar_cod_barras)

        # Categoria
        ctk.CTkLabel(cadastro_frame, text="Categoria:", anchor="w").grid(row=8, column=0, sticky="w", padx=30, pady=(2, 0))
        self.combo_categoria_produto = ctk.CTkComboBox(cadastro_frame, values=self.categorias, height=35)
        self.combo_categoria_produto.set("Sem Categoria")
        self.combo_categoria_produto.grid(row=9, column=0, sticky="ew", padx=30, pady=(0, 10))

        # Botões
        btn_salvar = ctk.CTkButton(cadastro_frame, text="💾 SALVAR PRODUTO", height=35,
                                fg_color=cores["PRIMARY"], font=ctk.CTkFont(weight="bold"),
                                command=self.salvar_produto)
        btn_salvar.grid(row=10, column=0, sticky="ew", padx=30, pady=(5, 5))

        ctk.CTkButton(cadastro_frame, text="🗂 Gerenciar Categorias", height=30,
                    fg_color="transparent", border_width=1, border_color=cores["PRIMARY"],
                    text_color=cores["TEXT_PRIMARY"], command=lambda: Categorias(self.app, self)).grid(
            row=11, column=0, sticky="ew", padx=30, pady=(0, 10)
        )
        
        # === COLUNA DIREITA: PESQUISA E LISTAGEM ===
        list_container = ctk.CTkFrame(main_container, fg_color="transparent")
        list_container.grid(row=0, column=1, sticky="nsew")
        list_container.grid_rowconfigure(1, weight=1)
        list_container.grid_columnconfigure(0, weight=1)

        # Filtros
        filtro_frame = ctk.CTkFrame(list_container, fg_color=cores["CARD_BG"], height=60)
        filtro_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.entry_busca = ctk.CTkEntry(filtro_frame, placeholder_text="🔍 Pesquisar produto...", width=300)
        self.entry_busca.pack(side="left", padx=15, pady=10)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.filtrar_produtos())

        self.combo_filtro_cat = ctk.CTkComboBox(filtro_frame, values=["Todas"] + self.categorias,
                                                command=lambda x: self.filtrar_produtos())
        self.combo_filtro_cat.set("Todas")
        self.combo_filtro_cat.pack(side="left", padx=5)

        btn_nova_categoria = ctk.CTkButton(
            filtro_frame,
            text="➕ Categoria",
            width=120,
            height=32,
            fg_color=cores["PRIMARY"],
            command=lambda: Categorias(self.app, self)
        )
        btn_nova_categoria.pack(side="left", padx=(5, 10))

        # Scrollable Frame para os Cards
        self.lista_frame = ctk.CTkScrollableFrame(list_container, fg_color=cores["BACKGROUND"], corner_radius=15)
        self.lista_frame.grid(row=1, column=0, sticky="nsew")

        self.atualizar_lista()

    # === FUNÇÕES DE INPUT ===
    def create_input_field(self, parent, label_text, attr_name):
        cores = colors.get_colors()
        ctk.CTkLabel(parent, text=label_text, anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        entry = ctk.CTkEntry(parent, height=40)
        entry.pack(fill="x", padx=30, pady=(0, 10))
        setattr(self, attr_name, entry)

    def validar_cod_barras(self, novo_valor):
        # Permitir apenas números, máximo 13
        numeros = ''.join(filter(str.isdigit, novo_valor))
        if len(numeros) > 13:
            return False
        return True

    def formatar_cod_barras(self, event=None):
        entry = self.entry_cod_barras
        valor = entry.get()
        numeros = ''.join(filter(str.isdigit, valor))[:13]
        partes = []

        if len(numeros) >= 3:
            partes.append(numeros[:3])
        if len(numeros) >= 7:
            partes.append(numeros[3:7])
        elif len(numeros) > 3:
            partes.append(numeros[3:])
        if len(numeros) >= 12:
            partes.append(numeros[7:12])
            partes.append(numeros[12])
        elif len(numeros) > 7:
            partes.append(numeros[7:])

        entry.delete(0, "end")
        entry.insert(0, ' '.join(partes))

    # === FUNÇÕES DE PRODUTO ===
    def salvar_produto(self):
        nome = self.entry_nome.get().strip()
        preco = self.entry_preco.get().strip().replace(",", ".")
        estoque = self.entry_estoque.get().strip()
        cod_barras = ''.join(filter(str.isdigit, self.entry_cod_barras.get()))
        categoria = self.combo_categoria_produto.get()
        img = self.img_path

        if not nome or not preco or not estoque:
            messagebox.showerror("Erro", "Nome, preço e estoque são obrigatórios.")
            return

        if cod_barras and len(cod_barras) != 13:
            messagebox.showerror("Erro", "Código de barras inválido. Deve ter exatamente 13 dígitos.")
            return

        try:
            preco_valor = float(preco)
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido. Use números (ex: 10,50 ou 10.50)")
            return
        try:
            estoque_valor = int(estoque)
        except ValueError:
            messagebox.showerror("Erro", "Estoque inválido. Use apenas números inteiros.")
            return

        if self.produto_editando:
            crud_produtos.atualizar_produto(
                self.produto_editando["codigo"],
                nome,
                preco_valor,
                estoque_valor,
                codigo_barras=cod_barras,
                img=img,
                categoria_nome=categoria
            )
            messagebox.showinfo("Sucesso", "Produto atualizado!")
            self.produto_editando = None
        else:
            crud_produtos.cadastrar_produto(
                nome,
                preco_valor,
                estoque_valor,
                codigo_barras=cod_barras,
                img=img,
                categoria_nome=categoria
            )
            messagebox.showinfo("Sucesso", "Produto cadastrado!")

        self.resetar_campos()
        self.produtos = crud_produtos.listar_produtos()
        self.carregar_imagens()
        self.atualizar_lista()

    def resetar_campos(self):
        self.entry_nome.delete(0, "end")
        self.entry_preco.delete(0, "end")
        self.entry_estoque.delete(0, "end")
        self.entry_cod_barras.delete(0, "end")
        self.img_preview.configure(image=None, text="📷")
        self.img_path = ""
        self.combo_categoria_produto.set("Sem Categoria")

    # === FILTRAR E LISTAR ===
    def filtrar_produtos(self):
        busca = self.entry_busca.get().lower()
        categoria = self.combo_filtro_cat.get()
        produtos_filtrados = [
            p for p in self.produtos
            if (busca in p["nome"].lower()) and (categoria == "Todas" or p.get("categoria") == categoria)
        ]
        self.atualizar_lista(produtos_filtrados)

    def atualizar_lista(self, produtos=None):
        for w in self.lista_frame.winfo_children():
            w.destroy()

        lista = produtos if produtos is not None else self.produtos
        cores = colors.get_colors()

        for prod in lista:
            card = ctk.CTkFrame(self.lista_frame, fg_color=cores["CARD_BG"], height=80, corner_radius=10)
            card.pack(fill="x", padx=5, pady=5)
            card.pack_propagate(False)

            img = self.imagens_cache.get(prod["codigo"])
            lbl_img = ctk.CTkLabel(card, text="📦" if not img else "", image=img, width=60)
            lbl_img.pack(side="left", padx=15)

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, pady=10)

            ctk.CTkLabel(info_frame, text=prod["nome"], font=ctk.CTkFont(size=15, weight="bold"), anchor="w").pack(fill="x")

            cod_barras = prod.get("codigo_barras", "")
            categoria = prod.get("categoria", "Sem Categoria")
            preco = f"{prod['preco']:.2f}"
            estoque = prod.get("estoque", 0)

            ctk.CTkLabel(
                info_frame,
                text=f"{categoria} • R$ {preco} • Estoque: {estoque} • Código: {cod_barras}",
                font=ctk.CTkFont(size=12),
                text_color=cores["TEXT_SECONDARY"],
                anchor="w"
            ).pack(fill="x")

            btn_edit = ctk.CTkButton(
                card, text="Editar", width=70, height=30,
                fg_color=cores["PRIMARY"], command=lambda p=prod: self.editar_produto(p)
            )
            btn_edit.pack(side="right", padx=15)

    # === EDITAR PRODUTO ===
    def editar_produto(self, produto):
        self.produto_editando = produto
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, produto["nome"])
        self.entry_preco.delete(0, "end")
        self.entry_preco.insert(0, str(produto["preco"]))
        self.entry_estoque.delete(0, "end")
        self.entry_estoque.insert(0, str(produto.get("estoque", 0)))
        self.entry_cod_barras.delete(0, "end")
        self.entry_cod_barras.insert(0, produto.get("codigo_barras", ""))
        self.img_path = produto.get("img", "")

        if self.img_path and os.path.isfile(self.img_path):
            img = ctk.CTkImage(light_image=Image.open(self.img_path), size=(140, 140))
            self.img_preview.configure(image=img, text="")
        else:
            self.img_preview.configure(image=None, text="📷")

        categoria = produto.get("categoria")
        if categoria and categoria in self.categorias:
            self.combo_categoria_produto.set(categoria)
        else:
            self.combo_categoria_produto.set("Sem Categoria")

    def voltar_menu(self):
        from data import menu
        import data.sessao as sessao
        menu.mostrar_menu(self.app, usuario=sessao.nome, perfil=sessao.perfil)


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

        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80)
        header.pack(fill="x")

        ctk.CTkButton(header, text="⬅", width=40, command=self.repositorio.abrir_repositorio).pack(side="left", padx=20)
        ctk.CTkLabel(header, text="Gerenciar Categorias", font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="white").pack(side="left")

        main = ctk.CTkFrame(self.app, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=20)

        input_f = ctk.CTkFrame(main, fg_color=cores["CARD_BG"], width=300, corner_radius=15)
        input_f.pack(side="left", fill="y", padx=(0, 20), pady=10)

        ctk.CTkLabel(input_f, text="Nova Categoria", font=ctk.CTkFont(weight="bold")).pack(pady=20)
        self.entry_cat = ctk.CTkEntry(input_f, placeholder_text="Ex: Bebidas", width=220)
        self.entry_cat.pack(pady=10)

        def add():
            nome = self.entry_cat.get().strip()
            if nome:
                crud_categorias.cadastrar_categoria(nome)
                self.repositorio.categorias = ["Sem Categoria"] + crud_categorias.listar_categorias()
                self.abrir_categorias()

        ctk.CTkButton(input_f, text="Adicionar", command=add, fg_color=cores["PRIMARY"]).pack(pady=20)

        list_f = ctk.CTkScrollableFrame(main, fg_color=cores["CARD_BG"], corner_radius=15)
        list_f.pack(side="right", fill="both", expand=True, pady=10)

        for cat in crud_categorias.listar_categorias():
            item = ctk.CTkFrame(list_f, fg_color=cores["BACKGROUND"], height=40)
            item.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(item, text=f"• {cat}", font=ctk.CTkFont(size=14)).pack(side="left", padx=15)


def abrir_repositorio(app):
    Repositorio(app)
