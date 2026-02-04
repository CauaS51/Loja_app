import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import data.colors as colors
import data.sessao as sessao
import crud.crud_produtos as produtos_crud
from decimal import Decimal, ROUND_HALF_UP
import tkinter as tk
import os

class CaixaApp:
    def __init__(self, app):
        self.app = app
        self.produto_selecionado_esq = None
        self.produto_selecionado_dir = None
        self.itens_carrinho = {}
        self.btns_produtos = {}
        self.btns_carrinho = {}
        self.img_label = None
        self.produtos = []
        self.current_image = None

        # Usar apenas StringVar para quantidade
        self.quantidade_var = ctk.StringVar(value="1")

        self.criar_tela()
        self.carregar_produtos()

    # ==================== CRIAÇÃO DA TELA ====================
    def criar_tela(self):
        """Cria e configura a interface principal do caixa"""
        try:
            # Limpar tela anterior
            for widget in self.app.winfo_children():
                widget.destroy()

            self.app.title("Sistema PDV - Caixa")
            self.app.geometry("1300x750")
           
            # Configurar layout
            self.app.grid_columnconfigure(0, weight=1)
            self.app.grid_rowconfigure(0, weight=1)

            # HEADER
            self.criar_header()

            # BODY
            self.criar_body()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar interface: {str(e)}")
            raise

    def criar_header(self):
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(
            self.app,
            fg_color=cores["PRIMARY"],
            height=80,
            corner_radius=0
        )
        header.pack(fill="x")

        # Botão voltar
        btn_voltar = ctk.CTkButton(
            header,
            text="⬅",
            width=40,
            height=40,
            font=ctk.CTkFont(size=20),
            corner_radius=12,
            text_color=cores["TEXT_PRIMARY"],
            fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"],
            command=self.voltar_menu
        )
        btn_voltar.pack(side="left", padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            header,
            text="🛒 Caixa · PDV",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        ).pack(side="left", pady=20)

        # ===== DIREITA (OPERADOR + TEMA) =====
        right_container = ctk.CTkFrame(header, fg_color="transparent")
        right_container.pack(side="right", padx=20, pady=20)

        # Operador
        ctk.CTkLabel(
            right_container,
            text=f"Operador: {sessao.nome}",
            fg_color='white',
            corner_radius=10,
            height=36,
            padx=12,
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            text_color=cores["SECONDARY"]
        ).pack(side="left", padx=(0, 8))

        # Botão tema
        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        ctk.CTkButton(
            right_container,
            text=icone_tema,
            width=40,
            height=40,
            corner_radius=12,
            fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"],
            font=ctk.CTkFont(size=25),
            command=self.alternar_tema
        ).pack(side="left")

    def criar_body(self):
        """Cria o corpo principal da aplicação"""
        cores = colors.get_colors()
        body = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"])
        body.pack(fill="both", expand=True, padx=10, pady=5)
        body.grid_columnconfigure((0, 1), weight=1)
        body.grid_rowconfigure(0, weight=1)

        # Colunas
        self.criar_coluna_esquerda(body, cores)
        self.criar_coluna_direita(body, cores)

    # ==================== COLUNA ESQUERDA ====================
    def criar_coluna_esquerda(self, parent, cores):
        """Cria a coluna esquerda com lista de produtos e detalhes"""
        left = ctk.CTkFrame(parent, fg_color=cores["BACKGROUND"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        # Frame de detalhes do produto
        self.criar_frame_detalhes_produto(left, cores)

        # Campo de busca
        self.search = ctk.CTkEntry(
            left, placeholder_text="🔍 Buscar produto por nome ou código...",
            height=40, font=ctk.CTkFont(family="Segoe UI", size=13),
            border_width=1, corner_radius=8
        )
        self.search.pack(fill="x", pady=(0, 10))
        self.search.bind("<KeyRelease>", lambda e: self.filtrar_produtos())

        # Lista de produtos
        self.lista_produtos = ctk.CTkScrollableFrame(
            left, fg_color=cores["BACKGROUND"]
        )
        self.lista_produtos.pack(fill="both", expand=True)

    def criar_frame_detalhes_produto(self, parent, cores):
        """Cria o frame com detalhes e imagem do produto"""
        frame_detalhes = ctk.CTkFrame(parent, fg_color=cores["CARD_BG"], corner_radius=10)
        frame_detalhes.pack(fill="x", pady=(0, 15))

        # Imagem do produto
        self.img_label = ctk.CTkLabel(
            frame_detalhes, text="🖼️",
            width=220, height=300, corner_radius=8,
            fg_color=cores["ENTRY_BG"], text_color=cores["TEXT_SECONDARY"],
            font=ctk.CTkFont(size=40),
            anchor="center"
        )
        self.img_label.pack(side="left", padx=15, pady=15)

        # Informações do produto
        frame_info = ctk.CTkFrame(frame_detalhes, fg_color="transparent")
        frame_info.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        # Título
        self.lbl_nome = ctk.CTkLabel(
            frame_info, text="SELECIONE UM PRODUTO",
            anchor="w", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=cores["TEXT_PRIMARY"]
        )
        self.lbl_nome.pack(fill="x", pady=(0, 10))

        # Informações
        self.lbl_codigo = ctk.CTkLabel(
            frame_info, text="Código: ---",
            anchor="w", font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.lbl_codigo.pack(fill="x", pady=2)
       
        self.lbl_categoria = ctk.CTkLabel(
            frame_info, text="Categoria: ---",
            anchor="w", font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.lbl_categoria.pack(fill="x", pady=2)
       
        self.lbl_preco_unit = ctk.CTkLabel(
            frame_info, text="Preço Unitário: R$ 0,00",
            anchor="w", font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.lbl_preco_unit.pack(fill="x", pady=2)

        # Separador
        separator_color = "#E0E0E0" if ctk.get_appearance_mode() == "Light" else "#444444"
        ctk.CTkFrame(frame_info, height=1, fg_color=separator_color).pack(fill="x", pady=15)

        # Quantidade
        frame_qtd = ctk.CTkFrame(frame_info, fg_color="transparent")
        frame_qtd.pack(fill="x", pady=5)

        ctk.CTkLabel(
            frame_qtd, text="Quantidade:",
            font=ctk.CTkFont(family="Segoe UI", size=13)
        ).pack(side="left", padx=(0, 10))

        # Botões de controle de quantidade
        ctk.CTkButton(
            frame_qtd, text="−", width=30, height=30,
            command=self.diminuir_quantidade,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6B7280", hover_color="#4B5563"
        ).pack(side="left", padx=2)

        self.quantidade_entry = ctk.CTkEntry(
            frame_qtd, textvariable=self.quantidade_var,
            width=60, font=ctk.CTkFont(family="Segoe UI", size=13), justify="center"
        )
        self.quantidade_entry.pack(side="left", padx=2)

        ctk.CTkButton(
            frame_qtd, text="+", width=30, height=30,
            command=self.aumentar_quantidade,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6B7280", hover_color="#4B5563"
        ).pack(side="left", padx=2)

        # Preço total
        self.lbl_preco_total = ctk.CTkLabel(
            frame_info, text="Total: R$ 0,00",
            anchor="w", font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#10B981"  # Verde para valores positivos
        )
        self.lbl_preco_total.pack(fill="x", pady=(15, 10))

        # Botão adicionar
        self.btn_adicionar = ctk.CTkButton(
            frame_info, text="➕ ADICIONAR AO CARRINHO",
            height=40, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#10B981", hover_color="#059669",  # Verde
            command=self.adicionar_carrinho
        )
        self.btn_adicionar.pack(fill="x", pady=(5, 0))

        # Vincular atualização automática
        self.quantidade_var.trace_add("write", lambda *args: self.atualizar_info_produto())

    # ==================== COLUNA DIREITA ====================
    def criar_coluna_direita(self, parent, cores):
        """Cria a coluna direita com carrinho e resumo"""
        right = ctk.CTkFrame(parent, fg_color=cores["BACKGROUND"])
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)

        # Título do carrinho
        lbl_titulo_carrinho = ctk.CTkLabel(
            right, text="🧾 CARRINHO DE COMPRAS",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        )
        lbl_titulo_carrinho.pack(anchor="w", pady=(0, 10))

        # Cabeçalho da tabela
        self.criar_cabecalho_carrinho(right, cores)

        # Lista de itens
        self.carrinho = ctk.CTkScrollableFrame(
            right, fg_color=cores["BACKGROUND"]
        )
        self.carrinho.pack(fill="both", expand=True, pady=(0, 10))

        # Botão remover
        self.btn_remover_direita = ctk.CTkButton(
            right, text="🗑️ REMOVER ITEM SELECIONADO",
            height=35, font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="#DC3545", hover_color="#C82333",
            command=self.remover_produto_selecionado_direita
        )
        self.btn_remover_direita.pack(fill="x", pady=(0, 15))

        # Resumo
        self.criar_resumo_compra(right, cores)

        # Botão finalizar
        self.btn_finalizar = ctk.CTkButton(
            right, text="💳 FINALIZAR VENDA",
            height=45, font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=cores["PRIMARY"], hover_color=cores["HOVER"]
            # command=self.finalizar_venda
        )
        self.btn_finalizar.pack(fill="x")

    def criar_cabecalho_carrinho(self, parent, cores):
        """Cria cabeçalho da tabela do carrinho"""
        header = ctk.CTkFrame(parent, fg_color=cores["CARD_BG"], height=35, corner_radius=6)
        header.pack(fill="x")
        header.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(
            header, text="PRODUTO", anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        ).grid(row=0, column=0, padx=10, sticky="w")

        ctk.CTkLabel(
            header, text="QTD", anchor="center",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        ).grid(row=0, column=1, padx=10)

        ctk.CTkLabel(
            header, text="UNITÁRIO", anchor="e",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        ).grid(row=0, column=2, padx=10, sticky="e")

        ctk.CTkLabel(
            header, text="TOTAL", anchor="e",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        ).grid(row=0, column=3, padx=10, sticky="e")

    def criar_resumo_compra(self, parent, cores):
        """Cria resumo da compra com totais"""
        resumo = ctk.CTkFrame(parent, fg_color=cores["CARD_BG"], corner_radius=8)
        resumo.pack(fill="x", pady=(0, 15))

        # Título
        ctk.CTkLabel(
            resumo, text="RESUMO DA COMPRA",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(pady=(10, 15))

        # Itens
        frame_itens = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_itens.pack(fill="x", padx=15, pady=2)

        self.lbl_itens = ctk.CTkLabel(
            frame_itens, text="Itens: 0",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.lbl_itens.pack(anchor="w")

        # Subtotal
        frame_sub = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_sub.pack(fill="x", padx=15, pady=2)

        self.lbl_sub = ctk.CTkLabel(
            frame_sub, text="Subtotal: R$ 0,00",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.lbl_sub.pack(anchor="w")

        # Desconto
        frame_desc = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_desc.pack(fill="x", padx=15, pady=2)

        self.lbl_desconto = ctk.CTkLabel(
            frame_desc, text="Desconto: R$ 0,00",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.lbl_desconto.pack(anchor="w")

        # Acréscimo
        frame_acres = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_acres.pack(fill="x", padx=15, pady=2)

        self.lbl_acrescimo = ctk.CTkLabel(
            frame_acres, text="Acréscimo: R$ 0,00",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.lbl_acrescimo.pack(anchor="w")

        # Separador
        separator_color = "#E0E0E0" if ctk.get_appearance_mode() == "Light" else "#444444"
        ctk.CTkFrame(resumo, height=1, fg_color=separator_color).pack(fill="x", padx=15, pady=10)

        # Total
        frame_total = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_total.pack(fill="x", padx=15, pady=(0, 15))

        self.lbl_total = ctk.CTkLabel(
            frame_total, text="TOTAL: R$ 0,00",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=cores["PRIMARY"]
        )
        self.lbl_total.pack(anchor="e")

    # ==================== FUNÇÕES AUXILIARES ====================
    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app, sessao.nome, sessao.perfil)

    def alternar_tema(self):
        colors.alternar_tema()
        self.criar_tela()
        self.carregar_produtos()
        self.atualizar_carrinho()
        self.atualizar_totais()

    def aumentar_quantidade(self):
        """Aumenta a quantidade em 1"""
        try:
            qtd = int(self.quantidade_var.get() or "1")
            self.quantidade_var.set(str(qtd + 1))
        except ValueError:
            self.quantidade_var.set("1")

    def diminuir_quantidade(self):
        """Diminui a quantidade em 1, mínimo 1"""
        try:
            qtd = int(self.quantidade_var.get() or "1")
            if qtd > 1:
                self.quantidade_var.set(str(qtd - 1))
        except ValueError:
            self.quantidade_var.set("1")

    def get_quantidade(self):
        """Obtém e valida a quantidade digitada"""
        try:
            qtd = int(self.quantidade_var.get() or "1")
            return max(1, qtd)
        except (ValueError, tk.TclError):
            return 1

    # ==================== CARREGAR E EXIBIR PRODUTOS ====================
    def carregar_produtos(self):
        """Carrega produtos do banco de dados"""
        try:
            self.produtos = produtos_crud.listar_produtos()
            self.exibir_lista_produtos(self.produtos)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")
            self.produtos = []

    def exibir_lista_produtos(self, produtos):
        """Exibe a lista de produtos na interface"""
        for widget in self.lista_produtos.winfo_children():
            widget.destroy()
       
        cores = colors.get_colors()
        self.btns_produtos.clear()
       
        if not produtos:
            ctk.CTkLabel(
                self.lista_produtos, text="Nenhum produto encontrado",
                text_color=cores["TEXT_SECONDARY"], font=ctk.CTkFont(size=12)
            ).pack(pady=20)
            return
       
        for produto in produtos:
            self.criar_botao_produto(produto, cores)

    def criar_botao_produto(self, produto, cores):
        """Cria um botão para cada produto na lista"""
        texto = f"{produto['nome']} | R$ {Decimal(str(produto['preco'])):.2f}"
       
        btn = ctk.CTkButton(
            self.lista_produtos, text=texto,
            text_color=cores["TEXT_PRIMARY"], fg_color=cores["CARD_BG"],
            hover_color=cores["HOVER"], anchor="w", height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            command=lambda p=produto: self.selecionar_produto_esquerda(p)
        )
        btn.pack(fill="x", pady=2, padx=2)
        self.btns_produtos[produto["nome"]] = btn

    # ==================== FILTRAR PRODUTOS ====================
    def filtrar_produtos(self):
        """Filtra produtos conforme texto digitado"""
        termo = self.search.get().lower().strip()
        if not termo:
            self.exibir_lista_produtos(self.produtos)
            return
       
        filtrados = [
            p for p in self.produtos
            if termo in p["nome"].lower() or
               termo in str(p.get("codigo", "")).lower()
        ]
        self.exibir_lista_produtos(filtrados)

    # ==================== SELEÇÃO DE PRODUTOS ====================
    def selecionar_produto_esquerda(self, produto):
        """Seleciona um produto na lista da esquerda"""
        self.produto_selecionado_esq = produto
        cores = colors.get_colors()
       
        # Resetar todos os botões
        for btn in self.btns_produtos.values():
            btn.configure(fg_color=cores["CARD_BG"], text_color=cores["TEXT_PRIMARY"])
       
        # Destacar botão selecionado
        if produto["nome"] in self.btns_produtos:
            self.btns_produtos[produto["nome"]].configure(
                fg_color=cores["PRIMARY"],
                text_color="white"
            )
       
        self.atualizar_imagem(produto)
        self.atualizar_info_produto()

    # ==================== ATUALIZAR IMAGEM ====================
    def atualizar_imagem(self, produto):
        """Atualiza a imagem do produto selecionado"""
        try:
            if produto and "img" in produto and produto["img"]:
                # Verificar se o arquivo existe
                if os.path.exists(produto["img"]):
                    img = Image.open(produto["img"])
                    img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(220, 300))
                   
                    # Limpar imagem anterior
                    if hasattr(self.img_label, 'image'):
                        self.img_label.image = None
                   
                    self.img_label.configure(image=img_ctk, text="")
                    self.current_image = img_ctk
                    self.img_label.image = img_ctk
                else:
                    self.img_label.configure(image="", text="🖼️", font=ctk.CTkFont(size=40))
            else:
                self.img_label.configure(image="", text="🖼️", font=ctk.CTkFont(size=40))
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            self.img_label.configure(image="", text="🖼️", font=ctk.CTkFont(size=40))

    # ==================== ATUALIZAR INFORMAÇÕES ====================
    def atualizar_info_produto(self):
        """Atualiza as informações do produto selecionado"""
        cores = colors.get_colors()
        if not self.produto_selecionado_esq:
            self.lbl_nome.configure(text="SELECIONE UM PRODUTO")
            self.lbl_codigo.configure(text="Código: ---")
            self.lbl_categoria.configure(text="Categoria: ---")
            self.lbl_preco_unit.configure(text="Preço Unitário: R$ 0,00")
            self.lbl_preco_total.configure(text="Total: R$ 0,00")
            return

        produto = self.produto_selecionado_esq
        quantidade = self.get_quantidade()
       
        preco_unitario = Decimal(str(produto.get("preco", 0)))
        preco_total = (preco_unitario * Decimal(quantidade)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        # Atualizar labels
        self.lbl_nome.configure(text=produto.get('nome', '---'))
        self.lbl_codigo.configure(text=f"Código: {produto.get('codigo', '---')}")
        self.lbl_categoria.configure(text=f"Categoria: {produto.get('categoria', '---')}")
        self.lbl_preco_unit.configure(text=f"Preço Unitário: R$ {preco_unitario:.2f}")
        self.lbl_preco_total.configure(text=f"Total: R$ {preco_total:.2f}")

    # ==================== CARRINHO ====================
    def adicionar_carrinho(self):
        """Adiciona produto selecionado ao carrinho"""
        if not self.produto_selecionado_esq:
            messagebox.showwarning("Aviso", "Selecione um produto para adicionar ao carrinho.")
            return

        produto = self.produto_selecionado_esq
        codigo = produto.get("codigo") or f"{produto['nome']}_{produto.get('preco', 0)}"
        quantidade = self.get_quantidade()

        if codigo in self.itens_carrinho:
            self.itens_carrinho[codigo]["quantidade"] += quantidade
        else:
            self.itens_carrinho[codigo] = {"produto": produto, "quantidade": quantidade}

        # Resetar quantidade
        self.quantidade_var.set("1")
       
        # Atualizar interface
        self.atualizar_carrinho()
        self.atualizar_totais()
       
        # Feedback
        messagebox.showinfo("Sucesso", f"Produto adicionado ao carrinho!\nQuantidade: {quantidade}")

    def atualizar_carrinho(self):
        """Atualiza a exibição do carrinho"""
        for widget in self.carrinho.winfo_children():
            widget.destroy()

        cores = colors.get_colors()
       
        if not self.itens_carrinho:
            ctk.CTkLabel(
                self.carrinho, text="Carrinho vazio",
                text_color=cores["TEXT_SECONDARY"], font=ctk.CTkFont(size=12),
                justify="center"
            ).pack(expand=True, pady=50)
            return

        self.btns_carrinho.clear()

        for codigo, dados in self.itens_carrinho.items():
            self.criar_linha_carrinho(codigo, dados, cores)

    def criar_linha_carrinho(self, codigo, dados, cores):
        """Cria uma linha de item no carrinho"""
        produto = dados["produto"]
        quantidade = dados["quantidade"]
       
        preco_unitario = Decimal(str(produto.get("preco", 0)))
        preco_total = (preco_unitario * Decimal(quantidade)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        # Frame da linha
        linha = ctk.CTkFrame(self.carrinho, fg_color=cores["CARD_BG"], corner_radius=6, height=45)
        linha.pack(fill="x", pady=2, padx=2)
        linha.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Produto
        lbl_produto = ctk.CTkLabel(
            linha, text=produto["nome"], anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        lbl_produto.grid(row=0, column=0, padx=10, sticky="w")

        # Quantidade
        lbl_qtd = ctk.CTkLabel(
            linha, text=str(quantidade), anchor="center",
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        lbl_qtd.grid(row=0, column=1, padx=10)

        # Unitário
        lbl_unit = ctk.CTkLabel(
            linha, text=f"R$ {preco_unitario:.2f}", anchor="e",
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        lbl_unit.grid(row=0, column=2, padx=10, sticky="e")

        # Total
        lbl_total = ctk.CTkLabel(
            linha, text=f"R$ {preco_total:.2f}", anchor="e",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#10B981"  # Verde para valores totais
        )
        lbl_total.grid(row=0, column=3, padx=10, sticky="e")

        # Vincular seleção
        linha.bind("<Button-1>", lambda e, c=codigo: self.selecionar_produto_direita_carrinho(c))
        for widget in linha.winfo_children():
            widget.bind("<Button-1>", lambda e, c=codigo: self.selecionar_produto_direita_carrinho(c))

        self.btns_carrinho[codigo] = linha

    def selecionar_produto_direita_carrinho(self, codigo):
        if codigo not in self.itens_carrinho:
            return

        produto = self.itens_carrinho[codigo]["produto"]
        self.produto_selecionado_dir = produto
        self.produto_selecionado_esq = produto  # <-- faz a esquerda atualizar

        cores = colors.get_colors()

        # Desselecionar todas as linhas do carrinho
        for linha in self.btns_carrinho.values():
            linha.configure(fg_color=cores["CARD_BG"])
            for widget in linha.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color=cores["TEXT_PRIMARY"])

        # Selecionar a linha clicada
        linha = self.btns_carrinho[codigo]
        linha.configure(fg_color=cores["PRIMARY"])
        for widget in linha.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color="white")

        # Atualizar imagem e informações na esquerda
        self.atualizar_imagem(produto)
        self.atualizar_info_produto()

    def remover_produto_selecionado_direita(self):
        if not self.produto_selecionado_dir:
            messagebox.showwarning("Aviso", "Selecione um item no carrinho para remover.")
            return

        # Encontrar código
        codigo = None
        for c, dados in self.itens_carrinho.items():
            if dados["produto"] == self.produto_selecionado_dir:
                codigo = c
                break

        if not codigo:
            return

        # Confirmar remoção
        if messagebox.askyesno("Confirmar", "Remover este item do carrinho?"):
            del self.itens_carrinho[codigo]
            if codigo in self.btns_carrinho:
                del self.btns_carrinho[codigo]

            # Resetar seleções
            self.produto_selecionado_dir = None
            self.produto_selecionado_esq = None  # <-- limpa a esquerda
            self.atualizar_carrinho()
            self.atualizar_totais()
            self.atualizar_imagem(None)
            self.atualizar_info_produto()  # <-- atualiza labels para nulo

    # ==================== TOTAIS ====================
    def atualizar_totais(self):
        """Calcula e atualiza os totais da venda"""
        subtotal = Decimal("0.00")
        total_itens = 0
       
        for dados in self.itens_carrinho.values():
            preco = Decimal(str(dados["produto"].get("preco", 0)))
            quantidade = dados["quantidade"]
            subtotal += preco * Decimal(quantidade)
            total_itens += quantidade
       
        subtotal = subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        desconto = Decimal("0.00")
        acrescimo = Decimal("0.00")
        total = (subtotal - desconto + acrescimo).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        self.lbl_itens.configure(text=f"Itens: {total_itens}")
        self.lbl_sub.configure(text=f"Subtotal: R$ {subtotal:.2f}")
        self.lbl_desconto.configure(text=f"Desconto: R$ {desconto:.2f}")
        self.lbl_acrescimo.configure(text=f"Acréscimo: R$ {acrescimo:.2f}")
        self.lbl_total.configure(text=f"TOTAL: R$ {total:.2f}")

# ================= FUNÇÃO PARA MOSTRAR CAIXA =================
def mostrar_menu(app):
    """Função principal para exibir a tela do caixa"""
    CaixaApp(app)