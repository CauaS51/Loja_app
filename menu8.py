import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from datetime import datetime

# Configurações iniciais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # só placeholder, cores personalizadas abaixo

# --- Tema laranja profissional ---
THEME = {
    "BACKGROUND": "#121212",
    "CARD_BG": "#1E1E1E",
    "PRIMARY": "#FF7043",
    "HOVER": "#FF9E40",
    "TEXT_PRIMARY": "#F2F2F2",
    "TEXT_SECONDARY": "#A0A0A0",
    "ENTRY_BG": "#333333",
    "ERROR": "#E53935"
}


class LojaApp:
    def __init__(self):
        # Produtos
        self.produtos = [
            {"nome": "Arroz 5kg", "preco": 7.90, "img": "arroz.png"},
            {"nome": "Feijão 1kg", "preco": 8.50, "img": "feijao.png"},
            {"nome": "Óleo 900ml", "preco": 7.80, "img": "oleo.jpg"},
            {"nome": "Macarrão 500g", "preco": 4.20, "img": "macarrao.png"},
            {"nome": "Café 250g", "preco": 9.90, "img": "café.png"},
            {"nome": "Batata frita congelada", "preco": 12.00, "img": "batata frita.png"},
            {"nome": "Leite 1L", "preco": 5.50, "img": "leite.png"},
            {"nome": "Pão de forma", "preco": 6.30, "img": "pao de forma.png"},
            {"nome": "Queijo mussarela 200g", "preco": 13.00, "img": "queijo.png"},
            {"nome": "Banana (por kg)", "preco": 6.50, "img": "banana.png"},
        ]
        self.carrinho = {}
        self.imagens_cache = {}
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.historico_path = os.path.join(self.base_dir, "historico_compras.txt")

        # Categorias automáticas
        self.categorias = self.criar_categorias()

        # App principal
        self.app = ctk.CTk()
        self.app.geometry("1100x700")
        self.app.title("Caixa Laranja")
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)

        self.carregar_imagens()
        self._build_ui()
        self.atualizar_lista_produtos()
        self.atualizar_carrinho()

    # --- Cores ---
    def get_colors(self):
        return THEME

    # --- Caminho das imagens ---
    def get_img_path(self, relative_path):
        return os.path.join(self.base_dir, relative_path)

    # --- Carregar imagens ---
    def carregar_imagens(self):
        for produto in self.produtos:
            try:
                img_path = self.get_img_path(produto["img"])
                self.imagens_cache[produto["nome"]] = ctk.CTkImage(
                    light_image=Image.open(img_path), size=(80, 80)
                )
            except Exception as e:
                print(f"Erro ao carregar imagem {produto['img']}: {e}")
                self.imagens_cache[produto["nome"]] = None

    # --- Categorias automáticas ---
    def criar_categorias(self):
        categorias = {}
        for p in self.produtos:
            nome = p["nome"].lower()
            if any(k in nome for k in ["arroz", "feijão", "feijao", "macarrão", "café", "cafe", "óleo", "oleo"]):
                categorias.setdefault("Alimentos", []).append(p)
            elif any(k in nome for k in ["leite", "queijo", "pão", "pao"]):
                categorias.setdefault("Laticínios & Padaria", []).append(p)
            elif any(k in nome for k in ["banana", "batata"]):
                categorias.setdefault("Hortifruti", []).append(p)
            else:
                categorias.setdefault("Outros", []).append(p)
        return categorias

    # --- Construir UI principal ---
    def _build_ui(self):
        cores = self.get_colors()
        self.app.configure(fg_color=cores["BACKGROUND"])

        # --- Menu lateral de categorias ---
        self.menu_frame = ctk.CTkFrame(self.app, width=220, fg_color=cores["CARD_BG"])
        self.menu_frame.grid(row=0, column=0, sticky="ns")
        self.menu_frame.grid_rowconfigure(0, weight=0)
        self.menu_frame.grid_rowconfigure(1, weight=1)

        title_label = ctk.CTkLabel(
            self.menu_frame,
            text="CATEGORIAS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=cores["PRIMARY"]
        )
        title_label.grid(row=0, column=0, padx=10, pady=20)

        self.categorias_frame = ctk.CTkScrollableFrame(self.menu_frame, fg_color=cores["CARD_BG"])
        self.categorias_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        for cat in self.categorias.keys():
            btn = ctk.CTkButton(
                self.categorias_frame,
                text=cat,
                width=200,
                fg_color=cores["PRIMARY"],
                hover_color=cores["HOVER"],
                text_color="white",
                corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda c=cat: self.filtrar_categoria(c)
            )
            btn.pack(pady=5)

        # --- Frame principal de produtos e carrinho ---
        self.main_frame = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"])
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)  # coluna do checkout inicialmente fixa

        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color=cores["CARD_BG"], height=80)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.entry_search = ctk.CTkEntry(
            self.header_frame,
            placeholder_text="🔍 Buscar produto...",
            width=300,
            height=40,
            corner_radius=12,
            fg_color=cores["ENTRY_BG"],
            text_color=cores["TEXT_PRIMARY"]
        )
        self.entry_search.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.entry_search.bind("<KeyRelease>", lambda e: self.atualizar_lista_produtos())

        # Botões do header
        self.toggle_frame_btn = ctk.CTkButton(
            self.header_frame,
            text="🛒 Carrinho",
            width=120,
            fg_color=cores["PRIMARY"],
            hover_color=cores["HOVER"],
            text_color="white",
            corner_radius=12,
            command=self.toggle_carrinho
        )
        self.toggle_frame_btn.grid(row=0, column=1, padx=10)

        self.historico_btn = ctk.CTkButton(
            self.header_frame,
            text="📜 Histórico",
            width=120,
            fg_color="#444",
            hover_color="#666",
            text_color="white",
            corner_radius=12,
            command=self.mostrar_historico
        )
        self.historico_btn.grid(row=0, column=2, padx=10)

        # Produtos
        self.produtos_frame = ctk.CTkScrollableFrame(
            self.main_frame, fg_color=cores["BACKGROUND"]
        )
        self.produtos_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Carrinho
        self.carrinho_frame = ctk.CTkScrollableFrame(
            self.main_frame, fg_color=cores["BACKGROUND"]
        )
        self.carrinho_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.carrinho_frame.grid_remove()  # inicialmente escondido

        # Histórico
        self.historico_frame = ctk.CTkFrame(self.main_frame, fg_color=cores["BACKGROUND"])
        self.historico_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.historico_frame.grid_remove()

        # Checkout
        self.checkout_frame = ctk.CTkFrame(
            self.main_frame, width=320, fg_color=cores["CARD_BG"]
        )
        self.checkout_frame.grid(row=1, column=1, sticky="ns", padx=(10, 20), pady=10)

        # Dentro do checkout, criar os widgets de resumo
        self.total_label = ctk.CTkLabel(
            self.checkout_frame,
            text="Total: R$ 0,00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=cores["PRIMARY"]
        )
        self.total_label.pack(pady=20)

        self.finalizar_btn = ctk.CTkButton(
            self.checkout_frame,
            text="Finalizar Compra",
            width=280,
            fg_color=cores["PRIMARY"],
            hover_color=cores["HOVER"],
            text_color="white",
            corner_radius=15,
            command=self.finalizar_compra
        )
        self.finalizar_btn.pack(pady=10)

    # --- Filtrar por categoria ---
    def filtrar_categoria(self, categoria):
        self.filtrar = categoria
        self.atualizar_lista_produtos()

    # --- Atualizar lista de produtos ---
    def atualizar_lista_produtos(self):
        filtro = self.entry_search.get().lower()
        self.produtos_frame.grid()
        for widget in self.produtos_frame.winfo_children():
            widget.destroy()

        produtos_filtrados = []
        if hasattr(self, 'filtrar') and self.filtrar:
            produtos_filtrados = [p for p in self.categorias.get(self.filtrar, []) if filtro in p["nome"].lower()]
        else:
            produtos_filtrados = [p for p in self.produtos if filtro in p["nome"].lower()]

        for produto in produtos_filtrados:
            frame = ctk.CTkFrame(self.produtos_frame, height=100, fg_color=THEME["CARD_BG"])
            frame.pack(fill="x", pady=5, padx=5)

            img = self.imagens_cache.get(produto["nome"])
            if img:
                label_img = ctk.CTkLabel(frame, image=img, text="")
                label_img.pack(side="left", padx=10)
            else:
                label_img = ctk.CTkLabel(frame, text="Sem imagem")
                label_img.pack(side="left", padx=10)

            nome_label = ctk.CTkLabel(
                frame, text=produto["nome"], font=ctk.CTkFont(size=16), width=200
            )
            nome_label.pack(side="left", padx=10)

            preco_label = ctk.CTkLabel(
                frame,
                text=f"R$ {produto['preco']:.2f}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=THEME["PRIMARY"],
                width=100,
            )
            preco_label.pack(side="left")

            btn_adicionar = ctk.CTkButton(
                frame,
                text="Adicionar",
                width=100,
                fg_color=THEME["PRIMARY"],
                hover_color=THEME["HOVER"],
                text_color="white",
                corner_radius=12,
                command=lambda p=produto: self.adicionar_carrinho(p),
            )
            btn_adicionar.pack(side="right", padx=10)

    # --- Adicionar produto ao carrinho ---
    def adicionar_carrinho(self, produto):
        if produto["nome"] in self.carrinho:
            self.carrinho[produto["nome"]]["quantidade"] += 1
        else:
            self.carrinho[produto["nome"]] = {"produto": produto, "quantidade": 1}
        self.atualizar_carrinho()

    # --- Atualizar carrinho ---
    def atualizar_carrinho(self):
        for widget in self.carrinho_frame.winfo_children():
            widget.destroy()

        if not self.carrinho:
            vazio_label = ctk.CTkLabel(self.carrinho_frame, text="Carrinho vazio.", font=ctk.CTkFont(size=16))
            vazio_label.pack(pady=20)
            self.total_label.configure(text="Total: R$ 0,00")
            return

        total = 0
        for item in self.carrinho.values():
            produto = item["produto"]
            quantidade = item["quantidade"]
            subtotal = produto["preco"] * quantidade
            total += subtotal

            frame = ctk.CTkFrame(self.carrinho_frame, height=80, fg_color=THEME["CARD_BG"])
            frame.pack(fill="x", pady=5, padx=5)

            nome_label = ctk.CTkLabel(frame, text=produto["nome"], font=ctk.CTkFont(size=14))
            nome_label.pack(side="left", padx=10)

            qtd_label = ctk.CTkLabel(frame, text=f"Qtd: {quantidade}", font=ctk.CTkFont(size=14))
            qtd_label.pack(side="left", padx=10)

            subtotal_label = ctk.CTkLabel(
                frame, text=f"R$ {subtotal:.2f}", font=ctk.CTkFont(size=14), text_color=THEME["PRIMARY"]
            )
            subtotal_label.pack(side="left", padx=10)

            btn_remover = ctk.CTkButton(
                frame,
                text="Remover",
                width=80,
                fg_color="#b22222",
                hover_color="#cc3232",
                text_color="white",
                corner_radius=12,
                command=lambda p=produto: self.remover_carrinho(p),
            )
            btn_remover.pack(side="right", padx=10)

        self.total_label.configure(text=f"Total: R$ {total:.2f}")

    # --- Remover produto do carrinho ---
    def remover_carrinho(self, produto):
        if produto["nome"] in self.carrinho:
            if self.carrinho[produto["nome"]]["quantidade"] > 1:
                self.carrinho[produto["nome"]]["quantidade"] -= 1
            else:
                del self.carrinho[produto["nome"]]
        self.atualizar_carrinho()

    # --- Finalizar compra ---
    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showinfo("Carrinho vazio", "Adicione produtos antes de finalizar a compra.")
            return

        total = 0
        itens = []
        for item in self.carrinho.values():
            p = item["produto"]
            q = item["quantidade"]
            total += p["preco"] * q
            itens.append(f"{p['nome']} x{q} = R$ {p['preco'] * q:.2f}")

        resumo = "\n".join(itens)
        msg = f"Confirme sua compra:\n\n{resumo}\n\nTotal: R$ {total:.2f}"
        if messagebox.askyesno("Finalizar Compra", msg):
            self.salvar_historico(itens, total)
            self.carrinho.clear()
            self.atualizar_carrinho()
            messagebox.showinfo("Compra finalizada", "Obrigado pela compra!")

    # --- Salvar histórico ---
    def salvar_historico(self, itens, total):
        with open(self.historico_path, "a", encoding="utf-8") as f:
            f.write(f"Compra em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            for item in itens:
                f.write(item + "\n")
            f.write(f"Total: R$ {total:.2f}\n\n")

    # --- Mostrar histórico ---
    def mostrar_historico(self):
        self.produtos_frame.grid_remove()
        self.carrinho_frame.grid_remove()
        self.menu_frame.grid_remove()
        self.historico_frame.grid()

        for widget in self.historico_frame.winfo_children():
            widget.destroy()

        cores = self.get_colors()
        with open(self.historico_path, "r", encoding="utf-8") as f:
            conteudo = f.read()

        label = ctk.CTkLabel(
            self.historico_frame,
            text=conteudo or "Nenhum histórico de compras encontrado.",
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color=cores["TEXT_PRIMARY"],
            wraplength=700
        )
        label.pack(padx=10, pady=10)

        btn_voltar = ctk.CTkButton(
            self.historico_frame,
            text="Voltar",
            width=120,
            fg_color=cores["PRIMARY"],
            hover_color=cores["HOVER"],
            text_color="white",
            corner_radius=12,
            command=self.voltar_produtos
        )
        btn_voltar.pack(pady=10)

    # --- Voltar da tela de histórico para produtos ---
    def voltar_produtos(self):
        self.historico_frame.grid_remove()
        self.menu_frame.grid()
        self.produtos_frame.grid()
        self.carrinho_frame.grid_remove()
        self.toggle_frame_btn.configure(text="🛒 Carrinho")
        self.main_frame.grid_columnconfigure(1, weight=0)

    # --- Toggle carrinho (mostrar/esconder) ---
    def toggle_carrinho(self):
        if self.carrinho_frame.winfo_ismapped():
            # Fechar carrinho: volta ao normal
            self.carrinho_frame.grid_remove()
            self.produtos_frame.grid()
            self.menu_frame.grid()  # mostra categorias
            self.toggle_frame_btn.configure(text="🛒 Carrinho")

            # Checkout volta a tamanho fixo
            self.checkout_frame.grid_configure(sticky="ns")
            self.main_frame.grid_columnconfigure(1, weight=0)

        else:
            # Abrir carrinho
            self.produtos_frame.grid_remove()
            self.historico_frame.grid_remove()
            self.carrinho_frame.grid()
            self.menu_frame.grid_remove()  # esconde categorias

            self.toggle_frame_btn.configure(text="🏠 Produtos")

            # Expande checkout para preencher espaço
            self.checkout_frame.grid_configure(sticky="nsew")
            self.main_frame.grid_columnconfigure(1, weight=1)

    # --- Rodar app ---
    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    loja = LojaApp()
    loja.run()
