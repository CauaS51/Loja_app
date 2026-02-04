import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageOps
import io  # Necessário para converter bytes
import os
import data.colors as colors
import data.sessao as sessao
import crud.crud_produtos as produtos_crud
from decimal import Decimal, ROUND_HALF_UP
import tkinter as tk
from crud.crud_relatorios import salvar_venda_completa

class CaixaApp:
    def __init__(self, app):
        self.app = app
        self.app.bind("<Key>", self.focar_busca_automatico)
        self.produto_selecionado_esq = None
        self.produto_selecionado_dir = None
        self.itens_carrinho = {}
        self.btns_produtos = {}
        self.btns_carrinho = {}
        self.img_label = None
        self.produtos = []
        self.current_image = None
        self.quantidade_var = ctk.StringVar(value="1")

        self.criar_tela()
        self.carregar_produtos()

    def focar_busca_automatico(self, event):
        if not isinstance(self.app.focus_get(), ctk.CTkEntry):
            self.search.focus()
    
    def criar_tela(self):
        try:
            for widget in self.app.winfo_children():
                widget.destroy()

            self.app.title("Sistema PDV - Caixa")
            self.app.geometry("1300x750")
            
            self.app.grid_columnconfigure(0, weight=1)
            self.app.grid_rowconfigure(0, weight=1)

            self.criar_header()
            self.criar_body()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar interface: {str(e)}")
            raise

    def criar_header(self):
        cores = colors.get_colors()

        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False) # Mantém a altura fixa de 80

        # Botão Voltar
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"],
            fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.voltar_menu
        )
        btn_voltar.pack(side="left", padx=20, pady=20)

        # --- NOVO CONTAINER PARA LOGO E TÍTULO ---
        header_title_frame = ctk.CTkFrame(header, fg_color="transparent")
        header_title_frame.pack(side="left", pady=15)

        # Lógica da Logo
        img_data = getattr(sessao, 'logo_path', None)
        logo_carregada = False

        if img_data:
            try:
                if isinstance(img_data, bytes):
                    img_pil = Image.open(io.BytesIO(img_data))
                elif isinstance(img_data, str) and os.path.exists(img_data):
                    img_pil = Image.open(img_data)
                else:
                    img_pil = None

                if img_pil:
                    img_fit = ImageOps.fit(img_pil, (80, 80), Image.Resampling.LANCZOS)
                    logo_img = ctk.CTkImage(light_image=img_fit, dark_image=img_fit, size=(80, 80))
                    ctk.CTkLabel(header_title_frame, image=logo_img, text="").pack(side="left", padx=(0, 10))
                    logo_carregada = True
            except Exception as e:
                print(f"Erro ao carregar logo no cabeçalho: {e}")

        # Texto do Título (Ícone 🛒 só aparece se a logo falhar)
        icone_prefixo = "" if logo_carregada else "🛒 "
        ctk.CTkLabel(
            header_title_frame, text=f"{icone_prefixo}Caixa · PDV", text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        ).pack(side="left")

        # Container Direita (Operador e Tema)
        right_container = ctk.CTkFrame(header, fg_color="transparent")
        right_container.pack(side="right", padx=20, pady=20)

        ctk.CTkLabel(
            right_container, text=f"Operador: {sessao.nome}", fg_color='white',
            corner_radius=10, height=36, padx=12,
            font=ctk.CTkFont("Segoe UI", 15, "bold"), text_color=cores["SECONDARY"]
        ).pack(side="left", padx=(0, 8))

        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        ctk.CTkButton(
            right_container, text=icone_tema, width=40, height=40, corner_radius=12,
            fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"], font=ctk.CTkFont(size=25),
            command=self.alternar_tema
        ).pack(side="left")

    def criar_body(self):
        cores = colors.get_colors()
        body = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"])
        body.pack(fill="both", expand=True, padx=10, pady=5)
        body.grid_columnconfigure((0, 1), weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.criar_coluna_esquerda(body, cores)
        self.criar_coluna_direita(body, cores)

    # ==================== COLUNA ESQUERDA ====================
    def criar_coluna_esquerda(self, parent, cores):
        left = ctk.CTkFrame(parent, fg_color=cores["BACKGROUND"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        self.criar_frame_detalhes_produto(left, cores)

        self.search = ctk.CTkEntry(
            left, placeholder_text="🔍 Buscar produto por nome ou código...",
            height=40, font=ctk.CTkFont(family="Segoe UI", size=13),
            border_width=1, corner_radius=8
        )
        self.search.pack(fill="x", pady=(0, 10))
        
        self.search.bind("<KeyRelease>", lambda e: self.filtrar_produtos())
        self.search.bind("<Return>", lambda e: self.processar_leitor())

        self.lista_produtos = ctk.CTkScrollableFrame(left, fg_color=cores["BACKGROUND"])
        self.lista_produtos.pack(fill="both", expand=True)

    def criar_frame_detalhes_produto(self, parent, cores):
        frame_detalhes = ctk.CTkFrame(parent, fg_color=cores["CARD_BG"], corner_radius=10)
        frame_detalhes.pack(fill="x", pady=(0, 15))

        self.img_label = ctk.CTkLabel(
            frame_detalhes, text="🖼️", width=220, height=300, corner_radius=8,
            fg_color=cores["ENTRY_BG"], text_color=cores["TEXT_SECONDARY"],
            font=ctk.CTkFont(size=40), anchor="center"
        )
        self.img_label.pack(side="left", padx=15, pady=15)

        frame_info = ctk.CTkFrame(frame_detalhes, fg_color="transparent")
        frame_info.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        self.lbl_nome = ctk.CTkLabel(
            frame_info, text="SELECIONE UM PRODUTO", anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color=cores["TEXT_PRIMARY"]
        )
        self.lbl_nome.pack(fill="x", pady=(0, 10))

        self.lbl_codigo = ctk.CTkLabel(frame_info, text="Código: ---", anchor="w", font=ctk.CTkFont(family="Segoe UI", size=13))
        self.lbl_codigo.pack(fill="x", pady=2)
        
        self.lbl_categoria = ctk.CTkLabel(frame_info, text="Categoria: ---", anchor="w", font=ctk.CTkFont(family="Segoe UI", size=13))
        self.lbl_categoria.pack(fill="x", pady=2)
        
        self.lbl_preco_unit = ctk.CTkLabel(frame_info, text="Preço Unitário: R$ 0,00", anchor="w", font=ctk.CTkFont(family="Segoe UI", size=13))
        self.lbl_preco_unit.pack(fill="x", pady=2)

        separator_color = "#E0E0E0" if ctk.get_appearance_mode() == "Light" else "#444444"
        ctk.CTkFrame(frame_info, height=1, fg_color=separator_color).pack(fill="x", pady=15)

        frame_qtd = ctk.CTkFrame(frame_info, fg_color="transparent")
        frame_qtd.pack(fill="x", pady=5)

        ctk.CTkLabel(frame_qtd, text="Quantidade:", font=ctk.CTkFont(family="Segoe UI", size=13)).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            frame_qtd, text="−", width=30, height=30, command=self.diminuir_quantidade,
            font=ctk.CTkFont(size=14, weight="bold"), fg_color="#6B7280", hover_color="#4B5563"
        ).pack(side="left", padx=2)

        self.quantidade_entry = ctk.CTkEntry(
            frame_qtd, textvariable=self.quantidade_var, width=60, 
            font=ctk.CTkFont(family="Segoe UI", size=13), justify="center"
        )
        self.quantidade_entry.pack(side="left", padx=2)

        ctk.CTkButton(
            frame_qtd, text="+", width=30, height=30, command=self.aumentar_quantidade,
            font=ctk.CTkFont(size=14, weight="bold"), fg_color="#6B7280", hover_color="#4B5563"
        ).pack(side="left", padx=2)

        self.lbl_preco_total = ctk.CTkLabel(
            frame_info, text="Total: R$ 0,00", anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color="#10B981"
        )
        self.lbl_preco_total.pack(fill="x", pady=(15, 10))

        self.btn_adicionar = ctk.CTkButton(
            frame_info, text="➕ ADICIONAR AO CARRINHO", height=40,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#10B981", hover_color="#059669", command=self.adicionar_carrinho
        )
        self.btn_adicionar.pack(fill="x", pady=(5, 0))

        self.quantidade_var.trace_add("write", lambda *args: self.atualizar_info_produto())

    # ==================== COLUNA DIREITA ====================
    def criar_coluna_direita(self, parent, cores):
        right = ctk.CTkFrame(parent, fg_color=cores["BACKGROUND"])
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)

        lbl_titulo_carrinho = ctk.CTkLabel(
            right, text="🧾 CARRINHO DE COMPRAS",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        )
        lbl_titulo_carrinho.pack(anchor="w", pady=(0, 10))

        self.criar_cabecalho_carrinho(right, cores)

        self.carrinho = ctk.CTkScrollableFrame(right, fg_color=cores["BACKGROUND"])
        self.carrinho.pack(fill="both", expand=True, pady=(0, 10))

        self.btn_remover_direita = ctk.CTkButton(
            right, text="🗑️ REMOVER ITEM SELECIONADO", height=35,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="#DC3545", hover_color="#C82333",
            command=self.remover_produto_selecionado_direita
        )
        self.btn_remover_direita.pack(fill="x", pady=(0, 15))

        self.criar_resumo_compra(right, cores)

        self.btn_finalizar = ctk.CTkButton(
            right, text="💳 FINALIZAR VENDA", height=45,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=cores["PRIMARY"], hover_color=cores["HOVER"],
            command=self.finalizar_venda
        )
        self.btn_finalizar.pack(fill="x")

    def criar_cabecalho_carrinho(self, parent, cores):
        header = ctk.CTkFrame(parent, fg_color=cores["CARD_BG"], height=35, corner_radius=6)
        header.pack(fill="x")
        header.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(header, text="PRODUTO", anchor="w", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")).grid(row=0, column=0, padx=10, sticky="w")
        ctk.CTkLabel(header, text="QTD", anchor="center", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")).grid(row=0, column=1, padx=10)
        ctk.CTkLabel(header, text="UNITÁRIO", anchor="e", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")).grid(row=0, column=2, padx=10, sticky="e")
        ctk.CTkLabel(header, text="TOTAL", anchor="e", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")).grid(row=0, column=3, padx=10, sticky="e")

    def criar_resumo_compra(self, parent, cores):
        resumo = ctk.CTkFrame(parent, fg_color=cores["CARD_BG"], corner_radius=8)
        resumo.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(resumo, text="RESUMO DA COMPRA", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).pack(pady=(10, 15))

        frame_itens = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_itens.pack(fill="x", padx=15, pady=2)
        self.lbl_itens = ctk.CTkLabel(frame_itens, text="Itens: 0", font=ctk.CTkFont(family="Segoe UI", size=12))
        self.lbl_itens.pack(anchor="w")

        frame_sub = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_sub.pack(fill="x", padx=15, pady=2)
        self.lbl_sub = ctk.CTkLabel(frame_sub, text="Subtotal: R$ 0,00", font=ctk.CTkFont(family="Segoe UI", size=12))
        self.lbl_sub.pack(anchor="w")

        frame_desc = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_desc.pack(fill="x", padx=15, pady=2)
        self.lbl_desconto = ctk.CTkLabel(frame_desc, text="Desconto: R$ 0,00", font=ctk.CTkFont(family="Segoe UI", size=12))
        self.lbl_desconto.pack(anchor="w")

        frame_acres = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_acres.pack(fill="x", padx=15, pady=2)
        self.lbl_acrescimo = ctk.CTkLabel(frame_acres, text="Acréscimo: R$ 0,00", font=ctk.CTkFont(family="Segoe UI", size=12))
        self.lbl_acrescimo.pack(anchor="w")

        separator_color = "#E0E0E0" if ctk.get_appearance_mode() == "Light" else "#444444"
        ctk.CTkFrame(resumo, height=1, fg_color=separator_color).pack(fill="x", padx=15, pady=10)

        frame_total = ctk.CTkFrame(resumo, fg_color="transparent")
        frame_total.pack(fill="x", padx=15, pady=(0, 15))
        self.lbl_total = ctk.CTkLabel(frame_total, text="TOTAL: R$ 0,00", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color=cores["PRIMARY"])
        self.lbl_total.pack(anchor="e")

    def finalizar_venda(self):
        if not self.itens_carrinho:
            messagebox.showwarning("Aviso", "O carrinho está vazio!")
            return

        subtotal = Decimal("0.00")
        for dados in self.itens_carrinho.values():
            preco = Decimal(str(dados["produto"].get("preco", 0)))
            subtotal += preco * Decimal(dados["quantidade"])
        
        total_final = subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        import data.pagamento as pgto
        pgto.abrir_pagamento(
            app=self.app, 
            total=total_final, 
            itens=self.itens_carrinho, 
            callback=self.concluir_venda_com_estoque 
        )

    def concluir_venda_com_estoque(self, forma_pagamento="Dinheiro"):
        try:
            total_venda = sum(float(d["produto"]["preco"]) * d["quantidade"] for d in self.itens_carrinho.values())
            sucesso = salvar_venda_completa(
                total=total_venda,
                forma_pagamento=forma_pagamento,
                itens_carrinho=self.itens_carrinho,          
            )

            if sucesso:
                messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
                self.resetar_carrinho()
                self.carregar_produtos() 
            else:
                messagebox.showerror("Erro", "Erro ao gravar a venda no banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha crítica na conclusão: {e}")

    def resetar_carrinho(self):
        self.itens_carrinho = {}
        self.produto_selecionado_esq = None
        self.produto_selecionado_dir = None
        self.quantidade_var.set("1")
        self.atualizar_carrinho()
        self.atualizar_totais()
        self.atualizar_info_produto()
        if self.img_label:
            self.img_label.configure(image="", text="🖼️")
        cores = colors.get_colors()
        for btn in self.btns_produtos.values():
            btn.configure(fg_color=cores["CARD_BG"], text_color=cores["TEXT_PRIMARY"])

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
        try:
            qtd = int(self.quantidade_var.get() or "1")
            self.quantidade_var.set(str(qtd + 1))
        except ValueError:
            self.quantidade_var.set("1")

    def diminuir_quantidade(self):
        try:
            qtd = int(self.quantidade_var.get() or "1")
            if qtd > 1:
                self.quantidade_var.set(str(qtd - 1))
        except ValueError:
            self.quantidade_var.set("1")

    def get_quantidade(self):
        try:
            qtd = int(self.quantidade_var.get() or "1")
            return max(1, qtd)
        except (ValueError, tk.TclError):
            return 1

    # ==================== CARREGAR E EXIBIR PRODUTOS ====================
    def carregar_produtos(self):
        try:
            self.produtos = produtos_crud.listar_produtos_por_loja(sessao.loja_id)
            self.exibir_lista_produtos(self.produtos)
            self.search.focus()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")
            self.produtos = []

    def exibir_lista_produtos(self, produtos):
        for widget in self.lista_produtos.winfo_children():
            widget.destroy()
        
        cores = colors.get_colors()
        self.btns_produtos.clear()
        
        if not produtos:
            ctk.CTkLabel(self.lista_produtos, text="Nenhum produto encontrado", text_color=cores["TEXT_SECONDARY"], font=ctk.CTkFont(size=12)).pack(pady=20)
            return
        
        for produto in produtos:
            self.criar_botao_produto(produto, cores)

    def criar_botao_produto(self, produto, cores):
        texto = f"{produto['nome']} | R$ {Decimal(str(produto['preco'])):.2f}"
        btn = ctk.CTkButton(
            self.lista_produtos, text=texto, text_color=cores["TEXT_PRIMARY"], fg_color=cores["CARD_BG"],
            hover_color=cores["HOVER"], anchor="w", height=40,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            command=lambda p=produto: self.selecionar_produto_esquerda(p)
        )
        btn.pack(fill="x", pady=2, padx=2)
        self.btns_produtos[produto["nome"]] = btn

    # ==================== FILTRAR E PROCESSAR LEITOR ====================
    def filtrar_produtos(self):
        termo = self.search.get().lower().strip()
        if not termo:
            self.exibir_lista_produtos(self.produtos)
            return
        
        filtrados = [
            p for p in self.produtos
            if termo in p["nome"].lower() or
               termo in str(p.get("codigo", "")).lower() or
               termo in str(p.get("codigo_barras", "")).lower()
        ]
        self.exibir_lista_produtos(filtrados)

    def processar_leitor(self):
        termo = self.search.get().strip()
        if not termo: return

        produto_encontrado = None
        for p in self.produtos:
            if str(p.get("codigo")) == termo or str(p.get("codigo_barras")) == termo:
                produto_encontrado = p
                break
        
        if produto_encontrado:
            self.selecionar_produto_esquerda(produto_encontrado)
            self.adicionar_carrinho()
            self.search.delete(0, 'end')

    # ==================== SELEÇÃO DE PRODUTOS ====================
    def selecionar_produto_esquerda(self, produto):
        self.produto_selecionado_esq = produto
        cores = colors.get_colors()
        
        for btn in self.btns_produtos.values():
            btn.configure(fg_color=cores["CARD_BG"], text_color=cores["TEXT_PRIMARY"])
        
        if produto["nome"] in self.btns_produtos:
            self.btns_produtos[produto["nome"]].configure(fg_color=cores["PRIMARY"], text_color="white")
        
        self.atualizar_imagem(produto)
        self.atualizar_info_produto()

    # ==================== ATUALIZAR IMAGEM (TRATANDO BYTES) ====================
    def atualizar_imagem(self, produto):
        try:
            img_data = produto.get("img") if produto else None

            if img_data and isinstance(img_data, (bytes, bytearray)):
                img_pil = Image.open(io.BytesIO(img_data))
                img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(220, 300))
                self.img_label.configure(image=img_ctk, text="")
                self.img_label.image = img_ctk 
            else:
                self.img_label.configure(image="", text="🖼️", font=ctk.CTkFont(size=40))
        except Exception as e:
            print(f"Erro ao carregar imagem binária: {e}")
            self.img_label.configure(image="", text="🖼️", font=ctk.CTkFont(size=40))

    # ==================== ATUALIZAR INFORMAÇÕES ====================
    def atualizar_info_produto(self):
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
        preco_total = (preco_unitario * Decimal(quantidade)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        self.lbl_nome.configure(text=produto.get('nome', '---'))
        self.lbl_codigo.configure(text=f"Código: {produto.get('codigo', '---')}")
        self.lbl_categoria.configure(text=f"Categoria: {produto.get('categoria', '---')}")
        self.lbl_preco_unit.configure(text=f"Preço Unitário: R$ {preco_unitario:.2f}")
        self.lbl_preco_total.configure(text=f"Total: R$ {preco_total:.2f}")

    # ==================== CARRINHO ====================
    def adicionar_carrinho(self):
        if not self.produto_selecionado_esq:
            messagebox.showwarning("Aviso", "Selecione um produto antes de adicionar.")
            return

        produto = self.produto_selecionado_esq
        codigo = produto.get("codigo")
        qtd_estoque = produto.get("estoque", 0)
        qtd_desejada = self.get_quantidade()

        qtd_no_carrinho = self.itens_carrinho[codigo]["quantidade"] if codigo in self.itens_carrinho else 0

        if (qtd_no_carrinho + qtd_desejada) > qtd_estoque:
            messagebox.showerror("Estoque Insuficiente", f"No estoque: {qtd_estoque}\nJá no carrinho: {qtd_no_carrinho}")
            return

        if codigo in self.itens_carrinho:
            self.itens_carrinho[codigo]["quantidade"] += qtd_desejada
        else:
            self.itens_carrinho[codigo] = {"produto": produto, "quantidade": qtd_desejada}

        self.quantidade_var.set("1")
        self.atualizar_carrinho()
        self.atualizar_totais()

    def atualizar_carrinho(self):
        for widget in self.carrinho.winfo_children():
            widget.destroy()

        cores = colors.get_colors()
        if not self.itens_carrinho:
            ctk.CTkLabel(self.carrinho, text="Carrinho vazio", text_color=cores["TEXT_SECONDARY"], font=ctk.CTkFont(size=12)).pack(expand=True, pady=50)
            return

        self.btns_carrinho.clear()
        for codigo, dados in self.itens_carrinho.items():
            self.criar_linha_carrinho(codigo, dados, cores)

    def criar_linha_carrinho(self, codigo, dados, cores):
        produto = dados["produto"]
        quantidade = dados["quantidade"]
        preco_unitario = Decimal(str(produto.get("preco", 0)))
        preco_total = (preco_unitario * Decimal(quantidade)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        linha = ctk.CTkFrame(self.carrinho, fg_color=cores["CARD_BG"], corner_radius=6, height=45)
        linha.pack(fill="x", pady=2, padx=2)
        linha.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(linha, text=produto["nome"], anchor="w", font=ctk.CTkFont(size=11)).grid(row=0, column=0, padx=10, sticky="w")
        ctk.CTkLabel(linha, text=str(quantidade), anchor="center", font=ctk.CTkFont(size=11)).grid(row=0, column=1, padx=10)
        ctk.CTkLabel(linha, text=f"R$ {preco_unitario:.2f}", anchor="e", font=ctk.CTkFont(size=11)).grid(row=0, column=2, padx=10, sticky="e")
        ctk.CTkLabel(linha, text=f"R$ {preco_total:.2f}", anchor="e", font=ctk.CTkFont(size=11, weight="bold"), text_color="#10B981").grid(row=0, column=3, padx=10, sticky="e")

        linha.bind("<Button-1>", lambda e, c=codigo: self.selecionar_produto_direita_carrinho(c))
        for widget in linha.winfo_children():
            widget.bind("<Button-1>", lambda e, c=codigo: self.selecionar_produto_direita_carrinho(c))
        self.btns_carrinho[codigo] = linha

    def selecionar_produto_direita_carrinho(self, codigo):
        if codigo not in self.itens_carrinho: return
        produto = self.itens_carrinho[codigo]["produto"]
        self.produto_selecionado_dir = produto
        self.produto_selecionado_esq = produto
        cores = colors.get_colors()

        for linha in self.btns_carrinho.values():
            linha.configure(fg_color=cores["CARD_BG"])
            for widget in linha.winfo_children():
                if isinstance(widget, ctk.CTkLabel): widget.configure(text_color=cores["TEXT_PRIMARY"])

        linha = self.btns_carrinho[codigo]
        linha.configure(fg_color=cores["PRIMARY"])
        for widget in linha.winfo_children():
            if isinstance(widget, ctk.CTkLabel): widget.configure(text_color="white")

        self.atualizar_imagem(produto)
        self.atualizar_info_produto()

    def remover_produto_selecionado_direita(self):
        if not self.produto_selecionado_dir:
            messagebox.showwarning("Aviso", "Selecione um item no carrinho para remover.")
            return

        codigo = next((c for c, d in self.itens_carrinho.items() if d["produto"] == self.produto_selecionado_dir), None)
        if codigo and messagebox.askyesno("Confirmar", "Remover este item do carrinho?"):
            del self.itens_carrinho[codigo]
            self.produto_selecionado_dir = None
            self.produto_selecionado_esq = None
            self.atualizar_carrinho()
            self.atualizar_totais()
            self.atualizar_imagem(None)
            self.atualizar_info_produto()

    def atualizar_totais(self):
        subtotal = Decimal("0.00")
        total_itens = 0
        for dados in self.itens_carrinho.values():
            preco = Decimal(str(dados["produto"].get("preco", 0)))
            quantidade = dados["quantidade"]
            subtotal += preco * Decimal(quantidade)
            total_itens += quantidade
        
        subtotal = subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.lbl_itens.configure(text=f"Itens: {total_itens}")
        self.lbl_sub.configure(text=f"Subtotal: R$ {subtotal:.2f}")
        self.lbl_total.configure(text=f"TOTAL: R$ {subtotal:.2f}")

def mostrar_menu(app):
    CaixaApp(app)