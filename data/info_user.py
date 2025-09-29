import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# === CONFIGURAÇÃO GLOBAL ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Dados do usuário (simulando um banco de dados)
dados_usuario = {
    "nome": "Maria Silva Santos",
    "email": "maria.silva@email.com",
    "telefone": "(11) 98765-4321",
    "endereco": "Rua das Flores, 123 - São Paulo/SP"
}

# === CRIAÇÃO DA JANELA PRINCIPAL ===
info_user = ctk.CTk()                   #app > info_user
info_user.geometry("1200x700")
info_user.minsize(900, 500)
info_user.title("Sistema de Gerenciamento")

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
    for w in info_user.winfo_children():
        w.destroy()
    info_user.title("✏️ Editar Informações do Usuário")

    # Cores e fontes
    PRIMARY_COLOR = "#FF7043"
    HOVER_COLOR = "#FF5722"
    BACKGROUND_COLOR = "#F8F8F8"
    CARD_COLOR = "#FFFFFF"
    TEXT_COLOR = "#333333"

    # === FRAME PRINCIPAL ===
    main_frame = ctk.CTkFrame(info_user, fg_color=BACKGROUND_COLOR)
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
        command=None
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
    for w in info_user.winfo_children():
        w.destroy()
    info_user.title("👤 Informações do Usuário")

    # Cores e fontes
    PRIMARY_COLOR = "#FF7043"
    HOVER_COLOR = "#FF5722"
    BACKGROUND_COLOR = "#F8F8F8"
    CARD_COLOR = "#FFFFFF"
    TEXT_COLOR = "#333333"

    # === FRAME PRINCIPAL ===
    main_frame = ctk.CTkFrame(info_user, fg_color=BACKGROUND_COLOR)
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
        command=None # aiaiai
    )
    btn_voltar.grid(row=0, column=1, sticky="e", padx=(0, 10), pady=15)

    # === INTERRUPTOR MODO ESCURO ===
    switch_tema = ctk.CTkSwitch(
        header,
        text="🌙 Escuro",
        command=None
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
        info_user.mainloop()