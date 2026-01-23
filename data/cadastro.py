import customtkinter as ctk
from tkinter import messagebox
import data.colors as colors
from data.colors import *
import data.sessao as sessao
from crud.crud_cadastros import excluir_usuario

# MENU DE CADASTROS
class AreaCadastrosApp:
    def __init__(self, app):
        self.app = app
        self.gerar_tela_area_cadastros()

    def gerar_tela_area_cadastros(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Área de Cadastros")
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        # BOTÃO VOLTAR
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.voltar_menu
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # TÍTULO
        title_label = ctk.CTkLabel(
            header, text="🗂 Área de Cadastros",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=1, padx=(0,30), pady=20, sticky="w")

        # BOTÃO ALTERNAR TEMA
        def alternar_tema():
            colors.alternar_tema()
            self.gerar_tela_area_cadastros()

        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        theme_button = ctk.CTkButton(
            header,
            text=icone_tema,
            width=40,
            height=40,
            corner_radius=12,
            fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"],
            font=ctk.CTkFont(size=25),
            command=alternar_tema
        )
        theme_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # === CONTEÚDO PRINCIPAL ===
        main_frame = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        main_frame.grid_columnconfigure(0, weight=1)

        # BOTÃO REALIZAR CADASTRO
        btn_realizar = ctk.CTkButton(
            main_frame, text="➕ Realizar Cadastro",
            fg_color=cores["PRIMARY"], hover_color=cores["HOVER"], text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"), height=50,
            command=self.abrir_tela_cadastro
        )
        btn_realizar.pack(pady=20, padx=60, fill="x")

        # BOTÃO MOSTRAR CADASTROS
        btn_listar = ctk.CTkButton(
            main_frame, text="📋 Mostrar Cadastros",
            fg_color=cores["PRIMARY"], hover_color=cores["HOVER"], text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"), height=50,
            command=self.abrir_tela_listagem
        )
        btn_listar.pack(pady=20, padx=60, fill="x")

    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app, usuario=sessao.usuario, perfil=sessao.perfil)

    def abrir_tela_cadastro(self):
        CadastroUsuariosApp(self.app)

    def abrir_tela_listagem(self):
        ListaUsuariosApp(self.app)
        
def abrir_cadastro(app):
    AreaCadastrosApp(app)

#=========================================================================================
#=========================================================================================

# USUÁRIOS CADASTRADOS
class ListaUsuariosApp:
    def __init__(self, app):
        self.app = app
        self.gerar_tela_lista()

    def gerar_tela_lista(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Usuários Cadastrados")
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        # BOTÃO VOLTAR
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.voltar_menu
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # TÍTULO
        title_label = ctk.CTkLabel(
            header, text="👥 Usuários Cadastrados",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=1, padx=(0,30), pady=20, sticky="w")

        # BOTÃO ALTERNAR TEMA
        def alternar_tema():
            colors.alternar_tema()
            self.gerar_tela_lista()

        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        theme_button = ctk.CTkButton(
            header,
            text=icone_tema,
            width=40,
            height=40,
            corner_radius=12,
            fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"],
            font=ctk.CTkFont(size=25),
            command=alternar_tema
        )
        theme_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # === CONTEÚDO PRINCIPAL ===
        main_frame = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        main_frame.grid_columnconfigure(0, weight=1)

        # LISTA DE USUÁRIOS (BANCO DE DADOS)
        from crud.crud_cadastros import listar_cadastros
        usuarios = listar_cadastros()
        
        # SCROLL FRAME
        lista_frame = ctk.CTkScrollableFrame(main_frame, fg_color=cores["CARD_BG"], corner_radius=12)
        lista_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # TÍTULOS DAS COLUNAS
        header_row = ctk.CTkFrame(lista_frame, fg_color="transparent")
        header_row.pack(fill="x", pady=5)
        ctk.CTkLabel(header_row, text="ID", width=50, font=("Segoe UI", 16, "bold")).grid(row=0, column=0)
        ctk.CTkLabel(header_row, text="Funcionário", width=200, font=("Segoe UI", 16, "bold")).grid(row=0, column=1)
        ctk.CTkLabel(header_row, text="Usuário", width=150, font=("Segoe UI", 16, "bold")).grid(row=0, column=2)
        ctk.CTkLabel(header_row, text="Perfil", width=100, font=("Segoe UI", 16, "bold")).grid(row=0, column=3)
        ctk.CTkLabel(header_row, text="Ações", width=80, font=("Segoe UI", 16, "bold")).grid(row=0, column=4)


        # LINHAS COM USUÁRIOS
        for user in usuarios:
            linha = ctk.CTkFrame(lista_frame, fg_color="transparent")
            linha.pack(fill="x", pady=3)

            ctk.CTkLabel(linha, text=user["id"], width=50).grid(row=0, column=0)
            ctk.CTkLabel(linha, text=user["nome"], width=200).grid(row=0, column=1)
            ctk.CTkLabel(linha, text=user["login"], width=150).grid(row=0, column=2)
            ctk.CTkLabel(linha, text=user["perfil"], width=100).grid(row=0, column=3)

            # === BOTÃO LIXEIRA ===
            btn_excluir = ctk.CTkButton(
                linha,
                text="🗑️",
                width=40,
                height=30,
                fg_color="red",
                hover_color="#ff6666",
                command=lambda u_id=user["id"]: self.confirmar_exclusao(u_id)
            )
            btn_excluir.grid(row=0, column=4, padx=5)

    def voltar_menu(self):
        from data.cadastro import AreaCadastrosApp
        AreaCadastrosApp(self.app)

    def confirmar_exclusao(self, id_funcionario):
        resposta = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja excluir o usuário de ID {id_funcionario}?"
        )
        if resposta:
            sucesso = excluir_usuario(id_funcionario)
            if sucesso:
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.gerar_tela_lista()  # Atualiza a lista
            else:
                messagebox.showerror("Erro", "Falha ao excluir usuário.")


def consultar_cadastros(app):
    ListaUsuariosApp(app)

#=========================================================================================
#=========================================================================================

# CADASTRO DE USUÁRIO
class CadastroUsuariosApp:
    def __init__(self, app):
        self.app = app
        self.gerar_tela_cadastro()

    def gerar_tela_cadastro(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Cadastro de Usuário")
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        # BOTÃO VOLTAR
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.voltar_menu
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # TÍTULO
        title_label = ctk.CTkLabel(
            header, text="🗂 Cadastro de Usuário",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=1, padx=(0,30), pady=20, sticky="w")

        # BOTÃO ALTERNAR TEMA
        def alternar_tema():
            colors.alternar_tema()
            self.gerar_tela_cadastro()

        icone_tema = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        theme_button = ctk.CTkButton(
            header,
            text=icone_tema,
            width=40,
            height=40,
            corner_radius=12,
            fg_color=cores["ENTRY_BG"],
            hover_color=cores["HOVER"],
            text_color=cores["TEXT_PRIMARY"],
            font=ctk.CTkFont(size=25),
            command=alternar_tema
        )
        theme_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # === CONTEÚDO PRINCIPAL ===
        main_frame = ctk.CTkFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        main_frame.grid_columnconfigure(0, weight=1)

        # CAMPOS DO FORMULÁRIO
        self.entry_id_usuario = self.criar_campo(main_frame, "ID Usuário:", placeholder="Gerado automaticamente", readonly=True)
        self.entry_nome_funcionario = self.criar_campo(main_frame, "Nome do Funcionário:")
        self.entry_nome_usuario = self.criar_campo(main_frame, "Nome de Usuário:")
        self.entry_senha = self.criar_campo(main_frame, "Senha:", is_password=True)

        # CAMPO ID DO PERFIL (DROPDOWN)
        ctk.CTkLabel(main_frame, text="ID Perfil:", text_color=cores["TEXT_PRIMARY"]).pack(pady=(10, 0))
        
        # OPÇÕES DE PERFIL
        self.opcoes_perfil = {
            "Desenvolvedor": 1,
            "Caixa": 2,
            "Repositor": 3,
            "Gestor de Dados": 4
        }

        self.perfil_var = ctk.StringVar(value="Selecione o perfil")
        self.dropdown_perfil = ctk.CTkOptionMenu(
            main_frame,
            values=list(self.opcoes_perfil.keys()),
            variable=self.perfil_var,
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            text_color="white",
            fg_color=cores["PRIMARY"],
            button_color=cores["PRIMARY"],
            button_hover_color=cores["HOVER"]

        )
        self.dropdown_perfil.pack(pady=(0,10), fill="x", padx=20)

        # BOTÃO SALVAR
        btn_salvar = ctk.CTkButton(
            main_frame, text="Salvar Cadastro",
            fg_color=cores["PRIMARY"], hover_color=cores["HOVER"],
            text_color="white", font=ctk.CTkFont(size=16, weight="bold"),
            command=self.salvar_cadastro  
        )
        btn_salvar.pack(pady=20, fill="x", padx=20)

    def criar_campo(self, frame, label_text, placeholder="", readonly=False, is_password=False):
        cores = colors.get_colors()
        ctk.CTkLabel(frame, text=label_text, text_color=cores["TEXT_PRIMARY"]).pack(pady=(10, 0))
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, show="*" if is_password else "")
        entry.pack(pady=(0,10), fill="x", padx=20)
        if readonly:
            entry.configure(state="disabled")
        return entry

    def salvar_cadastro(self):
        nome = self.entry_nome_funcionario.get()
        usuario = self.entry_nome_usuario.get()
        senha = self.entry_senha.get()
        
        perfil_selecionado = self.perfil_var.get()
        if perfil_selecionado not in self.opcoes_perfil:
            messagebox.showwarning("Aviso", "Selecione um perfil válido!")
            return

        id_perfil = self.opcoes_perfil[perfil_selecionado]
        

        if not nome or not usuario or not senha or not id_perfil:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        from crud.crud_cadastros import cadastrar_usuario

        sucesso = cadastrar_usuario(nome, usuario, senha, id_perfil)

        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

            self.entry_nome_funcionario.delete(0, "end")
            self.entry_nome_usuario.delete(0, "end")
            self.entry_senha.delete(0, "end")
            self.perfil_var.set("Selecione o perfil")

            self.voltar_menu()

        else:
            messagebox.showerror("Erro", "Falha ao cadastrar usuário.")

    def voltar_menu(self):
        from data.cadastro import AreaCadastrosApp
        import custompdv
        if sessao.usuario == None and sessao.perfil == None:
            custompdv.mostrar_login(self.app)
        else:
            AreaCadastrosApp(self.app)

def cadastro_login(app):
    CadastroUsuariosApp(app)
    
#=========================================================================================
#=========================================================================================