import customtkinter as ctk
from tkinter import messagebox

def mostrar_menu():
    # === CONFIGURAÇÃO GLOBAL ===
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Variável global de tema
    modo_escuro = False

    # === CRIAÇÃO DA JANELA PRINCIPAL ===
    menu = ctk.CTk()
    menu.geometry("1200x700")
    menu.minsize(900, 500)
    menu.title("Sistema de Gerenciamento")

        # === FUNÇÃO: EXIBE MENU DE PRODUTOS ===

    for w in menu.winfo_children():
        w.destroy()
    menu.title("🛍️ Loja Virtual")

    # Cores e fontes
    PRIMARY_COLOR    = "#FF7043"
    HOVER_COLOR      = "#FF5722"
    BACKGROUND_COLOR = "#F8F8F8"
    CARD_COLOR       = "#FFFFFF"
    TEXT_COLOR       = "#333333"

    # === FRAME PRINCIPAL ===
    main_frame = ctk.CTkFrame(menu, fg_color=BACKGROUND_COLOR)
    main_frame.pack(fill="both", expand=True)

    # === HEADER ===
    header = ctk.CTkFrame(main_frame, fg_color=CARD_COLOR, corner_radius=0)
    header.pack(fill="x")
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)
    header.grid_columnconfigure(2, weight=0)
    header.grid_columnconfigure(3, weight=0)

    ctk.CTkLabel(
        header,
        text="🛍️ Loja Virtual",
        text_color=PRIMARY_COLOR,
        font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
    ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

    entry_search = ctk.CTkEntry(
        header,
        placeholder_text="Buscar produto…",
        width=180, height=36, corner_radius=8,
        fg_color=BACKGROUND_COLOR,
        text_color=TEXT_COLOR,
        font=ctk.CTkFont(size=14)
    )
    entry_search.grid(row=0, column=1, sticky="e", padx=(0,5), pady=15)

    btn_search = ctk.CTkButton(
        header,
        text="🔍",
        width=48, height=36,
        fg_color=PRIMARY_COLOR,
        hover_color=HOVER_COLOR,
        text_color="#FFFFFF",
        corner_radius=8
    )
    btn_search.grid(row=0, column=2, sticky="e", padx=(5,5), pady=15)

    # === INTERRUPTOR MODO ESCURO ===
    switch_tema = ctk.CTkSwitch(
        header,
        text="🌙 Escuro",
        command = None
    )
    switch_tema.grid(row=0, column=3, padx=(10,20), pady=15)

    # Dados iniciais
    produtos = [
        {"nome": "Arroz 5kg", "preco": 22.90},
        {"nome": "Feijão 1kg", "preco": 8.50},
        {"nome": "Óleo 900ml", "preco": 7.80},
        {"nome": "Macarrão 500g", "preco": 4.20},
        {"nome": "Café 250g", "preco": 9.90}
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
    tabs.add("Promoções")

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
        atualizar_lista_produtos()
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

    # Atualizações
    def atualizar_lista_produtos():
        term = entry_search.get().lower().strip()
        for w in produtos_frame.winfo_children():
            w.destroy()
        for prod in produtos:
            if term and term not in prod["nome"].lower():
                continue
            card = ctk.CTkFrame(produtos_frame, fg_color=CARD_COLOR, corner_radius=12)
            card.pack(fill="x", pady=8, padx=8)
            ctk.CTkLabel(
                card,
                text=f"{prod['nome']}  —  R$ {prod['preco']:.2f}",
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

    def remover_do_carrinho(prod):
        carrinho.remove(prod)
        atualizar_carrinho()

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

    entry_search.bind("<KeyRelease>", lambda e: atualizar_lista_produtos())
    btn_search.configure(command=atualizar_lista_produtos)
    atualizar_lista_produtos()
    atualizar_carrinho()
    menu.mainloop()