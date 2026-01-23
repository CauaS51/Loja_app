import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import data.colors as colors
import data.sessao as sessao
import crud.crud_produtos as produtos_crud
from decimal import Decimal, ROUND_HALF_UP
import tkinter as tk

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

        # Usar apenas StringVar para quantidade
        self.quantidade_var = ctk.StringVar(value="1")

        self.criar_tela()
        self.carregar_produtos()

    # ==================== CRIAÇÃO DA TELA ====================
    def criar_tela(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Caixa | PDV")
        cores = colors.get_colors()

        # HEADER
        self.criar_header()

        # BODY
        body = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"])
        body.pack(fill="both", expand=True, padx=10, pady=10)
        body.grid_columnconfigure((0, 1), weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.criar_coluna_esquerda(body)
        self.criar_coluna_direita(body)

    # ==================== HEADER ====================
    def criar_header(self):
        cores = colors.get_colors()
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80)
        header.pack(fill="x")

        def voltar():
            from data import menu
            menu.mostrar_menu(self.app, sessao.usuario, sessao.perfil)

        ctk.CTkButton(
            header, text="⬅", width=40, height=40, corner_radius=12,
            fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"], font=ctk.CTkFont(family="Segoe UI", size=20),
            command=voltar
        ).pack(side="left", padx=20, pady=20)

        ctk.CTkLabel(
            header, text="🛒 Caixa",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=10)

        def alternar_tema():
            colors.alternar_tema()
            self.criar_tela()
            self.carregar_produtos()
            self.atualizar_carrinho()
            self.atualizar_totais()

        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        ctk.CTkButton(
            header, text=icone_tema, width=40, height=40, corner_radius=12,
            fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"], font=ctk.CTkFont(family="Segoe UI", size=22),
            command=alternar_tema
        ).pack(side="right", padx=20, pady=20)

    # ==================== COLUNA ESQUERDA ====================
    def criar_coluna_esquerda(self, parent):
        cores = colors.get_colors()
        left = ctk.CTkFrame(parent, fg_color=cores["BACKGROUND"])
        left.grid(row=0, column=0, sticky="nsew", padx=10)

        self.frame_produto = ctk.CTkFrame(left, fg_color="transparent")
        self.frame_produto.pack(fill="x", pady=(0, 15))

        self.img_label = ctk.CTkLabel(
            self.frame_produto, text="🖼 Imagem do Produto", width=200, height=300,
            fg_color=cores["CARD_BG"], corner_radius=12
        )
        self.img_label.pack(side="left", padx=(0, 15), pady=5)

        self.frame_info = ctk.CTkFrame(self.frame_produto, fg_color="transparent")
        self.frame_info.pack(side="left", fill="both", expand=True, pady=5)

        font_name = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        font_label = ctk.CTkFont(family="Segoe UI", size=14)
        font_valor = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")

        self.lbl_nome = ctk.CTkLabel(self.frame_info, text="Nome: -", anchor="w", font=font_name)
        self.lbl_nome.pack(fill="x", pady=3)
        self.lbl_codigo = ctk.CTkLabel(self.frame_info, text="Código: -", anchor="w", font=font_label)
        self.lbl_codigo.pack(fill="x", pady=3)
        self.lbl_categoria = ctk.CTkLabel(self.frame_info, text="Categoria: -", anchor="w", font=font_label)
        self.lbl_categoria.pack(fill="x", pady=3)
        self.lbl_preco_unit = ctk.CTkLabel(self.frame_info, text="Preço Unit.: R$ 0,00", anchor="w", font=font_label)
        self.lbl_preco_unit.pack(fill="x", pady=3)
        self.lbl_preco_total = ctk.CTkLabel(
            self.frame_info, text="Preço Total: R$ 0,00",
            anchor="w", font=font_valor, text_color=cores["PRIMARY"]
        )
        self.lbl_preco_total.pack(fill="x", pady=5)

        ctk.CTkLabel(self.frame_info, text="Quantidade:", font=ctk.CTkFont(family="Segoe UI", size=14)).pack(anchor="w", pady=(5, 0))

        self.quantidade_entry = ctk.CTkEntry(
            self.frame_info, textvariable=self.quantidade_var,
            width=60, font=ctk.CTkFont(family="Segoe UI", size=14)
        )
        self.quantidade_entry.pack(anchor="w", pady=(0, 5))

        # Atualiza info de produto enquanto digita, sem bloquear apagar
        self.quantidade_var.trace_add("write", lambda *args: self.atualizar_info_produto())

        self.btn_adicionar = ctk.CTkButton(self.frame_info, text="Adicionar ao Carrinho", command=self.adicionar_carrinho,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        )
        self.btn_adicionar.pack(pady=10, anchor="w")

        self.search = ctk.CTkEntry(
            left, placeholder_text="🔍 Buscar produto por nome ou código", height=40,
            font=ctk.CTkFont(family="Segoe UI", size=14)
        )
        self.search.pack(fill="x", pady=(10, 5))
        self.search.bind("<KeyRelease>", self.filtrar_produtos)

        self.lista_produtos = ctk.CTkScrollableFrame(left, height=300)
        self.lista_produtos.pack(fill="x", pady=5)

    # ==================== COLUNA DIREITA ====================
    def criar_coluna_direita(self, parent):
        cores = colors.get_colors()
        right = ctk.CTkFrame(parent, fg_color=cores["BACKGROUND"])
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        right.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            right, text="🧾 ITENS DO CARRINHO",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        ).pack(pady=(0, 10))

        # ===== HEADER DA TABELA =====
        header = ctk.CTkFrame(right, fg_color="transparent")
        header.pack(fill="x", padx=5)
        
        COL_PRODUTO = 260
        COL_QTD = 60
        COL_UNIT = 100
        COL_TOTAL = 100

        header.grid_columnconfigure(0, minsize=COL_PRODUTO)
        header.grid_columnconfigure(1, minsize=COL_QTD)
        header.grid_columnconfigure(2, minsize=COL_UNIT)
        header.grid_columnconfigure(3, minsize=COL_TOTAL)

        ctk.CTkLabel(header, text="Produto", anchor="w").grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header, text="Qtd", anchor="e").grid(row=0, column=1, sticky="e", padx=5)
        ctk.CTkLabel(header, text="Unitário", anchor="e").grid(row=0, column=2, sticky="e", padx=5)
        ctk.CTkLabel(header, text="Total", anchor="e").grid(row=0, column=3, sticky="e", padx=5)

        # ===== LISTA DO CARRINHO =====
        self.carrinho = ctk.CTkScrollableFrame(right)
        self.carrinho.pack(fill="both", expand=True, pady=5)

        self.btn_remover_direita = ctk.CTkButton(
            right, text="🗑 Remover Selecionado",
            fg_color="#FF4B4B", hover_color="#FF1A1A",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self.remover_produto_selecionado_direita
        )
        self.btn_remover_direita.pack(pady=5)

        # ===== RESUMO =====
        resumo = ctk.CTkFrame(right, fg_color=cores["ENTRY_BG"])
        resumo.pack(fill="x", pady=10)

        self.lbl_itens = ctk.CTkLabel(resumo, text="Itens: 0")
        self.lbl_itens.pack(anchor="w", padx=10)

        self.lbl_sub = ctk.CTkLabel(resumo, text="Subtotal: R$ 0,00")
        self.lbl_sub.pack(anchor="w", padx=10)

        self.lbl_desconto = ctk.CTkLabel(resumo, text="Desconto: R$ 0,00")
        self.lbl_desconto.pack(anchor="w", padx=10)

        self.lbl_acrescimo = ctk.CTkLabel(resumo, text="Acréscimo: R$ 0,00")
        self.lbl_acrescimo.pack(anchor="w", padx=10)

        self.lbl_total = ctk.CTkLabel(
            resumo, text="TOTAL: R$ 0,00",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=cores["PRIMARY"]
        )
        self.lbl_total.pack(anchor="e", padx=10, pady=10)

    # ===== BOTÃO FINALIZAR =====
        self.btn_finalizar = ctk.CTkButton(
        right,
        text="💳 FINALIZAR VENDA",
        font=ctk.CTkFont(size=16, weight="bold"),
        height=45,
        fg_color=cores["PRIMARY"],
        # command=self.abrir_pagamento
    )
        self.btn_finalizar.pack(fill="x", padx=10, pady=10)

    # ==================== CARREGAR PRODUTOS ====================
    def carregar_produtos(self):
        self.produtos = produtos_crud.listar_produtos()
        self.exibir_lista_produtos(self.produtos)

    def exibir_lista_produtos(self, produtos):
        for w in self.lista_produtos.winfo_children():
            w.destroy()
        cores = colors.get_colors()
        self.btns_produtos.clear()
        for p in produtos:
            btn = ctk.CTkButton(
                self.lista_produtos,
                text=f"{p['nome']} | R$ {Decimal(str(p['preco'])):.2f}",
                text_color=cores["TEXT_PRIMARY"],
                fg_color=cores["CARD_BG"],
                hover_color=cores["HOVER"],
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                command=lambda prod=p: self.selecionar_produto_esquerda(prod)
            )
            btn.pack(fill="x", pady=4)
            self.btns_produtos[p["nome"]] = btn

    # ==================== FILTRAR PRODUTOS ====================
    def filtrar_produtos(self, event=None):
        termo = self.search.get().lower()
        filtrados = [p for p in self.produtos if termo in p["nome"].lower() or termo in str(p.get("codigo", "")).lower()]
        self.exibir_lista_produtos(filtrados)

    # ==================== SELEÇÃO DE PRODUTOS ====================
    def selecionar_produto_esquerda(self, produto):
        self.produto_selecionado_esq = produto
        for btn in self.btns_produtos.values():
            btn.configure(fg_color=colors.get_colors()["CARD_BG"], text_color=colors.get_colors()["TEXT_PRIMARY"])
        self.btns_produtos[produto["nome"]].configure(fg_color=colors.get_colors()["PRIMARY"], text_color="white")
        self.atualizar_imagem(produto)
        self.atualizar_info_produto()

    def selecionar_produto_direita(self, produto):
        self.produto_selecionado_dir = produto
        for btn in self.btns_carrinho.values():
            btn.configure(fg_color=colors.get_colors()["CARD_BG"], text_color=colors.get_colors()["TEXT_PRIMARY"])
        codigo = produto.get("codigo")
        if codigo in self.btns_carrinho:
            self.btns_carrinho[codigo].configure(fg_color=colors.get_colors()["PRIMARY"], text_color="white")
        self.atualizar_imagem(produto)

    # ==================== ATUALIZAR IMAGEM ====================
    def atualizar_imagem(self, produto):
        try:
            img = Image.open(produto["img"])
            img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 300))
            self.img_label.configure(image=img_ctk, text="")
            self.img_label.image = img_ctk
        except Exception as e:
            print(f"Erro ao carregar imagem {produto.get('img')}: {e}")
            img = Image.new("RGB", (200, 300), color="gray")
            img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 300))
            self.img_label.configure(image=img_ctk, text="")
            self.img_label.image = img_ctk

    # ==================== QUANTIDADE ====================
    def get_quantidade(self):
        try:
            qtd = int(self.quantidade_var.get())
            if qtd < 1:
                qtd = 1
        except (ValueError, tk.TclError):
            qtd = 1
        self.quantidade_var.set("" if self.quantidade_var.get() == "" else str(qtd))
        return qtd

    # ==================== ATUALIZAR INFORMAÇÕES ====================
    def atualizar_info_produto(self):
        if not self.produto_selecionado_esq:
            self.lbl_nome.configure(text="Nome: -")
            self.lbl_codigo.configure(text="Código: -")
            self.lbl_categoria.configure(text="Categoria: -")
            self.lbl_preco_unit.configure(text="Preço Unit.: R$ 0,00")
            self.lbl_preco_total.configure(text="Preço Total: R$ 0,00")
            return

        produto = self.produto_selecionado_esq
        qtd = self.get_quantidade()

        preco_unitario = Decimal(str(produto["preco"]))
        preco_total = (preco_unitario * Decimal(qtd)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        self.lbl_nome.configure(text=f"Nome: {produto.get('nome', '-')}")
        self.lbl_codigo.configure(text=f"Código: {produto.get('codigo', '-')}")
        self.lbl_categoria.configure(text=f"Categoria: {produto.get('categoria', '-')}")
        self.lbl_preco_unit.configure(text=f"Preço Unit.: R$ {preco_unitario:.2f}")
        self.lbl_preco_total.configure(text=f"Preço Total: R$ {preco_total:.2f}")

    # ==================== CARRINHO ====================
    def adicionar_carrinho(self):
        if not self.produto_selecionado_esq:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return

        produto = self.produto_selecionado_esq
        # Usar ID único do produto; se não tiver, gerar um hash do nome + preço
        codigo = produto.get("codigo") or f"{produto['nome']}_{produto['preco']}"
        quantidade = self.get_quantidade()

        if codigo in self.itens_carrinho:
            self.itens_carrinho[codigo]["quantidade"] += quantidade
        else:
            self.itens_carrinho[codigo] = {"produto": produto, "quantidade": quantidade}

        self.atualizar_carrinho()
        self.atualizar_totais()

    def atualizar_carrinho(self):
        for w in self.carrinho.winfo_children():
            w.destroy()

        cores = colors.get_colors()
        self.btns_carrinho.clear()

        for codigo, dados in self.itens_carrinho.items():
            produto = dados["produto"]
            quantidade = dados["quantidade"]

            preco_unitario = Decimal(str(produto["preco"]))
            preco_total = (preco_unitario * Decimal(quantidade)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            linha = ctk.CTkFrame(self.carrinho, fg_color=cores["CARD_BG"], corner_radius=8)
            linha.pack(fill="x", pady=2, padx=2)

            COL_PRODUTO = 260
            COL_QTD = 60
            COL_UNIT = 100
            COL_TOTAL = 100

            linha.grid_columnconfigure(0, minsize=COL_PRODUTO)
            linha.grid_columnconfigure(1, minsize=COL_QTD)
            linha.grid_columnconfigure(2, minsize=COL_UNIT)
            linha.grid_columnconfigure(3, minsize=COL_TOTAL)


            ctk.CTkLabel(linha, text=produto["nome"], anchor="w").grid(
                row=0, column=0, sticky="w", padx=5
            )
            ctk.CTkLabel(linha, text=str(quantidade), anchor="e").grid(
                row=0, column=1, sticky="e", padx=5
            )
            ctk.CTkLabel(linha, text=f"R$ {preco_unitario:.2f}", anchor="e").grid(
                row=0, column=2, sticky="e", padx=5
            )
            ctk.CTkLabel(linha, text=f"R$ {preco_total:.2f}", anchor="e").grid(
                row=0, column=3, sticky="e", padx=5
            )

            linha.bind("<Button-1>", lambda e, c=codigo: self.selecionar_produto_direita_carrinho(c))
            for widget in linha.winfo_children():
                widget.bind("<Button-1>", lambda e, c=codigo: self.selecionar_produto_direita_carrinho(c))

            self.btns_carrinho[codigo] = linha


    def selecionar_produto_direita_carrinho(self, codigo):
        if codigo not in self.itens_carrinho:
            return

        self.produto_selecionado_dir = self.itens_carrinho[codigo]["produto"]
        cores = colors.get_colors()

        # Resetar todas as linhas
        for linha in self.btns_carrinho.values():
            linha.configure(fg_color=cores["CARD_BG"])
            for widget in linha.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color=cores["TEXT_PRIMARY"])

        # Destacar linha selecionada
        linha_selecionada = self.btns_carrinho[codigo]
        linha_selecionada.configure(fg_color=cores["PRIMARY"])

        for widget in linha_selecionada.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color="white")

        self.atualizar_imagem(self.produto_selecionado_dir)


    def remover_produto_selecionado_direita(self):
        if not self.produto_selecionado_dir:
            return
        # Encontrar o código do produto selecionado no carrinho
        codigo = None
        for c, dados in self.itens_carrinho.items():
            if dados["produto"] == self.produto_selecionado_dir:
                codigo = c
                break
        if codigo:
            del self.itens_carrinho[codigo]

        self.produto_selecionado_dir = None
        self.atualizar_carrinho()
        self.atualizar_totais()

        # Substituir por imagem padrão em vez de None
        from PIL import Image
        cores = colors.get_colors()
        placeholder_img = Image.new("RGB", (200, 300), color="gray")
        placeholder_ctk = ctk.CTkImage(light_image=placeholder_img, dark_image=placeholder_img, size=(200, 300))
        self.img_label.configure(image=placeholder_ctk, text="🖼 Imagem do Produto")
        self.img_label.image = placeholder_ctk

    # ==================== TOTAL ====================
    def atualizar_totais(self):
        subtotal = sum(
            Decimal(str(dados["produto"]["preco"])) * Decimal(dados["quantidade"]) 
            for dados in self.itens_carrinho.values()
        )
        # Garantir que subtotal seja Decimal mesmo se estiver vazio
        subtotal = Decimal(subtotal).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        desconto = Decimal("0.00")
        acrescimo = (subtotal * Decimal("0.0")).quantize(Decimal("0.0"), rounding=ROUND_HALF_UP)
        total = (subtotal - desconto + acrescimo).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        self.lbl_itens.configure(text=f"Itens: {sum(dados['quantidade'] for dados in self.itens_carrinho.values())}")
        self.lbl_sub.configure(text=f"Subtotal: R$ {subtotal:.2f}")
        self.lbl_desconto.configure(text=f"Desconto: R$ {desconto:.2f}")
        self.lbl_acrescimo.configure(text=f"Acréscimo: R$ {acrescimo:.2f}")
        self.lbl_total.configure(text=f"TOTAL: R$ {total:.2f}")


# ================= FUNÇÃO PARA MOSTRAR CAIXA =================
def mostrar_menu(app):
    CaixaApp(app)
