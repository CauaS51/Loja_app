import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps
import io
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
        self.img_bytes = None 
        
        # --- CARREGAMENTO DA LOGO DO CABEÇALHO ---
        self.logo_header = None
        self.carregar_logo_sistema()
        
        self.carregar_imagens_produtos()
        self.abrir_repositorio()

    def carregar_logo_sistema(self):
        """Carrega a logo que aparece no topo da tela."""
        try:
            # Tenta encontrar a logo (ajuste o nome do arquivo se necessário)
            caminho_logo = "logo.png" 
            if os.path.exists(caminho_logo):
                img_pil = Image.open(caminho_logo)
                # Ajuste o size=(50, 50) para mudar o tamanho da logo no topo
                self.logo_header = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(50, 50))
        except Exception as e:
            print(f"Aviso: Não foi possível carregar a logo do cabeçalho: {e}")

    def carregar_imagens_produtos(self):
        """Lê os bytes dos produtos e coloca no cache."""
        for prod in self.produtos:
            img_data = prod.get("img")
            if img_data:
                try:
                    img_pil = Image.open(io.BytesIO(img_data))
                    self.imagens_cache[prod["codigo"]] = ctk.CTkImage(
                        light_image=img_pil, size=(60, 60)
                    )
                except Exception as e:
                    self.imagens_cache[prod["codigo"]] = None
            else:
                self.imagens_cache[prod["codigo"]] = None

    def abrir_repositorio(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Sistema PDV - Repositório")
        cores = colors.get_colors()

        # === HEADER (CABEÇALHO) ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x", pady=(0, 0))
        header.grid_columnconfigure(1, weight=1)

        # Botão Voltar
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"], command=self.voltar_menu
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Container para Logo + Título (para ficarem juntos no centro/esquerda)
        title_container = ctk.CTkFrame(header, fg_color="transparent")
        title_container.grid(row=0, column=1, sticky="w")

        if self.logo_header:
            lbl_logo = ctk.CTkLabel(title_container, image=self.logo_header, text="")
            lbl_logo.pack(side="left", padx=(0, 15))

        title_label = ctk.CTkLabel(
            title_container, text="📦 Repositório de Produtos", text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.pack(side="left")

        # Botão de Tema
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

        # === CONTEÚDO PRINCIPAL ===
        main_container = ctk.CTkFrame(self.app, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        main_container.grid_rowconfigure(0, weight=1)

        # --- COLUNA ESQUERDA: CADASTRO ---
        self.criar_coluna_cadastro(main_container, cores)
        
        # --- COLUNA DIREITA: LISTA ---
        self.criar_coluna_lista(main_container, cores)

    def criar_coluna_cadastro(self, container, cores):
        cadastro_frame = ctk.CTkFrame(container, fg_color=cores["CARD_BG"], corner_radius=15)
        cadastro_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        cadastro_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(cadastro_frame, text="Gestão de Produto",
                    font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=(15, 10))

        img_container = ctk.CTkFrame(cadastro_frame, width=150, height=150, fg_color=cores["BACKGROUND"])
        img_container.grid(row=1, column=0, pady=(0, 5))
        img_container.grid_propagate(False)

        self.img_preview = ctk.CTkLabel(img_container, text="📷", font=ctk.CTkFont(size=50))
        self.img_preview.pack(expand=True, fill="both")

        def escolher_imagem():
            path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
            if path:
                try:
                    with open(path, "rb") as f:
                        self.img_bytes = f.read()
                    img_pil = Image.open(io.BytesIO(self.img_bytes))
                    img_ctk = ctk.CTkImage(light_image=img_pil, size=(140, 140))
                    self.img_preview.configure(image=img_ctk, text="")
                    self.img_preview.img = img_ctk 
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro na imagem: {e}")

        ctk.CTkButton(cadastro_frame, text="Selecionar Foto", command=escolher_imagem,
                    fg_color=cores["ENTRY_BG"], text_color=cores["TEXT_PRIMARY"], height=35).grid(
            row=2, column=0, pady=(0, 10), padx=30, sticky="ew"
        )

        # Campos de entrada
        self.entry_nome = self.criar_campo(cadastro_frame, "Nome do Produto:", 3)
        
        linha_pre_est = ctk.CTkFrame(cadastro_frame, fg_color="transparent")
        linha_pre_est.grid(row=5, column=0, sticky="ew", padx=30)
        linha_pre_est.grid_columnconfigure((0,1), weight=1)

        ctk.CTkLabel(linha_pre_est, text="Preço (R$):").grid(row=0, column=0, sticky="w")
        self.entry_preco = ctk.CTkEntry(linha_pre_est, height=30)
        self.entry_preco.grid(row=1, column=0, sticky="ew", padx=(0,5))

        ctk.CTkLabel(linha_pre_est, text="Estoque:").grid(row=0, column=1, sticky="w")
        self.entry_estoque = ctk.CTkEntry(linha_pre_est, height=30)
        self.entry_estoque.grid(row=1, column=1, sticky="ew", padx=(5,0))

        self.entry_cod_barras = self.criar_campo(cadastro_frame, "Código de Barras:", 6)
        
        ctk.CTkLabel(cadastro_frame, text="Categoria:").grid(row=8, column=0, sticky="w", padx=30)
        self.combo_categoria_produto = ctk.CTkComboBox(cadastro_frame, values=self.categorias, height=35)
        self.combo_categoria_produto.set("Sem Categoria")
        self.combo_categoria_produto.grid(row=9, column=0, sticky="ew", padx=30, pady=(0, 10))

        ctk.CTkButton(cadastro_frame, text="💾 SALVAR PRODUTO", height=40,
                    fg_color=cores["PRIMARY"], font=ctk.CTkFont(weight="bold"),
                    command=self.salvar_produto).grid(row=10, column=0, sticky="ew", padx=30, pady=5)

        ctk.CTkButton(cadastro_frame, text="🗂 Gerenciar Categorias", height=30,
                    fg_color="transparent", border_width=1, border_color=cores["PRIMARY"],
                    text_color=cores["TEXT_PRIMARY"], command=lambda: Categorias(self.app, self)).grid(
            row=11, column=0, sticky="ew", padx=30, pady=(0, 10)
        )

    def criar_coluna_lista(self, container, cores):
        list_container = ctk.CTkFrame(container, fg_color="transparent")
        list_container.grid(row=0, column=1, sticky="nsew")
        list_container.grid_rowconfigure(1, weight=1)
        list_container.grid_columnconfigure(0, weight=1)

        filtro_frame = ctk.CTkFrame(list_container, fg_color=cores["CARD_BG"], height=60)
        filtro_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.entry_busca = ctk.CTkEntry(filtro_frame, placeholder_text="🔍 Pesquisar produto...", width=300)
        self.entry_busca.pack(side="left", padx=15, pady=10)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.filtrar_produtos())

        self.combo_filtro_cat = ctk.CTkComboBox(filtro_frame, values=["Todas"] + self.categorias,
                                                command=lambda x: self.filtrar_produtos())
        self.combo_filtro_cat.set("Todas")
        self.combo_filtro_cat.pack(side="left", padx=5)

        self.lista_frame = ctk.CTkScrollableFrame(list_container, fg_color=cores["BACKGROUND"], corner_radius=15)
        self.lista_frame.grid(row=1, column=0, sticky="nsew")
        self.atualizar_lista()

    def criar_campo(self, master, texto, row):
        ctk.CTkLabel(master, text=texto).grid(row=row, column=0, sticky="w", padx=30, pady=(5,0))
        entry = ctk.CTkEntry(master, height=30)
        entry.grid(row=row+1, column=0, sticky="ew", padx=30, pady=(0,5))
        return entry

    # --- LÓGICA DE DADOS ---
    def salvar_produto(self):
        nome = self.entry_nome.get().strip()
        preco = self.entry_preco.get().strip().replace(",", ".")
        estoque = self.entry_estoque.get().strip()
        cod_barras = ''.join(filter(str.isdigit, self.entry_cod_barras.get()))
        categoria = self.combo_categoria_produto.get()

        if not nome or not preco or not estoque:
            messagebox.showerror("Erro", "Campos obrigatórios vazios.")
            return

        try:
            p_val, e_val = float(preco), int(estoque)
            if self.produto_editando:
                crud_produtos.atualizar_produto(self.produto_editando["codigo"], nome, p_val, e_val, cod_barras, self.img_bytes, categoria)
            else:
                crud_produtos.cadastrar_produto(nome, p_val, e_val, cod_barras, self.img_bytes, categoria)
            
            messagebox.showinfo("Sucesso", "Operação realizada!")
            self.resetar_campos()
            self.produtos = crud_produtos.listar_produtos()
            self.carregar_imagens_produtos()
            self.atualizar_lista()
        except ValueError:
            messagebox.showerror("Erro", "Preço ou estoque inválidos.")

    def resetar_campos(self):
        self.entry_nome.delete(0, "end")
        self.entry_preco.delete(0, "end")
        self.entry_estoque.delete(0, "end")
        self.entry_cod_barras.delete(0, "end")
        self.img_preview.configure(image=None, text="📷")
        self.img_bytes = None
        self.produto_editando = None

    def atualizar_lista(self, produtos=None):
        for w in self.lista_frame.winfo_children(): w.destroy()
        lista = produtos if produtos is not None else self.produtos
        cores = colors.get_colors()

        for prod in lista:
            card = ctk.CTkFrame(self.lista_frame, fg_color=cores["CARD_BG"], height=80, corner_radius=10)
            card.pack(fill="x", padx=5, pady=5)
            card.pack_propagate(False)

            img = self.imagens_cache.get(prod["codigo"])
            ctk.CTkLabel(card, text="📦" if not img else "", image=img, width=60).pack(side="left", padx=15)

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, pady=10)
            ctk.CTkLabel(info, text=prod["nome"], font=("Segoe UI", 14, "bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=f"R$ {prod['preco']:.2f} | Estoque: {prod.get('estoque',0)}", 
                        text_color=cores["TEXT_SECONDARY"], font=("Segoe UI", 11), anchor="w").pack(fill="x")

            ctk.CTkButton(card, text="Editar", width=70, fg_color=cores["PRIMARY"], 
                         command=lambda p=prod: self.editar_produto(p)).pack(side="right", padx=15)

    def editar_produto(self, produto):
        self.resetar_campos()
        self.produto_editando = produto
        self.entry_nome.insert(0, produto["nome"])
        self.entry_preco.insert(0, str(produto["preco"]))
        self.entry_estoque.insert(0, str(produto.get("estoque", 0)))
        self.entry_cod_barras.insert(0, produto.get("codigo_barras", ""))
        self.img_bytes = produto.get("img")
        if self.img_bytes:
            img_pil = Image.open(io.BytesIO(self.img_bytes))
            img_ctk = ctk.CTkImage(light_image=img_pil, size=(140, 140))
            self.img_preview.configure(image=img_ctk, text="")
        self.combo_categoria_produto.set(produto.get("categoria", "Sem Categoria"))

    def filtrar_produtos(self):
        busca = self.entry_busca.get().lower()
        cat = self.combo_filtro_cat.get()
        filtrados = [p for p in self.produtos if (busca in p["nome"].lower()) and (cat == "Todas" or p.get("categoria") == cat)]
        self.atualizar_lista(filtrados)

    def voltar_menu(self):
        from data import menu
        import data.sessao as sessao
        menu.mostrar_menu(self.app, usuario=sessao.nome, perfil=sessao.perfil)

class Categorias:
    def __init__(self, app, repositorio: Repositorio):
        self.app = app
        self.repositorio = repositorio
        self.abrir_categorias()

    def abrir_categorias(self):
        for w in self.app.winfo_children(): w.destroy()
        cores = colors.get_colors()
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80)
        header.pack(fill="x")
        ctk.CTkButton(header, text="⬅", width=40, command=self.repositorio.abrir_repositorio).pack(side="left", padx=20)
        ctk.CTkLabel(header, text="Gerenciar Categorias", font=("Segoe UI", 22, "bold"), text_color="white").pack(side="left")
        
        main = ctk.CTkFrame(self.app, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=20)
        
        input_f = ctk.CTkFrame(main, fg_color=cores["CARD_BG"], width=300, corner_radius=15)
        input_f.pack(side="left", fill="y", padx=(0, 20), pady=10)
        
        self.entry_cat = ctk.CTkEntry(input_f, placeholder_text="Ex: Bebidas", width=220)
        self.entry_cat.pack(pady=20)
        
        def add():
            nome = self.entry_cat.get().strip()
            if nome:
                crud_categorias.cadastrar_categoria(nome)
                self.repositorio.categorias = ["Sem Categoria"] + crud_categorias.listar_categorias()
                self.abrir_categorias()
        
        ctk.CTkButton(input_f, text="Adicionar", command=add, fg_color=cores["PRIMARY"]).pack()
        
        list_f = ctk.CTkScrollableFrame(main, fg_color=cores["CARD_BG"], corner_radius=15)
        list_f.pack(side="right", fill="both", expand=True, pady=10)
        for cat in crud_categorias.listar_categorias():
            item = ctk.CTkFrame(list_f, fg_color=cores["BACKGROUND"], height=40)
            item.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(item, text=f"• {cat}").pack(side="left", padx=15)

def abrir_repositorio(app):
    Repositorio(app)