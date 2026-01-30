import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog, colorchooser
from crud import crud_lojas
import data.sessao as sessao
from data.menu import mostrar_menu
from data.colors import get_colors
from PIL import Image, ImageTk, ImageOps # Adicionado ImageOps
import json
import os

# ==========================
# CARD COMPONENTE
# ==========================
class Card(ctk.CTkFrame):
    def __init__(self, master, title, color, icon_text, command=None, tooltip=None):
        super().__init__(master, fg_color=color, corner_radius=15)
        self.command = command
        self.default_color = color
        self.hover_color = get_colors()["HOVER"]

        self.icon = ctk.CTkLabel(
            self, text=icon_text, font=("Segoe UI", 28, "bold"),
            text_color="#E98C41", bg_color=color
        )
        self.icon.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")

        self.lbl = ctk.CTkLabel(
            self, text=title, font=("Segoe UI", 20, "bold"),
            text_color="white", bg_color=color
        )
        self.lbl.grid(row=0, column=1, sticky="w", padx=(0, 10))

        # Bindings unificados para evitar falhas de clique
        for widget in [self, self.icon, self.lbl]:
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)

        self.tooltip_text = tooltip
        self.tooltip = None

    def _on_click(self, event=None):
        if callable(self.command):
            self.command()

    def on_enter(self, event=None):
        self.configure(fg_color=self.hover_color)
        if self.tooltip_text and not self.tooltip:
            self.show_tooltip()

    def on_leave(self, event=None):
        self.configure(fg_color=self.default_color)
        if self.tooltip:
            self.hide_tooltip()

    def show_tooltip(self):
        self.tooltip = ctk.CTkLabel(self, text=self.tooltip_text, font=("Segoe UI", 12),
                                    fg_color="black", text_color="white")
        self.tooltip.place(x=0, y=-30)

    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# ==========================
# THEME EDITOR
# ==========================
class ThemeEditor(ctk.CTkToplevel):
    def __init__(self, app, tema_atual=None, nome_loja="", callback_confirmar=None):
        super().__init__(app)
        self.title("Configuração de Identidade Visual")
        self.geometry("950x650")
        self.resizable(False, False)
        self.transient(app)
        self.grab_set()
        
        self.callback_confirmar = callback_confirmar
        self.nome_loja = nome_loja

        self.tema_default = {
            "PRIMARY": "#E98C41", "SECONDARY": "#2F80ED", "HOVER": "#E2B539",
            "BACKGROUND": "#F5F5F5", "BACKGROUND_2": "#FFFFFF", "CARD_BG": "#FFFFFF",
            "TEXT_PRIMARY": "#333333", "TEXT_SECONDARY": "#666666", "ENTRY_BG": "#E0E0E0",
            "CARD_CAIXA": "#36A84A", "CARD_ESTOQUE": "#2F80ED", "CARD_RELATORIOS": "#F2994A",
            "CARD_CADASTROS": "#7C4DFF", "LOGO": "🏬", "LOGO_IMG": None
        }

        self.tema = tema_atual.copy() if tema_atual else self.tema_default.copy()
        self.cards_preview = []
        self.labels_preview = [] 
        self.color_buttons = {} # Dicionário para mapear os botões de seleção de cor

        self.center_window()
        self.criar_interface()
        self.atualizar_preview()

    def center_window(self):
        self.update_idletasks()
        w, h = 950, 650
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def criar_interface(self):
        # Limpar grids anteriores para evitar sobreposição
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ================= COLUNA ESQUERDA: AJUSTES =================
        left_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=None)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(left_panel, text="Customização", font=("Segoe UI", 20, "bold")).pack(pady=(0, 20), anchor="w")

        scroll_colors = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
        scroll_colors.pack(expand=True, fill="both")

        # Seções de Cores (Dicionário com botões para atualizar depois)
        self.criar_secao_cor(scroll_colors, "Cores Principais", ["PRIMARY", "SECONDARY", "HOVER", "BACKGROUND"])
        self.criar_secao_cor(scroll_colors, "Cores dos Cards", ["CARD_CAIXA", "CARD_ESTOQUE", "CARD_RELATORIOS", "CARD_CADASTROS"])
        self.criar_secao_cor(scroll_colors, "Interface e Texto", ["TEXT_PRIMARY", "TEXT_SECONDARY", "CARD_BG", "ENTRY_BG"])

        actions_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkButton(actions_frame, text="Resetar", fg_color="#E74C3C", hover_color="#C0392B", 
                      width=100, command=self.resetar_tema).pack(side="left", padx=5)
        ctk.CTkButton(actions_frame, text="Salvar e Finalizar", fg_color="#27AE60", hover_color="#1E8449",
                      command=self.confirmar).pack(side="right", fill="x", expand=True, padx=5)

        # ================= COLUNA DIREITA: PREVIEW =================
        self.right_panel = ctk.CTkFrame(self, corner_radius=20)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.preview_header = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.preview_header.pack(fill="x", padx=20, pady=20)

        self.logo_container = ctk.CTkFrame(self.preview_header, width=100, height=100, corner_radius=50)
        self.logo_container.pack(side="left")
        self.logo_container.pack_propagate(False)
        
        self.lbl_logo_preview = ctk.CTkLabel(self.logo_container, text=self.tema["LOGO"], font=("Segoe UI", 40))
        self.lbl_logo_preview.pack(expand=True)
        
        info_frame = ctk.CTkFrame(self.preview_header, fg_color="transparent")
        info_frame.pack(side="left", padx=20)
        
        self.nome_entry = ctk.CTkEntry(info_frame, placeholder_text="Nome da Loja", width=250, font=("Segoe UI", 16, "bold"))
        self.nome_entry.insert(0, self.nome_loja)
        self.nome_entry.pack(pady=5)

        self.desc_entry = ctk.CTkEntry(info_frame, placeholder_text="Slogan ou Descrição", width=250)
        self.desc_entry.pack(pady=5)
        
        ctk.CTkButton(self.preview_header, text="Alterar Logo", width=100, command=self.escolher_logo).pack(side="right", padx=10)

        self.cards_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.cards_container.pack(expand=True, fill="both", padx=20, pady=10)
        self.cards_container.grid_columnconfigure((0,1), weight=1)

        nomes_cards = ["Vendas", "Estoque", "Financeiro", "Config"]
        icones = ["💰", "📦", "📊", "⚙️"]
        
        self.cards_preview = []
        self.labels_preview = []

        for i, (nome, icone) in enumerate(zip(nomes_cards, icones)):
            card = ctk.CTkFrame(self.cards_container, corner_radius=12, height=100)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            card.pack_propagate(False)
            
            lbl_i = ctk.CTkLabel(card, text=icone, font=("Segoe UI", 24))
            lbl_i.pack(pady=(15, 0))
            lbl_t = ctk.CTkLabel(card, text=nome, font=("Segoe UI", 13, "bold"))
            lbl_t.pack()
            
            self.cards_preview.append(card)
            self.labels_preview.append((lbl_i, lbl_t))

    def criar_secao_cor(self, master, titulo, chaves):
        ctk.CTkLabel(master, text=titulo, font=("Segoe UI", 12, "bold"), text_color="gray").pack(pady=(10, 5), anchor="w")
        for chave in chaves:
            f = ctk.CTkFrame(master, fg_color="transparent")
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=chave.replace("_", " ").title(), font=("Segoe UI", 11)).pack(side="left")
            
            btn_color = ctk.CTkButton(f, text="", width=30, height=20, corner_radius=4,
                                     fg_color=self.tema[chave], border_width=1, border_color="gray",
                                     command=lambda c=chave: self.escolher_cor(c))
            btn_color.pack(side="right", padx=5)
            self.color_buttons[chave] = btn_color # Guarda a referência para mudar a cor do botão depois

    def escolher_cor(self, chave):
        cor = colorchooser.askcolor(title=f"Escolher {chave}", initialcolor=self.tema[chave])[1]
        if cor:
            self.tema[chave] = cor
            # Atualiza a cor do quadradinho no painel esquerdo
            if chave in self.color_buttons:
                self.color_buttons[chave].configure(fg_color=cor)
            # Atualiza o preview sem recriar a interface
            self.atualizar_preview()

    def escolher_logo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens","*.png *.jpg *.jpeg")])
        if caminho:
            self.tema["LOGO_IMG"] = caminho
            img_pil = Image.open(caminho)
            img_fit = ImageOps.fit(img_pil, (100, 100), Image.Resampling.LANCZOS)
            self_img = ctk.CTkImage(light_image=img_fit, dark_image=img_fit, size=(100,100))
            self.lbl_logo_preview.configure(image=self_img, text="")

    def atualizar_preview(self):
        # 1. Atualiza Fundo
        self.right_panel.configure(fg_color=self.tema["BACKGROUND"])
        
        # 2. Atualiza Entradas de Texto
        self.nome_entry.configure(fg_color=self.tema["ENTRY_BG"], text_color=self.tema["TEXT_PRIMARY"])
        self.desc_entry.configure(fg_color=self.tema["ENTRY_BG"], text_color=self.tema["TEXT_PRIMARY"])
        
        # 3. Atualiza os Cards do Preview
        cores_cards = [
            self.tema["CARD_CAIXA"], 
            self.tema["CARD_ESTOQUE"], 
            self.tema["CARD_RELATORIOS"], 
            self.tema["CARD_CADASTROS"]
        ]
        
        for card, cor, labels in zip(self.cards_preview, cores_cards, self.labels_preview):
            card.configure(fg_color=cor)
            labels[0].configure(text_color="white")
            labels[1].configure(text_color="white")
            
            # Hover dinâmico capturando as cores atuais
            card.bind("<Enter>", lambda e, c=card: c.configure(fg_color=self.tema["HOVER"]))
            card.bind("<Leave>", lambda e, c=card, o=cor: c.configure(fg_color=o))

    def resetar_tema(self):
        if messagebox.askyesno("Confirmar", "Deseja resetar para as cores padrão?"):
            self.tema = self.tema_default.copy()
            # Atualiza os botões da esquerda
            for chave, btn in self.color_buttons.items():
                btn.configure(fg_color=self.tema[chave])
            # Reseta Logo
            self.lbl_logo_preview.configure(image=None, text=self.tema["LOGO"])
            self.atualizar_preview()

    def confirmar(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Dê um nome para sua loja!")
            return
        
        self.tema["NOME_LOJA"] = nome
        self.tema["DESCRICAO"] = self.desc_entry.get()
        
        if self.callback_confirmar:
            self.callback_confirmar(self.tema)
        
        self.destroy()

    def salvar_auto_json(self):
        if not os.path.exists("themes"):
            os.makedirs("themes")
        nome_arquivo = f"themes/{self.tema['NOME_LOJA'].lower().replace(' ', '_')}.json"
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(self.tema, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar JSON: {e}")

# ==========================
# APP PRINCIPAL
# ==========================
class LojaApp:
    def __init__(self, app):
        self.app = app
        self.cores = get_colors()
        self.minhas_lojas = []
        self.carregar_lojas_usuario()
        self.mostrar_lojas()

    def carregar_lojas_usuario(self):
        try:
            self.minhas_lojas = crud_lojas.listar_lojas_usuario(sessao.usuario_id) or []
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar lojas: {e}")
            self.minhas_lojas = []

    def mostrar_lojas(self):
        for w in self.app.winfo_children(): w.destroy()
        self.criar_header()
        self.criar_cards_fixos()
        self.renderizar_minhas_lojas()

    def criar_header(self):
        header = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND_2"], corner_radius=15)
        header.pack(fill="x", padx=20, pady=20)
        logo_frame = ctk.CTkFrame(header, fg_color=self.cores["BACKGROUND_2"])
        logo_frame.pack(side="left", padx=50)
        ctk.CTkLabel(logo_frame, text="🏬", font=("Segoe UI",50), text_color=self.cores["SECONDARY"]).pack(side="left")
        ctk.CTkLabel(logo_frame, text="LOJAS", font=("Segoe UI",20,"bold"), text_color=self.cores["TEXT_PRIMARY"]).pack(side="left", padx=(10,0))

        user_frame = ctk.CTkFrame(header, fg_color=self.cores["BACKGROUND_2"])
        user_frame.pack(side="right", padx=30)
        ctk.CTkLabel(user_frame, text=sessao.nome, font=("Segoe UI",14), text_color=self.cores["TEXT_PRIMARY"]).pack(side="left", padx=(0,10))
        ctk.CTkButton(user_frame, text="Sair", command=self.logout,fg_color=self.cores["PRIMARY"],hover_color="#ff0000", width=80).pack(side="left")

    def criar_cards_fixos(self):
        container = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND_2"], corner_radius=10)
        container.pack(expand=True, fill="both", padx=20, pady=10)
        welcome_frame = ctk.CTkFrame(container, fg_color=self.cores["BACKGROUND"], corner_radius=10)
        welcome_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(welcome_frame, text=f"Bem-vindo, {sessao.nome}!", text_color=self.cores["TEXT_PRIMARY"], font=("Segoe UI",28,"bold")).pack(pady=(20,5))
        ctk.CTkLabel(welcome_frame, text="Escolha uma loja para continuar:", text_color=self.cores["TEXT_PRIMARY"]).pack(pady=(0,20))

        cards_frame = ctk.CTkFrame(welcome_frame, fg_color=self.cores["BACKGROUND"])
        cards_frame.pack(fill="x", padx=20)
        cards_frame.grid_columnconfigure((0,1), weight=1)

        Card(cards_frame, "Criar Loja", self.cores["CARD_CADASTROS"], "➕", self.criar_loja, "Clique para criar uma nova loja").grid(row=0,column=0,padx=20,pady=10,sticky="nsew")
        Card(cards_frame, "Entrar em Loja", self.cores["CARD_CAIXA"], "🔑", self.entrar_loja, "Digite o ID de uma loja").grid(row=0,column=1,padx=20,pady=10,sticky="nsew")

        self.lojas_frame = ctk.CTkFrame(welcome_frame, fg_color=self.cores["BACKGROUND"])
        self.lojas_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def renderizar_minhas_lojas(self):
        for w in self.lojas_frame.winfo_children(): w.destroy()
        if not self.minhas_lojas:
            ctk.CTkLabel(self.lojas_frame, text="Você ainda não está vinculado a nenhuma loja.", font=("Segoe UI",16), text_color=self.cores["TEXT_PRIMARY"]).pack(pady=40)
            return

        max_cols = 4
        card_size = 180
        self.lojas_frame.grid_columnconfigure(tuple(range(max_cols)), weight=1)

        for i, loja in enumerate(self.minhas_lojas):
            logo_path = loja.get("img")
            img_ctk = None

            if logo_path and os.path.exists(logo_path):
                try:
                    img_pil = Image.open(logo_path)
                    # O segredo para não distorcer: ImageOps.fit
                    img_fit = ImageOps.fit(img_pil, (card_size, card_size - 40), Image.Resampling.LANCZOS)
                    img_ctk = ctk.CTkImage(light_image=img_fit, dark_image=img_fit, size=(card_size, card_size - 40))
                except: img_ctk = None

            card = ctk.CTkFrame(self.lojas_frame, fg_color=self.cores["CARD_ESTOQUE"], corner_radius=15, width=card_size, height=card_size)
            card.grid(row=i//max_cols, column=i%max_cols, padx=10, pady=10, sticky="nw")
            card.pack_propagate(False)

            # Hover unificado
            def on_enter(e, c=card): c.configure(fg_color=self.cores["HOVER"])
            def on_leave(e, c=card): c.configure(fg_color=self.cores["CARD_ESTOQUE"])

            if img_ctk:
                lbl_img = ctk.CTkLabel(card, image=img_ctk, text="")
                lbl_img.pack(fill="both", expand=True)
                lbl_img.bind("<Button-1>", lambda e, l=loja: self.entrar_loja_id(l))
                lbl_img.bind("<Enter>", on_enter)
                lbl_img.bind("<Leave>", on_leave)
            else:
                lbl_icon = ctk.CTkLabel(card, text="🏬", font=("Segoe UI",48))
                lbl_icon.place(relx=0.5, rely=0.4, anchor="center")
                lbl_icon.bind("<Button-1>", lambda e, l=loja: self.entrar_loja_id(l))
                lbl_icon.bind("<Enter>", on_enter)
                lbl_icon.bind("<Leave>", on_leave)

            lbl_nome = ctk.CTkLabel(card, text=loja["nome"], font=("Segoe UI",13,"bold"), text_color="white")
            lbl_nome.pack(side="bottom", pady=5)
            
            card.bind("<Button-1>", lambda e, l=loja: self.entrar_loja_id(l))
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

    def criar_loja(self):
        def confirmar_tema(tema):
            nome = tema.get("NOME_LOJA")
            if not nome:
                messagebox.showerror("Erro", "Informe o nome da loja")
                return

            # 1️⃣ Cria a loja
            loja_id = crud_lojas.criar_loja(nome)
            if not loja_id:
                messagebox.showerror("Erro", "Falha ao criar loja")
                return

            # 2️⃣ Salva o tema no banco (FONTE DA VERDADE)
            crud_lojas.salvar_tema_loja(loja_id, tema)

            # 3️⃣ Salva logo (se houver)
            if tema.get("LOGO_IMG"):
                crud_lojas.atualizar_loja(loja_id, img=tema["LOGO_IMG"])

            # 4️⃣ Associa usuário como Administrador
            crud_lojas.associar_usuario_a_loja(
                sessao.usuario_id,
                loja_id,
                "Administrador"
            )

            # 5️⃣ Atualiza interface
            self.carregar_lojas_usuario()
            self.renderizar_minhas_lojas()

            messagebox.showinfo("Sucesso", "Loja criada com sucesso!")

        # Abre o editor de tema
        ThemeEditor(
            self.app,
            nome_loja="",
            callback_confirmar=confirmar_tema
        )

    def entrar_loja(self):
        loja_id = simpledialog.askinteger("Entrar em Loja", "Digite o ID da loja:")
        if not loja_id:
            return

        loja = crud_lojas.entrar_em_loja(loja_id, sessao.usuario_id)

        if not loja:
            criado = crud_lojas.associar_usuario_a_loja(
                sessao.usuario_id,
                loja_id,
                "Caixa"  # perfil padrão ao entrar em loja existente
            )

            if not criado:
                messagebox.showerror("Erro", "Loja não encontrada ou falha ao acessar.")
                return

            loja = crud_lojas.entrar_em_loja(loja_id, sessao.usuario_id)

        self.carregar_sessao_loja(loja)


    def entrar_loja_id(self, loja):
        self.carregar_sessao_loja(loja)

    def carregar_sessao_loja(self, loja):
        dados_visuais = crud_lojas.buscar_dados_visuais(loja["id"])

        sessao.funcionario_id = loja["id_funcionario"]
        sessao.loja_id = loja["id"]
        sessao.perfil = loja["perfil"]
        sessao.nome_loja = loja["nome"]

        tema_raw = dados_visuais.get("Tema_JSON")
        tema = json.loads(tema_raw) if tema_raw else None

        if tema:
            # Caminho do cache local
            nome_arquivo = sessao.nome_loja.lower().replace(" ", "_")
            caminho = f"themes/{nome_arquivo}.json"

            # Recria o JSON local se tiver sido apagado
            if not os.path.exists(caminho):
                os.makedirs("themes", exist_ok=True)
                with open(caminho, "w", encoding="utf-8") as f:
                    json.dump(tema, f, indent=4, ensure_ascii=False)

            import data.colors as colors
            colors.aplicar_tema_customizado(tema)

        mostrar_menu(self.app, sessao.nome, sessao.perfil)


    def logout(self):
        if messagebox.askyesno("Sair","Deseja realmente sair?"):
            sessao.usuario_id = None
            from custompdv import mostrar_login
            mostrar_login(self.app)

def mostrar_lojas(app):
    LojaApp(app)