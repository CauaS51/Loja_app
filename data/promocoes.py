import customtkinter as ctk

# Frame de promoções
def exibir_promocoes():
    # === CONFIGURAÇÃO GLOBAL ===
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Variável global de tema
    modo_escuro = False
    
    # === CRIAÇÃO DA JANELA PRINCIPAL ===
    promocoes = ctk.CTk()
    promocoes.geometry("1200x700")
    promocoes.minsize(900, 500)
    promocoes.title("Sistema de Gerenciamento")

    # Cores e fontes
    PRIMARY_COLOR    = "#FF7043"
    HOVER_COLOR      = "#FF5722"
    BACKGROUND_COLOR = "#F8F8F8"
    CARD_COLOR       = "#FFFFFF"
    TEXT_COLOR       = "#333333"


    promocoes_frame = ctk.CTkFrame(promocoes, fg_color=CARD_COLOR, corner_radius=12)
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

    for promocao in promocoes:
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