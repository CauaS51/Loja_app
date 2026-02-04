import customtkinter as ctk
from tkinter import messagebox
from crud import crud_lojas
import data.sessao as sessao
from data.menu import mostrar_menu
from data.colors import get_colors
from PIL import Image, ImageOps
import json
import os
import re
import io  # Necessário para manipular bytes de imagem

# === CARD COMPONENTE ===
class Card(ctk.CTkFrame):
    def __init__(self, master, title, color, icon_text, command=None, tooltip=None):
        super().__init__(master, fg_color=color, corner_radius=15)
        self.command = command
        self.default_color = color
        self.hover_color = get_colors()["HOVER"]

        self.icon = ctk.CTkLabel(self, text=icon_text, font=("Segoe UI", 28, "bold"),
                                 text_color="#E98C41", bg_color=color)
        self.icon.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")

        self.lbl = ctk.CTkLabel(self, text=title, font=("Segoe UI", 20, "bold"),
                                text_color="white", bg_color=color)
        self.lbl.grid(row=0, column=1, sticky="w", padx=(0, 10))

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

# === TELA PRINCIPAL ===
class LojaApp:
    def __init__(self, app):
        self.app = app
        self.cores = get_colors()
        self.minhas_lojas = []
        self.image_cache = {}
        self.carregar_lojas_usuario()
        self.mostrar_lojas()

    def carregar_lojas_usuario(self):
        try:
            self.minhas_lojas = crud_lojas.listar_lojas_usuario(sessao.usuario_id) or []
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar lojas: {e}")
            self.minhas_lojas = []

    def mostrar_lojas(self):
        for w in self.app.winfo_children():
            w.destroy()
        self.criar_header()
        self.criar_cards_fixos()
        self.renderizar_minhas_lojas()

    def criar_header(self):
        header = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND_2"], corner_radius=15)
        header.pack(fill="x", padx=20, pady=20)

        logo_frame = ctk.CTkFrame(header, fg_color=self.cores["BACKGROUND_2"])
        logo_frame.pack(side="left", padx=50, pady=10)

        ctk.CTkLabel(logo_frame, text="🏬", font=("Segoe UI",50),
                     text_color=self.cores["SECONDARY"]).pack(side="left")
        ctk.CTkLabel(logo_frame, text="LOJAS", font=("Segoe UI",20,"bold"),
                     text_color=self.cores["TEXT_PRIMARY"]).pack(side="left", padx=(8,0))

        user_frame = ctk.CTkFrame(header, fg_color=self.cores["BACKGROUND_2"])
        user_frame.pack(side="right", padx=30)

        ctk.CTkLabel(user_frame, text=sessao.nome, font=("Segoe UI",14),
                     text_color=self.cores["TEXT_PRIMARY"]).pack(side="left", padx=(0,10))
        ctk.CTkButton(user_frame, text="Sair", command=self.logout,
                      fg_color=self.cores["SECONDARY"], hover_color="#ff0000",
                      width=80).pack(side="left")

    def criar_cards_fixos(self):
        container = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND_2"], corner_radius=10)
        container.pack(expand=True, fill="both", padx=20, pady=10)

        welcome_frame = ctk.CTkFrame(container, fg_color=self.cores["BACKGROUND"], corner_radius=10)
        welcome_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(welcome_frame, text=f"Bem-vindo, {sessao.nome}!",
                    text_color=self.cores["TEXT_PRIMARY"], font=("Segoe UI",28,"bold")).pack(pady=(20,5))
        ctk.CTkLabel(welcome_frame, text="Escolha uma loja para continuar:",
                    text_color=self.cores["TEXT_PRIMARY"]).pack(pady=(0,20))

        cards_frame = ctk.CTkFrame(welcome_frame, fg_color=self.cores["BACKGROUND"])
        cards_frame.pack(fill="x", padx=20)
        cards_frame.grid_columnconfigure((0,1), weight=1)

        Card(cards_frame, "Criar Loja", self.cores["CARD_CADASTROS"], "➕",
            self.criar_loja).grid(row=0,column=0,padx=20,pady=10,sticky="nsew")
        Card(cards_frame, "Entrar em Loja", self.cores["CARD_CAIXA"], "🔑",
            self.entrar_loja).grid(row=0,column=1,padx=20,pady=10,sticky="nsew")

        ctk.CTkLabel(welcome_frame, text="Minhas lojas:", font=("Segoe UI", 20, "bold"),
                    text_color=self.cores["TEXT_PRIMARY"], anchor="w").pack(fill="x", padx=20, pady=(20,10))

        self.lojas_frame = ctk.CTkFrame(welcome_frame, fg_color=self.cores["BACKGROUND"])
        self.lojas_frame.pack(expand=True, fill="both", padx=20, pady=(0,20))

    def renderizar_minhas_lojas(self):
        for w in self.lojas_frame.winfo_children():
            w.destroy()

        if not self.minhas_lojas:
            ctk.CTkLabel(self.lojas_frame, text="Você ainda não está vinculado a nenhuma loja.",
                         font=("Segoe UI",16), text_color=self.cores["TEXT_PRIMARY"]).pack(pady=40)
            return

        max_cols = 4
        card_size = 180
        self.lojas_frame.grid_columnconfigure(tuple(range(max_cols)), weight=1)

        for i, loja in enumerate(self.minhas_lojas):
            logo_data = loja.get("img") # Agora recebe BYTES do banco
            img_ctk = None

            if logo_data:
                try:
                    # Usamos o ID da loja como chave de cache
                    cache_key = f"loja_{loja['id']}"
                    if cache_key in self.image_cache:
                        img_ctk = self.image_cache[cache_key]
                    else:
                        # Converte bytes para imagem
                        img_pil = Image.open(io.BytesIO(logo_data))
                        img_fit = ImageOps.fit(img_pil, (card_size, card_size - 40), Image.Resampling.LANCZOS)
                        img_ctk = ctk.CTkImage(light_image=img_fit, dark_image=img_fit,
                                               size=(card_size, card_size - 40))
                        self.image_cache[cache_key] = img_ctk
                except Exception as e:
                    print(f"Erro ao processar imagem binária: {e}")

            card = ctk.CTkFrame(self.lojas_frame, fg_color=self.cores["CARD_ESTOQUE"],
                                corner_radius=15, width=card_size, height=card_size)
            card.grid(row=i//max_cols, column=i%max_cols, padx=10, pady=10, sticky="nw")
            card.pack_propagate(False)

            btn_menu = ctk.CTkButton(card, text="⋮", width=28, height=28, corner_radius=14,
                                     fg_color="transparent", text_color="white", hover_color="#444",
                                     font=("Segoe UI", 16, "bold"),
                                     command=lambda l=loja: self.abrir_menu_card(l))
            btn_menu.place(relx=1.0, x=-8, y=8, anchor="ne")

            def on_enter(e, c=card): c.configure(fg_color=self.cores["HOVER"])
            def on_leave(e, c=card): c.configure(fg_color=self.cores["CARD_ESTOQUE"])

            if img_ctk:
                lbl_img = ctk.CTkLabel(card, image=img_ctk, fg_color="white", text="")
                lbl_img.pack(fill="both", expand=True)
                lbl_img.bind("<Button-1>", lambda e, l=loja: self.entrar_loja_id(l))
                lbl_img.bind("<Button-3>", lambda e, l=loja: self.menu_acoes_loja(e, l))
                lbl_img.bind("<Enter>", on_enter)
                lbl_img.bind("<Leave>", on_leave)
            else:
                lbl_icon = ctk.CTkLabel(card, text="🏬",fg_color="white", font=("Segoe UI",48))
                lbl_icon.place(relx=0.5, rely=0.4, anchor="center")
                lbl_icon.bind("<Button-1>", lambda e, l=loja: self.entrar_lo_id(l))
                lbl_icon.bind("<Button-3>", lambda e, l=loja: self.menu_acoes_loja(e, l))
                lbl_icon.bind("<Enter>", on_enter)
                lbl_icon.bind("<Leave>", on_leave)

            lbl_nome = ctk.CTkLabel(card, text=loja["nome"], font=("Segoe UI",13,"bold"), text_color="white")
            lbl_nome.pack(side="bottom", pady=0)

            lbl_perfil = ctk.CTkLabel(card, text=f"Função: {loja.get('perfil','—')}",
                                      font=("Segoe UI",10,"italic",'bold'), text_color="#E0E0E0")
            lbl_perfil.pack(side="bottom")

            card.bind("<Button-1>", lambda e, l=loja: self.entrar_loja_id(l))
            card.bind("<Button-3>", lambda e, l=loja: self.menu_acoes_loja(e, l))
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

    # === AÇÕES DE LOJA ===
    def menu_acoes_loja(self, event, loja):
        menu = ctk.CTkToplevel(self.app)
        menu.overrideredirect(True)
        menu.geometry(f"180x120+{event.x_root}+{event.y_root}")

        perfil = loja.get("perfil")

        if perfil == "Administrador":
            ctk.CTkButton(menu, text="✏️ Editar Loja",
                          command=lambda: self.editar_loja(loja, menu)).pack(fill="x", pady=5, padx=5)
            ctk.CTkButton(menu, text="🗑 Excluir Loja", fg_color="#aa0000", hover_color="#cc0000",
                          command=lambda: self.excluir_loja(loja, menu)).pack(fill="x", pady=5, padx=5)
        else:
            ctk.CTkButton(menu, text="🚪 Sair da Loja",
                          command=lambda: self.sair_da_loja(loja, menu)).pack(fill="x", pady=5, padx=5)

        menu.bind("<FocusOut>", lambda e: menu.destroy())
        menu.focus_force()

    def abrir_menu_card(self, loja):
        x = self.app.winfo_pointerx()
        y = self.app.winfo_pointery()
        fake_event = type("Event", (), {"x_root": x, "y_root": y})
        self.menu_acoes_loja(fake_event, loja)

    def editar_loja(self, loja, menu):
        menu.destroy()
        from data.tema import ThemeEditor
        
        dados_visuais = crud_lojas.buscar_dados_visuais(loja["id"])
        tema_existente = json.loads(dados_visuais.get("Tema_JSON") or "{}")
        
        if not tema_existente:
            tema_existente = {"NOME_LOJA": loja["nome"]}

        def salvar(novo_tema):
            crud_lojas.salvar_tema_loja(loja["id"], novo_tema)
            
            novo_nome = novo_tema.get("NOME_LOJA")
            logo_path = novo_tema.get("LOGO_IMG")
            logo_blob = None
            
            if logo_path and os.path.exists(logo_path):
                with open(logo_path, "rb") as f:
                    logo_blob = f.read()
            
            crud_lojas.atualizar_loja(loja["id"], nome=novo_nome, img=logo_blob)
            
            self.image_cache.clear()
            self.carregar_lojas_usuario()
            self.renderizar_minhas_lojas()

            messagebox.showinfo("Sucesso", "Loja atualizada com sucesso!")
            
            editor.destroy()

        editor = ThemeEditor(self.app, nome_loja=loja["nome"], callback_confirmar=salvar)
        
        editor.carregar_tema_existente(tema_existente)

        def salvar(novo_tema):
            # A. Atualiza o JSON do tema na tabela Temas_Lojas
            crud_lojas.salvar_tema_loja(loja["id"], novo_tema)
            
            # B. Extrai Nome e Logo para atualizar a tabela principal (Lojas)
            novo_nome = novo_tema.get("NOME_LOJA", loja["nome"])
            logo_path = novo_tema.get("LOGO_IMG")
            logo_blob = None
            
            # Se o usuário selecionou uma nova imagem no PC
            if logo_path and os.path.exists(logo_path):
                try:
                    with open(logo_path, "rb") as f:
                        logo_blob = f.read()
                except Exception as e:
                    print(f"Erro ao ler imagem: {e}")

            # C. Chama o CRUD para atualizar o nome e a imagem binária
            sucesso = crud_lojas.atualizar_loja(loja["id"], nome=novo_nome, img=logo_blob)
            
            if sucesso:
                # D. Limpa o cache e atualiza a tela
                self.image_cache.clear()
                self.carregar_lojas_usuario()
                self.renderizar_minhas_lojas()
                messagebox.showinfo("Sucesso", "Configurações da loja atualizadas!")
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar os dados no banco.")

        # 3. Abre o editor e popula os campos
        editor = ThemeEditor(self.app, nome_loja=loja["nome"], callback_confirmar=salvar)
        editor.carregar_tema_existente(tema_existente)

    def excluir_loja(self, loja, menu):
        menu.destroy()
        if messagebox.askyesno("Excluir Loja", f"Deseja excluir '{loja['nome']}'?"):
            if crud_lojas.excluir_loja(loja["id"]):
                self.image_cache.clear()
                self.carregar_lojas_usuario()
                self.renderizar_minhas_lojas()

    def sair_da_loja(self, loja, menu):
        menu.destroy()
        if messagebox.askyesno("Sair da Loja", f"Sair de '{loja['nome']}'?"):
            if crud_lojas.remover_usuario_da_loja(sessao.usuario_id, loja["id"]):
                self.carregar_lojas_usuario()
                self.renderizar_minhas_lojas()

    def criar_loja(self):
        from data.tema import ThemeEditor
        def confirmar_tema(tema):
            nome = tema.get("NOME_LOJA")
            if not nome:
                messagebox.showerror("Erro", "Informe o nome da loja")
                return

            # Primeiro cria a loja básica
            logo_blob = None
            logo_path = tema.get("LOGO_IMG")
            if logo_path and os.path.exists(logo_path):
                with open(logo_path, "rb") as f:
                    logo_blob = f.read()

            loja_id = crud_lojas.criar_loja(nome, logo_blob=logo_blob)
            if not loja_id:
                messagebox.showerror("Erro", "Falha ao criar loja")
                return

            crud_lojas.salvar_tema_loja(loja_id, tema)
            crud_lojas.associar_usuario_a_loja(sessao.usuario_id, loja_id, "Administrador")

            self.image_cache.clear()
            self.carregar_lojas_usuario()
            self.renderizar_minhas_lojas()
            messagebox.showinfo("Sucesso", "Loja criada com sucesso!")

        ThemeEditor(self.app, nome_loja="", callback_confirmar=confirmar_tema)

    def entrar_loja_id(self, loja):
        self.carregar_sessao_loja(loja)

    def entrar_loja(self):
        lojas = crud_lojas.listar_lojas()
        if not lojas:
            messagebox.showinfo("Lojas", "Nenhuma loja disponível.")
            return
        janela = ctk.CTkToplevel(self.app)
        janela.title("Selecionar Loja")
        janela.geometry("500x400")
        frame = ctk.CTkScrollableFrame(janela)
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        for loja in lojas:
            ctk.CTkButton(frame, text=f"{loja['id']} - {loja['nome']}",
                          command=lambda l=loja: self._selecionar_loja_externa(l, janela)).pack(fill="x", pady=5)

    def _selecionar_loja_externa(self, loja, janela):
        janela.destroy()
        loja_db = crud_lojas.entrar_em_loja(loja["id"], sessao.usuario_id)
        if not loja_db:
            crud_lojas.associar_usuario_a_loja(sessao.usuario_id, loja["id"], "Caixa")
            loja_db = crud_lojas.entrar_em_loja(loja["id"], sessao.usuario_id)
        self.carregar_sessao_loja(loja_db)

    def carregar_sessao_loja(self, loja):
        dados_visuais = crud_lojas.buscar_dados_visuais(loja["id"])
        sessao.funcionario_id = loja["id_funcionario"]
        sessao.loja_id = loja["id"]
        sessao.perfil = loja["perfil"]
        sessao.nome_loja = loja["nome"]

        tema_raw = dados_visuais.get("Tema_JSON")
        tema = json.loads(tema_raw) if tema_raw else None

        if tema:
            nome_seguro = re.sub(r'[^a-zA-Z0-9_]', '', sessao.nome_loja.lower().replace(" ", "_"))
            caminho = f"cache_temas/{nome_seguro}_{sessao.loja_id}.json"
            os.makedirs("cache_temas", exist_ok=True)
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(tema, f, indent=4, ensure_ascii=False)
            import data.colors as colors
            colors.aplicar_tema_customizado(tema)

        mostrar_menu(self.app, sessao.nome, sessao.perfil)

    def logout(self):
        from custompdv import mostrar_login
        import data.colors as colors
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            colors.resetar_tema()
            sessao.usuario_id = None
            sessao.nome = None
            sessao.funcionario_id = None
            sessao.perfil = None
            sessao.loja_id = None
            sessao.nome_loja = None
            mostrar_login(self.app)

def mostrar_lojas(app):
    LojaApp(app)