import customtkinter as ctk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageOps
import os

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

        # ================== TEMAS PADRÃO ==================
        self.tema_light_default = {
            "PRIMARY": "#E98C41", "SECONDARY": "#2F80ED", "HOVER": "#E2B539",
            "BACKGROUND": "#F5F5F5", "BACKGROUND_2": "#FFFFFF", "CARD_BG": "#FFFFFF",
            "TEXT_PRIMARY": "#333333", "TEXT_SECONDARY": "#666666", "ENTRY_BG": "#E0E0E0",
            "CARD_CAIXA": "#36A84A", "CARD_ESTOQUE": "#2F80ED", "CARD_RELATORIOS": "#F2994A",
            "CARD_CADASTROS": "#7C4DFF", "LOGO": "🏬", "LOGO_IMG": None
        }

        self.tema_dark_default = {
            "PRIMARY": "#3F71A6", "SECONDARY": "#1856FF", "HOVER": "#00388D",
            "BACKGROUND": "#2C2C2C", "BACKGROUND_2": "#4D80B9", "CARD_BG": "#1E1E1E",
            "TEXT_PRIMARY": "#FFFFFF", "TEXT_SECONDARY": "#BBBBBB", "ENTRY_BG": "#333333",
            "CARD_CAIXA": "#36A84A", "CARD_ESTOQUE": "#2F80ED", "CARD_RELATORIOS": "#F2994A",
            "CARD_CADASTROS": "#7C4DFF", "LOGO": "🏬", "LOGO_IMG": None
        }

        self.modo_preview = "Light"
        self.tema_light = self.tema_light_default.copy()
        self.tema_dark = self.tema_dark_default.copy()
        self.tema = self.tema_light 

        self.logo_img_light = None
        self.logo_img_dark = None
        self.color_buttons = {}

        self.center_window()
        self.criar_interface()

    def center_window(self):
        self.update_idletasks()
        w, h = 950, 650
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def criar_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ================= COLUNA ESQUERDA =================
        left_panel = ctk.CTkFrame(self, corner_radius=0, fg_color=None)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(left_panel, text="Customização", font=("Segoe UI", 22, "bold")).pack(pady=(0, 5), anchor="w")

        # Seletor de Tema (Toggle)
        self.switch_tema = ctk.CTkSegmentedButton(left_panel, values=["Light", "Dark"],
                                                command=self.alternar_preview_segmented)
        self.switch_tema.set("Light")
        self.switch_tema.pack(pady=(0, 20), fill="x")

        scroll_colors = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
        scroll_colors.pack(expand=True, fill="both")

        self.criar_secao_cor(scroll_colors, "Cores Principais", ["PRIMARY", "SECONDARY", "HOVER", "BACKGROUND"])
        self.criar_secao_cor(scroll_colors, "Cores dos Cards", ["CARD_CAIXA", "CARD_ESTOQUE", "CARD_RELATORIOS", "CARD_CADASTROS"])
        self.criar_secao_cor(scroll_colors, "Interface e Texto", ["TEXT_PRIMARY", "TEXT_SECONDARY", "CARD_BG", "ENTRY_BG"])

        # Ações
        actions_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(10, 0))

        ctk.CTkButton(actions_frame, text="Resetar", fg_color="#E74C3C", hover_color="#C0392B", 
                      width=80, command=self.resetar_tema).pack(side="left", padx=5)
        
        # Botão Salvar - Já configurado para fechar a janela no comando confirmar
        ctk.CTkButton(actions_frame, text="Salvar Alterações", fg_color="#27AE60", hover_color="#1E8449",
                      font=("Segoe UI", 13, "bold"), command=self.confirmar).pack(side="right", fill="x", expand=True, padx=5)

        # ================= COLUNA DIREITA (PREVIEW) =================
        self.right_panel = ctk.CTkFrame(self, corner_radius=20)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.preview_header = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.preview_header.pack(fill="x", padx=20, pady=20)

        self.logo_container = ctk.CTkFrame(self.preview_header, width=100, height=100, corner_radius=50)
        self.logo_container.pack(side="left")
        self.logo_container.pack_propagate(False)
        
        self.lbl_logo_preview = ctk.CTkLabel(self.logo_container, text="🏬", font=("Segoe UI", 40))
        self.lbl_logo_preview.pack(expand=True)
        
        info_frame = ctk.CTkFrame(self.preview_header, fg_color="transparent")
        info_frame.pack(side="left", padx=20)
        
        self.nome_entry = ctk.CTkEntry(info_frame, placeholder_text="Nome da Loja", width=250, font=("Segoe UI", 16, "bold"))
        self.nome_entry.insert(0, self.nome_loja)
        self.nome_entry.pack(pady=2)

        self.desc_entry = ctk.CTkEntry(info_frame, placeholder_text="Slogan ou Descrição", width=250)
        self.desc_entry.pack(pady=2)
        
        ctk.CTkButton(self.preview_header, text="Alterar Logo", width=100, command=self.escolher_logo).pack(side="right", padx=10)

        self.cards_container = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.cards_container.pack(expand=True, fill="both", padx=20, pady=10)
        self.cards_container.grid_columnconfigure((0,1), weight=1)

        nomes_cards = ["Vendas", "Estoque", "Financeiro", "Config"]
        icones = ["💰", "📦", "📊", "⚙️"]
        self.preview_cards_list = []

        for i, (nome, icone) in enumerate(zip(nomes_cards, icones)):
            card = ctk.CTkFrame(self.cards_container, corner_radius=12, height=100)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            card.pack_propagate(False)
            
            lbl_i = ctk.CTkLabel(card, text=icone, font=("Segoe UI", 24))
            lbl_i.pack(pady=(15, 0))
            lbl_t = ctk.CTkLabel(card, text=nome, font=("Segoe UI", 13, "bold"))
            lbl_t.pack()
            
            # Guardamos o card e seus elementos para atualizar cores depois
            self.preview_cards_list.append({
                "frame": card,
                "labels": [lbl_i, lbl_t],
                "tipo": f"CARD_{['CAIXA', 'ESTOQUE', 'RELATORIOS', 'CADASTROS'][i]}"
            })

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
            self.color_buttons[chave] = btn_color

    def carregar_tema_existente(self, tema):
        if not tema: return
        if "NOME_LOJA" in tema:
            self.nome_entry.delete(0, "end"); self.nome_entry.insert(0, tema["NOME_LOJA"])
        if "DESCRICAO" in tema:
            self.desc_entry.delete(0, "end"); self.desc_entry.insert(0, tema["DESCRICAO"])

        if "Light" in tema: self.tema_light = tema["Light"].copy()
        if "Dark" in tema: self.tema_dark = tema["Dark"].copy()

        self.tema = self.tema_light
        self.switch_tema.set("Light")
        
        caminho_logo = tema.get("LOGO_IMG")
        if caminho_logo and os.path.exists(caminho_logo):
            self.logo_img_light = self.carregar_imagem_preview(caminho_logo)
            self.logo_img_dark = self.logo_img_light
        
        self.sincronizar_cores_botoes()
        self.atualizar_preview()

    def alternar_preview_segmented(self, modo):
        if self.modo_preview == "Light": self.tema_light = self.tema.copy()
        else: self.tema_dark = self.tema.copy()

        self.modo_preview = modo
        self.tema = self.tema_light if modo == "Light" else self.tema_dark
        self.sincronizar_cores_botoes()
        self.atualizar_preview()

    def sincronizar_cores_botoes(self):
        for chave, btn in self.color_buttons.items():
            if chave in self.tema: btn.configure(fg_color=self.tema[chave])

    def atualizar_preview(self):
        self.right_panel.configure(fg_color=self.tema["BACKGROUND"])
        self.nome_entry.configure(fg_color=self.tema["ENTRY_BG"], text_color=self.tema["TEXT_PRIMARY"])
        self.desc_entry.configure(fg_color=self.tema["ENTRY_BG"], text_color=self.tema["TEXT_PRIMARY"])
        
        # Atualiza os cards com as novas cores e redefine o efeito de Hover
        for item in self.preview_cards_list:
            cor_base = self.tema[item["tipo"]]
            cor_hover = self.tema["HOVER"]
            
            item["frame"].configure(fg_color=cor_base)
            for lbl in item["labels"]:
                lbl.configure(text_color="white", bg_color=cor_base)

            # Bind dinâmico para o efeito Hover
            item["frame"].bind("<Enter>", lambda e, f=item["frame"], c=cor_hover: f.configure(fg_color=c))
            item["frame"].bind("<Leave>", lambda e, f=item["frame"], c=cor_base: f.configure(fg_color=c))
            for lbl in item["labels"]:
                lbl.bind("<Enter>", lambda e, f=item["frame"], c=cor_hover: f.configure(fg_color=c))
                lbl.bind("<Leave>", lambda e, f=item["frame"], c=cor_base: f.configure(fg_color=c))

        img_atual = self.logo_img_light if self.modo_preview == "Light" else self.logo_img_dark
        self.lbl_logo_preview.configure(image=img_atual, text="" if img_atual else self.tema.get("LOGO", "🏬"))

    def escolher_cor(self, chave):
        cor = colorchooser.askcolor(title=f"Escolher {chave}", initialcolor=self.tema[chave])[1]
        if cor:
            self.tema[chave] = cor
            self.color_buttons[chave].configure(fg_color=cor)
            self.atualizar_preview()

    def escolher_logo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens","*.png *.jpg *.jpeg")])
        if caminho:
            img_ctk = self.carregar_imagem_preview(caminho)
            self.tema["LOGO_IMG"] = caminho
            if self.modo_preview == "Light": self.logo_img_light = img_ctk
            else: self.logo_img_dark = img_ctk
            self.atualizar_preview()

    def carregar_imagem_preview(self, caminho):
        try:
            img_pil = Image.open(caminho)
            img_fit = ImageOps.fit(img_pil, (100, 100), Image.Resampling.LANCZOS)
            return ctk.CTkImage(light_image=img_fit, dark_image=img_fit, size=(100,100))
        except: return None

    def resetar_tema(self):
        if messagebox.askyesno("Confirmar", "Resetar este modo para o padrão?"):
            self.tema = self.tema_light_default.copy() if self.modo_preview == "Light" else self.tema_dark_default.copy()
            self.sincronizar_cores_botoes(); self.atualizar_preview()

    def confirmar(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Dê um nome para sua loja!")
            return
        
        # Salva o estado atual
        if self.modo_preview == "Light": self.tema_light = self.tema.copy()
        else: self.tema_dark = self.tema.copy()

        dados_finais = {
            "NOME_LOJA": nome,
            "DESCRICAO": self.desc_entry.get(),
            "LOGO_IMG": self.tema.get("LOGO_IMG"),
            "Light": self.tema_light,
            "Dark": self.tema_dark
        }
        
        if self.callback_confirmar:
            self.callback_confirmar(dados_finais)
        
        # Fecha a janela automaticamente
        self.destroy()