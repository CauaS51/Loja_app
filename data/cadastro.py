import customtkinter as ctk
from tkinter import messagebox
import data.colors as colors
from data.colors import *
import data.sessao as sessao
from crud.crud_cadastros import excluir_usuario, listar_cadastros, cadastrar_usuario

class AreaCadastrosApp:
    def __init__(self, app):
        self.app = app
        self.cores = colors.get_colors()
        self.gerar_tela_unificada()

    def gerar_tela_unificada(self):
        # Limpa a tela
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Gerenciamento de Usuários")
        
        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=self.cores["PRIMARY"], height=70, corner_radius=0)
        header.pack(fill="x")
        
        btn_voltar = ctk.CTkButton(header, text="⬅", width=40, height=40, corner_radius=12,
                                   fg_color=self.cores["ENTRY_BG"], hover_color=self.cores["HOVER"],
                                   text_color=self.cores["TEXT_PRIMARY"], command=self.voltar_menu)
        btn_voltar.pack(side="left", padx=20, pady=15)

        title_label = ctk.CTkLabel(header, text="📊 Gestão de Funcionários", text_color="white",
                                   font=ctk.CTkFont("Segoe UI", 24, "bold"))
        title_label.pack(side="left", padx=10)

        # === ÁREA PRINCIPAL (Grid 2 Colunas) ===
        container = ctk.CTkFrame(self.app, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1) # Coluna Form
        container.grid_columnconfigure(1, weight=2) # Coluna Tabela
        container.grid_rowconfigure(0, weight=1)

        # --- COLUNA 1: FORMULÁRIO ---
        self.frame_form = ctk.CTkFrame(container, fg_color=self.cores["CARD_BG"], corner_radius=15)
        self.frame_form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(self.frame_form, text="📝 Novo Cadastro", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.ent_nome = self.criar_campo(self.frame_form, "Nome do Funcionário:")
        self.ent_login = self.criar_campo(self.frame_form, "Nome de Usuário:")
        self.ent_senha = self.criar_campo(self.frame_form, "Senha:", is_password=True)

        # Dropdown Perfil
        ctk.CTkLabel(self.frame_form, text="Perfil de Acesso:", text_color=self.cores["TEXT_PRIMARY"]).pack(pady=(10, 0))
        self.opcoes_perfil = {"Desenvolvedor": 1, "Caixa": 2, "Repositor": 3, "Gestor de Dados": 4}
        self.perfil_var = ctk.StringVar(value="Selecione o perfil")
        self.dropdown = ctk.CTkOptionMenu(self.frame_form, values=list(self.opcoes_perfil.keys()),
                                         variable=self.perfil_var, fg_color=self.cores["PRIMARY"],
                                         button_color=self.cores["PRIMARY"], button_hover_color=self.cores["HOVER"])
        self.dropdown.pack(pady=(5, 20), fill="x", padx=30)

        btn_salvar = ctk.CTkButton(self.frame_form, text="Confirmar Cadastro", height=45,
                                   font=("Segoe UI", 14, "bold"), fg_color=self.cores["PRIMARY"],
                                   command=self.salvar_e_atualizar)
        btn_salvar.pack(pady=10, fill="x", padx=30)

        # --- COLUNA 2: LISTAGEM ---
        self.frame_lista = ctk.CTkFrame(container, fg_color=self.cores["CARD_BG"], corner_radius=15)
        self.frame_lista.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(self.frame_lista, text="👥 Usuários Ativos", font=("Segoe UI", 18, "bold")).pack(pady=20)

        # Scrollable Frame para os dados
        self.scroll_lista = ctk.CTkScrollableFrame(self.frame_lista, fg_color="transparent")
        self.scroll_lista.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.atualizar_lista_interface()

    def criar_campo(self, frame, label_text, is_password=False):
        ctk.CTkLabel(frame, text=label_text, text_color=self.cores["TEXT_PRIMARY"]).pack(anchor="w", padx=30, pady=(10, 0))
        entry = ctk.CTkEntry(frame, height=35, show="*" if is_password else "")
        entry.pack(pady=(5, 5), fill="x", padx=30)
        return entry

    def atualizar_lista_interface(self):
        # Limpa o scroll
        for w in self.scroll_lista.winfo_children():
            w.destroy()

        # Cabeçalho da Tabela
        h_frame = ctk.CTkFrame(self.scroll_lista, fg_color="transparent", height=30)
        h_frame.pack(fill="x", pady=5)
        headers = [("ID", 50), ("Funcionário", 180), ("Login", 120), ("Perfil", 100)]
        for text, width in headers:
            ctk.CTkLabel(h_frame, text=text, width=width, font=("Segoe UI", 12, "bold"), anchor="w").pack(side="left", padx=5)

        # Dados
        usuarios = listar_cadastros()
        for user in usuarios:
            linha = ctk.CTkFrame(self.scroll_lista, fg_color=self.cores["BACKGROUND"], corner_radius=8)
            linha.pack(fill="x", pady=2, padx=5)

            ctk.CTkLabel(linha, text=user["id"], width=50).pack(side="left", padx=5)
            ctk.CTkLabel(linha, text=user["nome"], width=180, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(linha, text=user["login"], width=120, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(linha, text=user["perfil"], width=100, anchor="w").pack(side="left", padx=5)

            btn_del = ctk.CTkButton(linha, text="🗑️", width=30, height=30, fg_color="#E74C3C", 
                                    hover_color="#C0392B", command=lambda u_id=user["id"]: self.excluir_e_atualizar(u_id))
            btn_del.pack(side="right", padx=10, pady=5)

    def salvar_e_atualizar(self):
        nome = self.ent_nome.get()
        login = self.ent_login.get()
        senha = self.ent_senha.get()
        perfil_txt = self.perfil_var.get()

        if not nome or not login or not senha or perfil_txt == "Selecione o perfil":
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        id_perfil = self.opcoes_perfil[perfil_txt]
        if cadastrar_usuario(nome, login, senha, id_perfil):
            messagebox.showinfo("Sucesso", "Usuário cadastrado!")
            self.ent_nome.delete(0, 'end'); self.ent_login.delete(0, 'end'); self.ent_senha.delete(0, 'end')
            self.perfil_var.set("Selecione o perfil")
            self.atualizar_lista_interface()

    def excluir_e_atualizar(self, u_id):
        if messagebox.askyesno("Confirmar", f"Excluir usuário ID {u_id}?"):
            if excluir_usuario(u_id):
                self.atualizar_lista_interface()

    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app, usuario=sessao.nome, perfil=sessao.perfil)

def abrir_cadastro(app):
    AreaCadastrosApp(app)