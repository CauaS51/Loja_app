# === data/caixa.py ===
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import data.colors as colors
import data.sessao as sessao

# === TELA DO CAIXA / LOJA ===
class LojaApp:
    def __init__(self, app):
        self.app = app
        self.produtos = [
            {"nome": "Arroz 5kg", "preco": 7.90, "img": "imagens/arroz.png"},
            {"nome": "Feijão 1kg", "preco": 8.50, "img": "imagens/feijao.png"},
            {"nome": "Óleo 900ml", "preco": 7.80, "img": "imagens/oleo.png"},
            {"nome": "Macarrão 500g", "preco": 4.20, "img": "imagens/macarrao.png"},
            {"nome": "Café 250g", "preco": 9.90, "img": "imagens/cafe.jpeg"},
            {"nome": "Batata frita congelada", "preco": 12.00, "img": "imagens/batata.png"},
            {"nome": "Leite 1L", "preco": 5.50, "img": "imagens/leite.png"},
            {"nome": "Pão de forma", "preco": 6.30, "img": "imagens/pao.png"},
            {"nome": "Queijo mussarela 200g", "preco": 13.00, "img": "imagens/queijo.png"},
            {"nome": "Banana (por kg)", "preco": 6.50, "img": "imagens/banana.png"},
        ]
        self.carrinho = {}
        self.modo_escuro = False
        self.imagens_cache = {}

        self.carregar_imagens()
        self.mostrar_tela()

    # === CORES ===
    def get_colors(app):
        return colors.get_colors(app)
    
    # === CARREGAR IMAGENS ===
    def carregar_imagens(self):
        for produto in self.produtos:
            try:
                self.imagens_cache[produto["nome"]] = ctk.CTkImage(
                    light_image=Image.open(produto["img"]),
                    size=(80, 80)
                )
            except:
                self.imagens_cache[produto["nome"]] = None

    # === ALTERAR TEMA ===
    def alternar_tema(self):
        self.modo_escuro = not self.modo_escuro
        ctk.set_appearance_mode("dark" if self.modo_escuro else "light")
        self.mostrar_tela()

    # === MONTAR INTERFACE ===
    def mostrar_tela(self):
        for w in self.app.winfo_children():
            w.destroy()

        cores = self.get_colors()
        self.app.configure(fg_color=cores["BACKGROUND"])

        # Header
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)

        # Botão voltar ao menu
        btn_voltar = ctk.CTkButton(
            header, text="⬅ Voltar", width=80, height=40,
            corner_radius=12, fg_color="#333", hover_color=cores["HOVER"],
            command=lambda: self.voltar_menu()
        )
        btn_voltar.place(relx=0.9, rely=0.5, anchor="center")
        
        title_label = ctk.CTkLabel(
            header, text="🛒 Caixa / Loja", text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=0, padx=30, pady=20, sticky="w")

        self.entry_search = ctk.CTkEntry(
            header, placeholder_text="🔍 Buscar produto...",
            width=250, height=40, corner_radius=12,
            fg_color=cores["ENTRY_BG"], text_color=cores["TEXT_PRIMARY"]
        )
        self.entry_search.grid(row=0, column=1, padx=10, pady=20)

        icone_tema = "🌙" if self.modo_escuro else "☀️"
        theme_button = ctk.CTkButton(
            header, text=icone_tema, width=50, height=40,
            corner_radius=12, fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"], text_color=cores["TEXT_PRIMARY"],
            font=ctk.CTkFont(size=20), command=self.alternar_tema
        )
        theme_button.grid(row=0, column=2, padx=30, pady=20)

        # Tabs
        tabs = ctk.CTkTabview(self.app,
            fg_color=cores["BACKGROUND"],
            segmented_button_selected_color=cores["PRIMARY"],
            segmented_button_selected_hover_color=cores["HOVER"],
            corner_radius=12
        )
        tabs.pack(expand=True, fill="both", padx=20, pady=(10,20))
        tabs.add("Produtos")
        tabs.add("Carrinho")

        # Frames
        self.produtos_frame = ctk.CTkScrollableFrame(
            tabs.tab("Produtos"), fg_color=cores["BACKGROUND"]
        )
        self.produtos_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.carrinho_frame = ctk.CTkScrollableFrame(
            tabs.tab("Carrinho"), fg_color=cores["BACKGROUND"]
        )
        self.carrinho_frame.pack(fill="both", expand=True, padx=20, pady=20)

        btn_finalizar = ctk.CTkButton(
            tabs.tab("Carrinho"), text="✅ Finalizar compra",
            width=200, height=50, corner_radius=16,
            fg_color=cores["PRIMARY"], hover_color=cores["HOVER"],
            text_color="white", font=ctk.CTkFont(size=16, weight="bold"),
            command=self.finalizar_compra
        )
        btn_finalizar.pack(pady=10)

        self.entry_search.bind("<KeyRelease>", lambda e: self.atualizar_lista_produtos())
        self.atualizar_lista_produtos()
        self.atualizar_carrinho()

    # === VOLTAR PARA MENU PRINCIPAL ===
    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app,usuario=sessao.usuario,perfil=sessao.perfil)

    # === LÓGICA DA LOJA ===
    def adicionar_ao_carrinho(self, produto, qtd_str):
        nome = produto["nome"]
        preco = produto["preco"]
        try:
            qtd = float(qtd_str.replace(",", "."))
            if qtd <= 0:
                raise ValueError
        except:
            self.toast("⚠️ Quantidade inválida.")
            return

        if nome in self.carrinho:
            self.carrinho[nome]["qtd"] += qtd
        else:
            self.carrinho[nome] = {"preco": preco, "qtd": qtd, "img": produto["img"]}
        self.atualizar_carrinho()
        self.toast(f"✅ {nome} adicionado ao carrinho ({qtd:.2f}).")

    def remover_do_carrinho(self, nome):
        if nome in self.carrinho:
            del self.carrinho[nome]
        self.atualizar_carrinho()

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showinfo("Aviso", "Carrinho vazio!")
            return
        total = sum(v["preco"] * v["qtd"] for v in self.carrinho.values())
        resumo = "\n".join(
            f"- {n} ({v['qtd']:.2f}) = R$ {v['preco'] * v['qtd']:.2f}"
            for n, v in self.carrinho.items()
        )
        messagebox.showinfo(
            "Compra concluída",
            f"Itens comprados:\n\n{resumo}\n\nTotal pago: R$ {total:.2f}"
        )
        self.carrinho.clear()
        self.atualizar_carrinho()

    def atualizar_lista_produtos(self):
        for w in self.produtos_frame.winfo_children():
            w.destroy()
        cores = self.get_colors()
        termo = self.entry_search.get().lower().strip()
        num_colunas = 2
        for index, prod in enumerate(self.produtos):
            if termo and termo not in prod["nome"].lower():
                continue
            row = index // num_colunas
            col = index % num_colunas
            card = ctk.CTkFrame(self.produtos_frame, fg_color=cores["CARD_BG"], corner_radius=12, width=400, height=150)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            self.produtos_frame.grid_columnconfigure(col, weight=1)
            img = self.imagens_cache.get(prod["nome"])
            if img:
                ctk.CTkLabel(card, image=img, text="").place(relx=0.05, rely=0.5, anchor="w")
            else:
                ctk.CTkLabel(card, text="📦", font=ctk.CTkFont(size=30)).place(relx=0.05, rely=0.5, anchor="w")
            info_x = 0.25
            ctk.CTkLabel(card, text=prod["nome"], font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=cores["TEXT_PRIMARY"]).place(relx=info_x, rely=0.25, anchor="w")
            ctk.CTkLabel(card, text=f"R$ {prod['preco']:.2f}", font=ctk.CTkFont(size=14),
                         text_color=cores["TEXT_SECONDARY"]).place(relx=info_x, rely=0.55, anchor="w")
            entry_qtd = ctk.CTkEntry(card, width=60, height=32, corner_radius=10, placeholder_text="kg/un")
            entry_qtd.insert(0, "1")
            entry_qtd.place(relx=0.25, rely=0.75, anchor="w")
            ctk.CTkButton(
                card, text="➕ Adicionar", width=120, height=35,
                fg_color=cores["PRIMARY"], hover_color=cores["HOVER"],
                text_color="white", corner_radius=10,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda p=prod, e=entry_qtd: self.adicionar_ao_carrinho(p, e.get())
            ).place(relx=0.9, rely=0.75, anchor="e")

    def atualizar_carrinho(self):
        for w in self.carrinho_frame.winfo_children():
            w.destroy()
        cores = self.get_colors()
        if not self.carrinho:
            ctk.CTkLabel(
                self.carrinho_frame,
                text="🛒 Carrinho vazio",
                font=ctk.CTkFont(size=18),
                text_color=cores["TEXT_PRIMARY"]
            ).pack(pady=40)
            return
        total = 0
        for nome, info in self.carrinho.items():
            subtotal = info["preco"] * info["qtd"]
            total += subtotal
            card = ctk.CTkFrame(self.carrinho_frame, fg_color=cores["CARD_BG"], corner_radius=12)
            card.pack(fill="x", padx=20, pady=8)
            img = self.imagens_cache.get(nome)
            if img:
                ctk.CTkLabel(card, image=img, text="").pack(side="left", padx=15, pady=12)
            else:
                ctk.CTkLabel(card, text="📦", font=ctk.CTkFont(size=24)).pack(side="left", padx=15, pady=12)
            ctk.CTkLabel(
                card,
                text=f"{nome} — {info['qtd']:.2f} x R$ {info['preco']:.2f} = R$ {subtotal:.2f}",
                font=ctk.CTkFont(size=15),
                text_color=cores["TEXT_PRIMARY"]
            ).pack(side="left", padx=10)
            ctk.CTkButton(
                card, text="🗑 Remover", width=100, height=32,
                fg_color="#D32F2F", hover_color="#B71C1C",
                text_color="white", corner_radius=10,
                font=ctk.CTkFont(size=12),
                command=lambda n=nome: self.remover_do_carrinho(n)
            ).pack(side="right", padx=20)
        ctk.CTkLabel(
            self.carrinho_frame,
            text=f"🧾 Total geral: R$ {total:.2f}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=cores["PRIMARY"]
        ).pack(pady=20)

    def toast(self, texto):
        toast = ctk.CTkLabel(
            self.app,
            text=texto,
            fg_color="#323232",
            text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=14)
        )
        toast.place(relx=0.5, rely=0.95, anchor="s")
        self.app.after(2500, toast.destroy)


# === FUNÇÃO DE ACESSO PELO MENU ===
def mostrar_menu(app):
    LojaApp(app)
