import customtkinter as ctk
from tkinter import messagebox
import random
from datetime import datetime

# === CONFIGURAÇÃO GLOBAL ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Variável global de tema
modo_escuro = False

# Dados do usuário (simulando um banco de dados)
dados_usuario = {
    "nome": "Maria Silva Santos",
    "email": "maria.silva@email.com",
    "telefone": "(11) 98765-4321",
    "endereco": "Rua das Flores, 123 - São Paulo/SP"
}

# === CRIAÇÃO DA JANELA PRINCIPAL ===
app = ctk.CTk()
app.geometry("1200x700")
app.minsize(900, 500)
app.title("Sistema de Gerenciamento")

# Dados de exemplo para promoções com produto destaque do mês
def obter_promocao_destaque_mes():
    mes_atual = datetime.now().month
    produtos_destaque = [
        {
            "nome": "🍖 Cesta de Carnes Premium 5kg",
            "preco_original": 189.90,
            "preco_promocional": 129.90,
            "desconto": "32%",
            "descricao": "Contém: Picanha, Alcatra, Costela e Linguiça",
            "destaque": True,
            "cor_fundo": "#FFF0F5",
            "cor_borda": "#FF69B4"
        },
        {
            "nome": "🎄 Cesta Natalina Completa",
            "preco_original": 299.90,
            "preco_promocional": 229.90,
            "desconto": "23%",
            "descricao": "Todos os itens para sua ceia de Natal",
            "destaque": True,
            "cor_fundo": "#F0FFF0",
            "cor_borda": "#32CD32"
        },
        {
            "nome": "🥩 Frango Caipira + Carnes Especiais",
            "preco_original": 159.90,
            "preco_promocional": 119.90,
            "desconto": "25%",
            "descricao": "Kit proteínas premium para o mês",
            "destaque": True,
            "cor_fundo": "#FFF5EE",
            "cor_borda": "#FF4500"
        }
    ]
    return produtos_destaque[(mes_atual - 1) % len(produtos_destaque)]

promocoes_mes = [
    {"nome": "Arroz 5kg", "preco_original": 25.90, "preco_promocional": 22.90, "desconto": "12%", "destaque": False},
    {"nome": "Feijão 1kg", "preco_original": 9.50, "preco_promocional": 8.50, "desconto": "11%", "destaque": False},
    {"nome": "Óleo 900ml", "preco_original": 8.80, "preco_promocional": 7.80, "desconto": "11%", "destaque": False},
    {"nome": "Macarrão 500g", "preco_original": 4.90, "preco_promocional": 4.20, "desconto": "14%", "destaque": False},
    {"nome": "Café 250g", "preco_original": 11.90, "preco_promocional": 9.90, "desconto": "17%", "destaque": False},
    {"nome": "Açúcar 1kg", "preco_original": 5.50, "preco_promocional": 4.50, "desconto": "18%", "destaque": False},
    {"nome": "Leite 1L", "preco_original": 4.80, "preco_promocional": 3.99, "desconto": "17%", "destaque": False},
    {"nome": "Sabão em Pó", "preco_original": 15.90, "preco_promocional": 12.90, "desconto": "19%", "destaque": False}
]

# Adicionar produto destaque do mês
produto_destaque = obter_promocao_destaque_mes()
promocoes_com_destaque = [produto_destaque] + promocoes_mes

# === FUNÇÃO: EXIBIR TELA DE EDIÇÃO DE INFORMAÇÕES ===
def mostrar_editar_info():
    for w in app.winfo_children():
        w.destroy()
    app.title("✏️ Editar Informações do Usuário")

    # Cores e fontes
    PRIMARY_COLOR = "#FF7043"
    HOVER_COLOR = "#FF5722"
    BACKGROUND_COLOR = "#F8F8F8"
    CARD_COLOR = "#FFFFFF"
    TEXT_COLOR = "#333333"

    # === FRAME PRINCIPAL ===
    main_frame = ctk.CTkFrame(app, fg_color=BACKGROUND_COLOR)
    main_frame.pack(fill="both", expand=True)

    # === HEADER ===
    header = ctk.CTkFrame(main_frame, fg_color=CARD_COLOR, corner_radius=0)
    header.pack(fill="x")
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)
    header.grid_columnconfigure(2, weight=0)

    ctk.CTkLabel(
        header,
        text="✏️ Editar Informações do Usuário",
        text_color=PRIMARY_COLOR,
        font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
    ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

    # Botão para voltar às informações do usuário
    btn_voltar = ctk.CTkButton(
        header,
        text="⬅️ Voltar",
        width=100, height=36,
        fg_color=PRIMARY_COLOR,
        hover_color=HOVER_COLOR,
        text_color="#FFFFFF",
        corner_radius=8,
        command=mostrar_info_usuario
    )
    btn_voltar.grid(row=0, column=1, sticky="e", padx=(0, 10), pady=15)

    # === INTERRUPTOR MODO ESCURO ===
    switch_tema = ctk.CTkSwitch(
        header,
        text="🌙 Escuro",
        command=alternar_tema
    )
    switch_tema.grid(row=0, column=2, padx=(10, 20), pady=15)

    # === SEPARADOR ===
    ctk.CTkFrame(main_frame, fg_color="#E0E0E0", height=1).pack(fill="x", padx=20)

    # === CONTEÚDO PRINCIPAL ===
    content_frame = ctk.CTkFrame(main_frame, fg_color=BACKGROUND_COLOR)
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Frame de formulário de edição
    form_frame = ctk.CTkFrame(content_frame, fg_color=CARD_COLOR, corner_radius=12)
    form_frame.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(
        form_frame,
        text="Editar Dados Pessoais",
        text_color=PRIMARY_COLOR,
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))

    # Campos de entrada para edição
    campos = []
    
    # Nome
    nome_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    nome_frame.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(nome_frame, text="👤 Nome:", text_color=TEXT_COLOR, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
    entry_nome = ctk.CTkEntry(
        nome_frame, 
        placeholder_text="Digite seu nome completo",
        width=400, height=40, corner_radius=8,
        fg_color=BACKGROUND_COLOR,
        text_color=TEXT_COLOR,
        font=ctk.CTkFont(size=14)
    )
    entry_nome.pack(fill="x", pady=(5, 0))
    entry_nome.insert(0, dados_usuario["nome"])
    campos.append(("nome", entry_nome))

    # E-mail
    email_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    email_frame.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(email_frame, text="📧 E-mail:", text_color=TEXT_COLOR, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
    entry_email = ctk.CTkEntry(
        email_frame, 
        placeholder_text="Digite seu e-mail",
        width=400, height=40, corner_radius=8,
        fg_color=BACKGROUND_COLOR,
        text_color=TEXT_COLOR,
        font=ctk.CTkFont(size=14)
    )
    entry_email.pack(fill="x", pady=(5, 0))
    entry_email.insert(0, dados_usuario["email"])
    campos.append(("email", entry_email))

    # Telefone
    telefone_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    telefone_frame.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(telefone_frame, text="📞 Telefone:", text_color=TEXT_COLOR, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
    entry_telefone = ctk.CTkEntry(
        telefone_frame, 
        placeholder_text="Digite seu telefone",
        width=400, height=40, corner_radius=8,
        fg_color=BACKGROUND_COLOR,
        text_color=TEXT_COLOR,
        font=ctk.CTkFont(size=14)
    )
    entry_telefone.pack(fill="x", pady=(5, 0))
    entry_telefone.insert(0, dados_usuario["telefone"])
    campos.append(("telefone", entry_telefone))

    # Endereço
    endereco_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    endereco_frame.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(endereco_frame, text="📍 Endereço:", text_color=TEXT_COLOR, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
    entry_endereco = ctk.CTkEntry(
        endereco_frame, 
        placeholder_text="Digite seu endereço completo",
        width=400, height=40, corner_radius=8,
        fg_color=BACKGROUND_COLOR,
        text_color=TEXT_COLOR,
        font=ctk.CTkFont(size=14)
    )
    entry_endereco.pack(fill="x", pady=(5, 0))
    entry_endereco.insert(0, dados_usuario["endereco"])
    campos.append(("endereco", entry_endereco))

    # Frame para botões
    botoes_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    botoes_frame.pack(fill="x", padx=20, pady=20)
    
    def salvar_alteracoes():
        # Validar campos obrigatórios
        if not entry_nome.get().strip():
            messagebox.showwarning("Atenção", "O campo Nome é obrigatório.")
            return
        
        if not entry_email.get().strip():
            messagebox.showwarning("Atenção", "O campo E-mail é obrigatório.")
            return
        
        # Validar formato de e-mail básico
        if "@" not in entry_email.get() or "." not in entry_email.get():
            messagebox.showwarning("Atenção", "Por favor, insira um e-mail válido.")
            return
        
        # Atualizar dados do usuário
        dados_usuario["nome"] = entry_nome.get().strip()
        dados_usuario["email"] = entry_email.get().strip()
        dados_usuario["telefone"] = entry_telefone.get().strip()
        dados_usuario["endereco"] = entry_endereco.get().strip()
        
        messagebox.showinfo("Sucesso", "Informações atualizadas com sucesso!")
        mostrar_info_usuario()

    def cancelar_edicao():
        if messagebox.askyesno("Cancelar", "Tem certeza que deseja cancelar as alterações?"):
            mostrar_info_usuario()

    # Botão Salvar
    ctk.CTkButton(
        botoes_frame,
        text="💾 Salvar Alterações",
        width=180, height=40,
        fg_color="#4CAF50",
        hover_color="#45a049",
        text_color="#FFFFFF",
        corner_radius=8,
        font=ctk.CTkFont(size=14, weight="bold"),
        command=salvar_alteracoes
    ).pack(side="left", padx=(0, 10))

    # Botão Cancelar
    ctk.CTkButton(
        botoes_frame,
        text="❌ Cancelar",
        width=120, height=40,
        fg_color="#D32F2F",
        hover_color="#B71C1C",
        text_color="#FFFFFF",
        corner_radius=8,
        font=ctk.CTkFont(size=14),
        command=cancelar_edicao
    ).pack(side="left")

# === FUNÇÃO: EXIBIR TELA DE INFORMAÇÕES DO USUÁRIO ===
def mostrar_info_usuario():
    for w in app.winfo_children():
        w.destroy()
    app.title("👤 Informações do Usuário")

    # Cores e fontes
    PRIMARY_COLOR = "#FF7043"
    HOVER_COLOR = "#FF5722"
    BACKGROUND_COLOR = "#F8F8F8"
    CARD_COLOR = "#FFFFFF"
    TEXT_COLOR = "#333333"

    # === FRAME PRINCIPAL ===
    main_frame = ctk.CTkFrame(app, fg_color=BACKGROUND_COLOR)
    main_frame.pack(fill="both", expand=True)

    # === HEADER ===
    header = ctk.CTkFrame(main_frame, fg_color=CARD_COLOR, corner_radius=0)
    header.pack(fill="x")
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)
    header.grid_columnconfigure(2, weight=0)

    ctk.CTkLabel(
        header,
        text="👤 Informações do Usuário",
        text_color=PRIMARY_COLOR,
        font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
    ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

    # Botão para voltar ao menu principal
    btn_voltar = ctk.CTkButton(
        header,
        text="⬅️ Voltar",
        width=100, height=36,
        fg_color=PRIMARY_COLOR,
        hover_color=HOVER_COLOR,
        text_color="#FFFFFF",
        corner_radius=8,
        command=mostrar_menu
    )
    btn_voltar.grid(row=0, column=1, sticky="e", padx=(0, 10), pady=15)

    # === INTERRUPTOR MODO ESCURO ===
    switch_tema = ctk.CTkSwitch(
        header,
        text="🌙 Escuro",
        command=alternar_tema
    )
    switch_tema.grid(row=0, column=2, padx=(10, 20), pady=15)

    # === SEPARADOR ===
    ctk.CTkFrame(main_frame, fg_color="#E0E0E0", height=1).pack(fill="x", padx=20)

    # === CONTEÚDO PRINCIPAL ===
    content_frame = ctk.CTkFrame(main_frame, fg_color=BACKGROUND_COLOR)
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Frame de informações do usuário
    info_frame = ctk.CTkFrame(content_frame, fg_color=CARD_COLOR, corner_radius=12)
    info_frame.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(
        info_frame,
        text="Dados Pessoais",
        text_color=PRIMARY_COLOR,
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))

    user_info = [
        ("👤 Nome:", dados_usuario["nome"]),
        ("📧 E-mail:", dados_usuario["email"]),
        ("📞 Telefone:", dados_usuario["telefone"]),
        ("📍 Endereço:", dados_usuario["endereco"])
    ]

    for label, value in user_info:
        row = ctk.CTkFrame(info_frame, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(row, text=label, text_color=TEXT_COLOR, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        ctk.CTkLabel(row, text=value, text_color=TEXT_COLOR, font=ctk.CTkFont(size=14)).pack(side="left", padx=(10, 0))

    # Botão para editar informações
    ctk.CTkButton(
        info_frame,
        text="✏️ Editar Informações",
        width=200, height=36,
        fg_color=PRIMARY_COLOR,
        hover_color=HOVER_COLOR,
        text_color="#FFFFFF",
        corner_radius=8,
        font=ctk.CTkFont(size=14),
        command=mostrar_editar_info
    ).pack(pady=15)

    # Frame de promoções
    promocoes_frame = ctk.CTkFrame(content_frame, fg_color=CARD_COLOR, corner_radius=12)
    promocoes_frame.pack(fill="both", expand=True)

    ctk.CTkLabel(
        promocoes_frame,
        text="🔥 Promoções do Mês",
        text_color=PRIMARY_COLOR,
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(anchor="w", padx=20, pady=(15, 10))

    # Frame rolável para promoções
    promocoes_scroll = ctk.CTkScrollableFrame(promocoes_frame, fg_color="transparent")
    promocoes_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    for promocao in promocoes_com_destaque:
        if promocao["destaque"]:
            # Card especial para produto destaque
            card = ctk.CTkFrame(
                promocoes_scroll, 
                fg_color=promocao["cor_fundo"],
                border_color=promocao["cor_borda"],
                border_width=3,
                corner_radius=15
            )
            card.pack(fill="x", pady=12, padx=5)
            
            # Badge "DESTAQUE DO MÊS"
            badge_frame = ctk.CTkFrame(card, fg_color=promocao["cor_borda"], corner_radius=8)
            badge_frame.pack(anchor="w", padx=15, pady=(12, 5))
            
            ctk.CTkLabel(
                badge_frame,
                text="⭐ DESTAQUE DO MÊS ⭐",
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(padx=10, pady=3)
        else:
            # Card normal para promoções regulares
            card = ctk.CTkFrame(promocoes_scroll, fg_color="#FFF5EE", corner_radius=12)
            card.pack(fill="x", pady=8)

        # Informações do produto em promoção
        info_col = ctk.CTkFrame(card, fg_color="transparent")
        info_col.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(
            info_col,
            text=promocao["nome"],
            text_color=PRIMARY_COLOR,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        # Adicionar descrição para produtos destaque
        if promocao["destaque"] and "descricao" in promocao:
            ctk.CTkLabel(
                info_col,
                text=promocao["descricao"],
                text_color="#666666",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=(2, 0))

        preco_original = ctk.CTkLabel(
            info_col,
            text=f"De: R$ {promocao['preco_original']:.2f}",
            text_color="#888888",
            font=ctk.CTkFont(size=14)
        )
        preco_original.pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            info_col,
            text=f"Por: R$ {promocao['preco_promocional']:.2f}",
            text_color="#E53935",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", pady=(2, 0))

        # Economia do cliente
        economia = promocao["preco_original"] - promocao["preco_promocional"]
        ctk.CTkLabel(
            info_col,
            text=f"💵 Economize: R$ {economia:.2f}",
            text_color="#4CAF50",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(5, 0))

        # Badge de desconto
        discount_badge = ctk.CTkFrame(card, fg_color="#E53935", corner_radius=8)
        discount_badge.pack(side="right", padx=15, pady=10)

        ctk.CTkLabel(
            discount_badge,
            text=f"🔻 {promocao['desconto']} OFF",
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(padx=10, pady=5)

# === FUNÇÃO: EXIBE MENU DE PRODUTOS ===
def mostrar_menu():
    for w in app.winfo_children():
        w.destroy()
    app.title("🛍️ Loja Virtual")

    # Cores e fontes
    PRIMARY_COLOR    = "#FF7043"
    HOVER_COLOR      = "#FF5722"
    BACKGROUND_COLOR = "#F8F8F8"
    CARD_COLOR       = "#FFFFFF"
    TEXT_COLOR       = "#333333"

    # === FRAME PRINCIPAL ===
    main_frame = ctk.CTkFrame(app, fg_color=BACKGROUND_COLOR)
    main_frame.pack(fill="both", expand=True)

    # === HEADER ===
    header = ctk.CTkFrame(main_frame, fg_color=CARD_COLOR, corner_radius=0)
    header.pack(fill="x")
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)
    header.grid_columnconfigure(2, weight=0)
    header.grid_columnconfigure(3, weight=0)
    header.grid_columnconfigure(4, weight=0)

    ctk.CTkLabel(
        header,
        text="🛍️ Loja Virtual",
        text_color=PRIMARY_COLOR,
        font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
    ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

    # Botão para informações do usuário
    btn_user = ctk.CTkButton(
        header,
        text="👤",
        width=48, height=36,
        fg_color=PRIMARY_COLOR,
        hover_color=HOVER_COLOR,
        text_color="#FFFFFF",
        corner_radius=8,
        command=mostrar_info_usuario
    )
    btn_user.grid(row=0, column=1, sticky="e", padx=(0,5), pady=15)

    # Campo de busca
    entry_search = ctk.CTkEntry(
        header,
        placeholder_text="Buscar produto…",
        width=180, height=36, corner_radius=8,
        fg_color=BACKGROUND_COLOR,
        text_color=TEXT_COLOR,
        font=ctk.CTkFont(size=14)
    )
    entry_search.grid(row=0, column=2, sticky="e", padx=(0,5), pady=15)

    # Botão de busca com funcionalidade
    btn_search = ctk.CTkButton(
        header,
        text="🔍",
        width=48, height=36,
        fg_color=PRIMARY_COLOR,
        hover_color=HOVER_COLOR,
        text_color="#FFFFFF",
        corner_radius=8,
        command=lambda: atualizar_lista_produtos(entry_search.get().strip())
    )
    btn_search.grid(row=0, column=3, sticky="e", padx=(5,5), pady=15)

    # === INTERRUPTOR MODO ESCURO ===
    switch_tema = ctk.CTkSwitch(
        header,
        text="🌙 Escuro",
        command=alternar_tema
    )
    switch_tema.grid(row=0, column=4, padx=(10,20), pady=15)

    # Dados iniciais
    produtos = [
        {"nome": "Arroz 5kg", "preco": 22.90},
        {"nome": "Feijão 1kg", "preco": 8.50},
        {"nome": "Óleo 900ml", "preco": 7.80},
        {"nome": "Macarrão 500g", "preco": 4.20},
        {"nome": "Café 250g", "preco": 9.90},
        {"nome": "Açúcar 1kg", "preco": 4.50},
        {"nome": "Leite 1L", "preco": 3.99},
        {"nome": "Sabão em Pó", "preco": 12.90},
        {"nome": "Sal 1kg", "preco": 2.50},
        {"nome": "Farinha de Trigo 1kg", "preco": 5.90},
        {"nome": "Creme Dental", "preco": 4.80},
        {"nome": "Sabonete", "preco": 1.99}
    ]
    carrinho = []

    # === SEPARADOR ===
    ctk.CTkFrame(main_frame, fg_color="#E0E0E0", height=1).pack(fill="x", padx=20)

    # === ABA DE TABS ===
    tabs = ctk.CTkTabview(
        main_frame,
        fg_color=BACKGROUND_COLOR,
        segmented_button_selected_color=PRIMARY_COLOR,
        segmented_button_selected_hover_color=HOVER_COLOR
    )
    tabs.pack(fill="both", expand=True, padx=20, pady=20)
    tabs.add("Produtos")
    tabs.add("Carrinho")
    tabs.add("Promoções")  # Nova aba para promoções

    # === FRAME PRODUTOS ===
    produtos_frame = ctk.CTkScrollableFrame(
        tabs.tab("Produtos"),
        fg_color=BACKGROUND_COLOR,
        corner_radius=0
    )
    produtos_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

    form = ctk.CTkFrame(tabs.tab("Produtos"), fg_color=CARD_COLOR, corner_radius=12)
    form.pack(fill="x", padx=10, pady=10)

    entry_nome = ctk.CTkEntry(
        form, placeholder_text="Nome do produto",
        width=300, height=36, corner_radius=8,
        fg_color=BACKGROUND_COLOR,
        text_color=TEXT_COLOR,
        font=ctk.CTkFont(size=14)
    )
    entry_nome.pack(side="left", padx=(20,10), pady=12)

    entry_preco = ctk.CTkEntry(
        form, placeholder_text="Preço (ex: 10.99)",
        width=150, height=36, corner_radius=8,
        fg_color=BACKGROUND_COLOR,
        text_color=TEXT_COLOR,
        font=ctk.CTkFont(size=14)
    )
    entry_preco.pack(side="left", padx=(0,10), pady=12)

    def adicionar_produto():
        nome = entry_nome.get().strip()
        preco = entry_preco.get().replace(",", ".").strip()
        if not nome or not preco:
            messagebox.showwarning("Atenção", "Preencha nome e preço válidos.")
            return
        try:
            valor = float(preco)
        except ValueError:
            messagebox.showerror("Erro", "Formato de preço inválido.")
            return
        produtos.append({"nome": nome, "preco": valor})
        entry_nome.delete(0, "end")
        entry_preco.delete(0, "end")
        atualizar_lista_produtos(entry_search.get().strip())
        messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado.")

    btn_add_prod = ctk.CTkButton(
        form,
        text="➕ Adicionar produto",
        width=160, height=36,
        fg_color=PRIMARY_COLOR,
        hover_color=HOVER_COLOR,
        text_color="#FFFFFF",
        corner_radius=10,
        font=ctk.CTkFont(size=14),
        command=adicionar_produto
    )
    btn_add_prod.pack(side="right", padx=(10,20), pady=12)

    # Função de busca aprimorada
    def realizar_busca(termo_busca):
        """Realiza a busca nos produtos e retorna resultados"""
        if not termo_busca:
            return produtos  # Retorna todos os produtos se não há busca
        
        termo_busca = termo_busca.lower().strip()
        resultados = []
        
        for produto in produtos:
            # Busca por nome do produto
            if termo_busca in produto["nome"].lower():
                resultados.append(produto)
        
        return resultados

    # Atualizações
    def atualizar_lista_produtos(termo_busca=None):
        if termo_busca is None:
            termo_busca = entry_search.get().strip()
        
        # Limpar frame atual
        for w in produtos_frame.winfo_children():
            w.destroy()
        
        # Obter produtos filtrados
        produtos_filtrados = realizar_busca(termo_busca)
        
        if not produtos_filtrados:
            # Mostrar mensagem quando não há resultados
            if termo_busca:
                ctk.CTkLabel(
                    produtos_frame,
                    text=f"🔍 Nenhum produto encontrado para '{termo_busca}'",
                    text_color="#666666",
                    font=ctk.CTkFont(size=16)
                ).pack(pady=50)
                
                # Sugerir adicionar novo produto
                sugestao_frame = ctk.CTkFrame(produtos_frame, fg_color="transparent")
                sugestao_frame.pack(pady=10)
                
                ctk.CTkLabel(
                    sugestao_frame,
                    text="Deseja adicionar este produto?",
                    text_color=TEXT_COLOR,
                    font=ctk.CTkFont(size=14)
                ).pack()
                
                ctk.CTkButton(
                    sugestao_frame,
                    text=f"➕ Adicionar '{termo_busca}'",
                    width=200, height=36,
                    fg_color=PRIMARY_COLOR,
                    hover_color=HOVER_COLOR,
                    text_color="#FFFFFF",
                    corner_radius=8,
                    font=ctk.CTkFont(size=12),
                    command=lambda: [entry_nome.insert(0, termo_busca), entry_preco.focus()]
                ).pack(pady=10)
            else:
                ctk.CTkLabel(
                    produtos_frame,
                    text="📦 Nenhum produto cadastrado",
                    text_color="#666666",
                    font=ctk.CTkFont(size=16)
                ).pack(pady=50)
            return
        
        # Mostrar contador de resultados
        if termo_busca:
            resultado_label = ctk.CTkFrame(produtos_frame, fg_color="transparent")
            resultado_label.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(
                resultado_label,
                text=f"🔍 {len(produtos_filtrados)} produto(s) encontrado(s) para '{termo_busca}'",
                text_color=PRIMARY_COLOR,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(anchor="w")
        
        # Adicionar produtos filtrados
        for prod in produtos_filtrados:
            card = ctk.CTkFrame(produtos_frame, fg_color=CARD_COLOR, corner_radius=12)
            card.pack(fill="x", pady=8, padx=8)
            
            # Destacar termo de busca no nome do produto
            nome_produto = prod["nome"]
            if termo_busca and termo_busca in nome_produto.lower():
                # Criar label com destaque (simulação)
                nome_label = ctk.CTkLabel(
                    card,
                    text=f"{nome_produto}  —  R$ {prod['preco']:.2f}",
                    text_color=TEXT_COLOR,
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                nome_label.pack(side="left", padx=20, pady=15)
            else:
                ctk.CTkLabel(
                    card,
                    text=f"{nome_produto}  —  R$ {prod['preco']:.2f}",
                    text_color=TEXT_COLOR,
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack(side="left", padx=20, pady=15)
            
            ctk.CTkButton(
                card,
                text="➕ Adicionar",
                width=120, height=36,
                fg_color=PRIMARY_COLOR,
                hover_color=HOVER_COLOR,
                text_color="#FFFFFF",
                corner_radius=10,
                font=ctk.CTkFont(size=14),
                command=lambda p=prod: adicionar_ao_carrinho(p)
            ).pack(side="right", padx=20)

    carrinho_frame = ctk.CTkScrollableFrame(
        tabs.tab("Carrinho"),
        fg_color=BACKGROUND_COLOR,
        corner_radius=0
    )
    carrinho_frame.pack(fill="both", expand=True, padx=10, pady=(10,0))

    def atualizar_carrinho():
        for w in carrinho_frame.winfo_children():
            w.destroy()
        if not carrinho:
            ctk.CTkLabel(
                carrinho_frame,
                text="Seu carrinho está vazio",
                text_color=TEXT_COLOR,
                font=ctk.CTkFont(size=16)
            ).pack(pady=20)
            return
        total = 0.0
        for prod in carrinho:
            total += prod["preco"]
            card = ctk.CTkFrame(carrinho_frame, fg_color=CARD_COLOR, corner_radius=12)
            card.pack(fill="x", pady=8, padx=8)
            ctk.CTkLabel(
                card,
                text=f"{prod['nome']} — R$ {prod['preco']:.2f}",
                text_color=TEXT_COLOR,
                font=ctk.CTkFont(size=15)
            ).pack(side="left", padx=20, pady=12)
            ctk.CTkButton(
                card,
                text="🗑️ Remover",
                width=120, height=36,
                fg_color="#D32F2F",
                hover_color="#B71C1C",
                text_color="#FFFFFF",
                corner_radius=10,
                font=ctk.CTkFont(size=14),
                command=lambda p=prod: remover_do_carrinho(p)
            ).pack(side="right", padx=20)
        ctk.CTkLabel(
            carrinho_frame,
            text=f"🧾 Total: R$ {total:.2f}",
            text_color=PRIMARY_COLOR,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20)

    def adicionar_ao_carrinho(prod):
        carrinho.append(prod)
        atualizar_carrinho()
        messagebox.showinfo("Sucesso", f"'{prod['nome']}' adicionado ao carrinho!")

    def remover_do_carrinho(prod):
        carrinho.remove(prod)
        atualizar_carrinho()
        messagebox.showinfo("Removido", f"'{prod['nome']}' removido do carrinho!")

    btn_finalizar = ctk.CTkButton(
        tabs.tab("Carrinho"),
        text="✅ Finalizar compra",
        width=200, height=44,
        fg_color=PRIMARY_COLOR,
        hover_color=HOVER_COLOR,
        text_color="#FFFFFF",
        corner_radius=12,
        font=ctk.CTkFont(size=16, weight="bold"),
        command=lambda: (
            messagebox.showinfo("Compra concluída", f"Total pago: R$ {sum(p['preco'] for p in carrinho):.2f}"),
            carrinho.clear(),
            atualizar_carrinho()
        )
    )
    btn_finalizar.pack(pady=20)

    # === FRAME PROMOÇÕES (MELHORADA) ===
    promocoes_frame = ctk.CTkScrollableFrame(
        tabs.tab("Promoções"),
        fg_color=BACKGROUND_COLOR,
        corner_radius=0
    )
    promocoes_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Título das promoções
    ctk.CTkLabel(
        promocoes_frame,
        text="🔥 PROMOÇÕES DO MÊS",
        text_color=PRIMARY_COLOR,
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(pady=(0, 10))

    # Subtítulo com contador de promoções
    ctk.CTkLabel(
        promocoes_frame,
        text=f"🎯 {len(promocoes_com_destaque)} ofertas especiais para você",
        text_color="#666666",
        font=ctk.CTkFont(size=14)
    ).pack(pady=(0, 20))

    # Adicionar cards de promoção
    for promocao in promocoes_com_destaque:
        if promocao["destaque"]:
            # Card DESTAQUE DO MÊS (design premium)
            card = ctk.CTkFrame(
                promocoes_frame, 
                fg_color=promocao["cor_fundo"],
                border_color=promocao["cor_borda"],
                border_width=4,
                corner_radius=20,
                height=140
            )
            card.pack(fill="x", pady=15, padx=5)
            card.pack_propagate(False)
            
            # Container interno para o card destaque
            inner_frame = ctk.CTkFrame(card, fg_color="transparent")
            inner_frame.pack(fill="both", expand=True, padx=20, pady=15)
            
            # Linha superior com badge e título
            top_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
            top_frame.pack(fill="x", pady=(0, 10))
            
            # Badge "DESTAQUE DO MÊS"
            badge_frame = ctk.CTkFrame(top_frame, fg_color=promocao["cor_borda"], corner_radius=10)
            badge_frame.pack(side="left")
            
            ctk.CTkLabel(
                badge_frame,
                text="⭐ DESTAQUE DO MÊS ⭐",
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(padx=12, pady=4)
            
            # Preços alinhados à direita
            price_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
            price_frame.pack(side="right")
            
            ctk.CTkLabel(
                price_frame,
                text=f"R$ {promocao['preco_original']:.2f}",
                text_color="#888888",
                font=ctk.CTkFont(size=14, overstrike=True)
            ).pack(anchor="e")
            
            ctk.CTkLabel(
                price_frame,
                text=f"R$ {promocao['preco_promocional']:.2f}",
                text_color="#E53935",
                font=ctk.CTkFont(size=20, weight="bold")
            ).pack(anchor="e")
            
            # Linha inferior com informações do produto
            bottom_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
            bottom_frame.pack(fill="x")
            
            # Informações do produto
            product_info = ctk.CTkFrame(bottom_frame, fg_color="transparent")
            product_info.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(
                product_info,
                text=promocao["nome"],
                text_color=PRIMARY_COLOR,
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                product_info,
                text=promocao["descricao"],
                text_color="#666666",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=(2, 0))
            
            # Economia destacada
            economia = promocao["preco_original"] - promocao["preco_promocional"]
            economy_frame = ctk.CTkFrame(product_info, fg_color="#4CAF50", corner_radius=6)
            economy_frame.pack(anchor="w", pady=(8, 0))
            
            ctk.CTkLabel(
                economy_frame,
                text=f"💰 ECONOMIZE R$ {economia:.2f} • {promocao['desconto']} OFF",
                text_color="white",
                font=ctk.CTkFont(size=11, weight="bold")
            ).pack(padx=8, pady=3)
            
            # Botão de ação destacado
            btn_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
            btn_frame.pack(side="right")
            
            ctk.CTkButton(
                btn_frame,
                text="🛒 COMPRAR AGORA",
                width=140, height=40,
                fg_color=promocao["cor_borda"],
                hover_color="#D32F2F",
                text_color="white",
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda p=promocao: adicionar_promocao_ao_carrinho(p)
            ).pack(pady=(10, 0))
            
        else:
            # Card normal para promoções regulares (também melhorado)
            card = ctk.CTkFrame(
                promocoes_frame, 
                fg_color="#FFF5EE",
                border_color="#FFD700",
                border_width=2,
                corner_radius=15,
                height=100
            )
            card.pack(fill="x", pady=8, padx=2)
            card.pack_propagate(False)
            
            inner_frame = ctk.CTkFrame(card, fg_color="transparent")
            inner_frame.pack(fill="both", expand=True, padx=15, pady=10)
            
            # Layout em duas colunas
            left_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
            left_frame.pack(side="left", fill="both", expand=True)
            
            right_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
            right_frame.pack(side="right")
            
            # Informações do produto
            ctk.CTkLabel(
                left_frame,
                text=promocao["nome"],
                text_color=PRIMARY_COLOR,
                font=ctk.CTkFont(size=15, weight="bold")
            ).pack(anchor="w")
            
            # Preços
            price_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
            price_frame.pack(anchor="w", pady=(5, 0))
            
            ctk.CTkLabel(
                price_frame,
                text=f"De: R$ {promocao['preco_original']:.2f}",
                text_color="#888888",
                font=ctk.CTkFont(size=12, overstrike=True)
            ).pack(side="left")
            
            ctk.CTkLabel(
                price_frame,
                text=f"  Por: R$ {promocao['preco_promocional']:.2f}",
                text_color="#E53935",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left")
            
            # Badge de desconto
            discount_badge = ctk.CTkFrame(right_frame, fg_color="#E53935", corner_radius=8)
            discount_badge.pack(pady=(5, 0))
            
            ctk.CTkLabel(
                discount_badge,
                text=f"🔻 {promocao['desconto']}",
                text_color="white",
                font=ctk.CTkFont(size=11, weight="bold")
            ).pack(padx=10, pady=4)
            
            # Botão de adicionar
            ctk.CTkButton(
                right_frame,
                text="➕ Adicionar",
                width=100, height=30,
                fg_color=PRIMARY_COLOR,
                hover_color=HOVER_COLOR,
                text_color="#FFFFFF",
                corner_radius=8,
                font=ctk.CTkFont(size=12),
                command=lambda p=promocao: adicionar_promocao_ao_carrinho(p)
            ).pack(pady=(8, 0))

    def adicionar_promocao_ao_carrinho(promocao):
        # Adiciona o produto promocional ao carrinho
        carrinho.append({"nome": promocao["nome"], "preco": promocao["preco_promocional"]})
        atualizar_carrinho()
        # Muda para a aba do carrinho
        tabs.set("Carrinho")
        messagebox.showinfo("Sucesso", f"Produto '{promocao['nome']}' adicionado ao carrinho!")

    # Configurar eventos de busca
    def on_search_keyrelease(event):
        atualizar_lista_produtos(entry_search.get().strip())
    
    def on_search_button():
        termo = entry_search.get().strip()
        atualizar_lista_produtos(termo)
        if termo:
            messagebox.showinfo("Busca", f"Buscando por: '{termo}'")

    # Conectar eventos
    entry_search.bind("<KeyRelease>", on_search_keyrelease)
    btn_search.configure(command=on_search_button)
    
    # Tecla Enter para busca
    entry_search.bind("<Return>", lambda e: on_search_button())
    
    # Inicializar a lista de produtos
    atualizar_lista_produtos()
    atualizar_carrinho()

# === FUNÇÃO: VALIDAÇÃO DO LOGIN ===
def on_login():
    user = entry_user.get().strip()
    pwd  = entry_pass.get().strip()
    if not user or not pwd:
        messagebox.showwarning("Atenção", "Informe usuário e senha.")
        return
    mostrar_menu()

# === FUNÇÃO: CADASTRO ===
def abrir_cadastro():
    cadastro_win = ctk.CTkToplevel(app)
    cadastro_win.title("Cadastro de Usuário")
    cadastro_win.geometry("400x400")
    ctk.CTkLabel(cadastro_win, text="Cadastro", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)
    entry_nome_cad = ctk.CTkEntry(cadastro_win, placeholder_text="Nome completo", width=300, height=40)
    entry_nome_cad.pack(pady=10)
    entry_user_cad = ctk.CTkEntry(cadastro_win, placeholder_text="Usuário", width=300, height=40)
    entry_user_cad.pack(pady=10)
    entry_pass_cad = ctk.CTkEntry(cadastro_win, placeholder_text="Senha", show="*", width=300, height=40)
    entry_pass_cad.pack(pady=10)
    ctk.CTkButton(
        cadastro_win,
        text="Cadastrar",
        width=200, height=40,
        fg_color="#4CAF50",
        hover_color="#388E3C",
        command=lambda: messagebox.showinfo("Sucesso", f"Usuário '{entry_user_cad.get()}' cadastrado!")
    ).pack(pady=20)

# === FUNÇÃO: ALTERNAR TEMA ===
def alternar_tema():
    global modo_escuro
    modo_escuro = not modo_escuro
    if modo_escuro:
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")

# === TELA DE LOGIN ===
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Frame esquerdo (login)
frame_left = ctk.CTkFrame(app, corner_radius=0, fg_color="#F5F5F5")
frame_left.grid(row=0, column=0, sticky="nsew")
frame_left.grid_rowconfigure(1, weight=2)
frame_left.grid_columnconfigure(0, weight=1)

login_container = ctk.CTkFrame(frame_left, fg_color="transparent")
login_container.grid(row=1, column=0, sticky="nsew")

ctk.CTkLabel(login_container, text="SUPERMERCADO", font=("Comfortaa", 35, "bold"), text_color="#3A3A3A").pack(pady=(40,50))
ctk.CTkLabel(login_container, text="BEM VINDO!", font=("Comfortaa", 40, "bold"), text_color="#3A3A3A").pack(pady=(0,10))
ctk.CTkLabel(login_container, text="Gerencie sua loja de forma prática e rápida", font=("Arial", 16,"bold"), text_color="#3A3A3A").pack(pady=(0,10))

entry_user = ctk.CTkEntry(login_container, placeholder_text="👤 Usuário", width=300, height=45, corner_radius=10)
entry_user.pack(pady=8)
entry_pass = ctk.CTkEntry(login_container, placeholder_text="🔒 Senha", show="*", width=300, height=45, corner_radius=10)
entry_pass.pack(pady=8)

ctk.CTkButton(
    login_container,
    text="Esqueceu sua senha?",
    fg_color="transparent",
    hover_color="#E8E8E8",
    text_color="#3A3A3A",
    command=lambda: messagebox.showinfo("Recuperar senha", "Funcionalidade em construção.")
).pack(pady=(5,15))

btn_login = ctk.CTkButton(login_container, text="Entrar", width=300, height=45, corner_radius=10, fg_color="#E28539", hover_color="#E2B539", command=on_login)
btn_login.pack(pady=8)

ctk.CTkButton(
    login_container,
    text="Cadastre-se",
    width=300, height=45,
    corner_radius=10,
    fg_color="transparent",
    hover_color="#E2B539",
    border_width=2,
    border_color="#E28539",
    text_color="#E28539",
    command=abrir_cadastro
).pack(pady=8)

# Frame direito (logo)
frame_right = ctk.CTkFrame(app, corner_radius=0, fg_color="#E28539")
frame_right.grid(row=0, column=1, sticky="nsew")
frame_right.grid_rowconfigure(1, weight=1)
frame_right.grid_columnconfigure(0, weight=1)

ctk.CTkButton(frame_right, text="⚙️", width=40, height=40, corner_radius=10, fg_color="white", hover_color="#818181", border_width=2, border_color="#3A3A3A", text_color="#3A3A3A").grid(row=0, column=0, sticky="ne", padx=20, pady=20)

frame_footer = ctk.CTkFrame(frame_right, corner_radius=0, fg_color="#E28539", height=80)
frame_footer.grid(row=2, column=0, sticky="ew")
frame_footer.grid_propagate(False)
ctk.CTkLabel(frame_footer, text="Política de Privacidade | Ajuda | Suporte\n\n📞 (91)98765-4321   🌐 www.projetoloja.com", text_color="#FFFFFF", font=("Arial",14,"bold")).pack(expand=True)

# === INICIA APLICATIVO ===
app.mainloop()