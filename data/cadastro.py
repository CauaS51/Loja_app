import customtkinter as ctk
from tkinter import messagebox
import data.colors as colors
from crud.crud_cadastros import cadastrar_usuario
import re

class TelaCadastroConta:
    def __init__(self, app):
        self.app = app
        self.cores = colors.get_colors()
        
        # Variáveis de controle com rastreamento (Traces)
        self.var_nome = ctk.StringVar()
        self.var_login = ctk.StringVar()
        self.var_email = ctk.StringVar()
        self.var_telefone = ctk.StringVar()
        self.var_cpf = ctk.StringVar()
        
        # Aplicar máscaras automáticas
        self.var_cpf.trace_add("write", self.mascara_cpf)
        self.var_telefone.trace_add("write", self.mascara_telefone)
        self.var_nome.trace_add("write", self.validar_nome)

        self.montar_tela()

    def montar_tela(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Sistema PDV | Cadastro de Operador")

        # HEADER (Igual ao Caixa)
        self.criar_header()

        # CONTAINER PRINCIPAL
        main_container = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND"])
        main_container.pack(fill="both", expand=True)

        # CARD CENTRAL (Largura fixa para parecer um formulário profissional)
        card = ctk.CTkFrame(main_container, width=550, corner_radius=20, fg_color=self.cores["CARD_BG"])
        card.place(relx=0.5, rely=0.5, anchor="center")

        # TÍTULO INTERNO
        ctk.CTkLabel(card, text="📝 Registro de Funcionário", 
                     font=("Segoe UI", 24, "bold"), text_color=self.cores["PRIMARY"]).pack(pady=(30, 5))
        ctk.CTkLabel(card, text="Informe os dados para acesso ao terminal", 
                     font=("Segoe UI", 13), text_color=self.cores["TEXT_SECONDARY"]).pack(pady=(0, 25))

        # GRID DE FORMULÁRIO (2 Colunas para otimizar espaço)
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(fill="x", padx=40)
        form_frame.grid_columnconfigure((0, 1), weight=1, pad=20)

        # CAMPOS
        self.ent_nome = self.criar_campo(form_frame, "Nome Completo*", self.var_nome, 0, 0, colspan=2)
        self.ent_email = self.criar_campo(form_frame, "E-mail Corporativo*", self.var_email, 1, 0, colspan=2)
        
        self.ent_login = self.criar_campo(form_frame, "Usuário (Login)*", self.var_login, 2, 0)
        self.ent_cpf = self.criar_campo(form_frame, "CPF (Somente números)*", self.var_cpf, 2, 1)
        
        self.ent_tel = self.criar_campo(form_frame, "Telefone", self.var_telefone, 3, 0)
        self.ent_senha = self.criar_campo(form_frame, "Senha*", None, 3, 1, senha=True)

        # BOTÕES (Estilo PDV)
        self.btn_cadastrar = ctk.CTkButton(card, text="CONFIRMAR CADASTRO", height=50,
                                         font=("Segoe UI", 16, "bold"), fg_color=self.cores["PRIMARY"],
                                         hover_color=self.cores["HOVER"], command=self.executar_cadastro)
        self.btn_cadastrar.pack(pady=(30, 10), padx=40, fill="x")

        ctk.CTkButton(card, text="CANCELAR", height=40, fg_color="transparent",
                     border_width=2, border_color="#FF4B4B", text_color="#FF4B4B",
                     command=self.voltar).pack(pady=(0, 30), padx=40, fill="x")

    def criar_header(self):
        header = ctk.CTkFrame(self.app, fg_color=self.cores["PRIMARY"], height=70)
        header.pack(fill="x")
        
        ctk.CTkLabel(header, text="🛡️ Cadastrar-se", 
                     font=("Segoe UI", 20, "bold"), text_color="white").pack(side="left", padx=20)

    def criar_campo(self, master, texto, variavel, row, col, colspan=1, senha=False):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=10)
        
        ctk.CTkLabel(frame, text=texto, font=("Segoe UI", 12, "bold"), 
                     text_color=self.cores["TEXT_PRIMARY"]).pack(anchor="w")
        
        entry = ctk.CTkEntry(frame, height=40, textvariable=variavel, 
                            show="*" if senha else "", fg_color=self.cores["ENTRY_BG"])
        entry.pack(fill="x", pady=2)
        return entry

    # ==================== MÁSCARAS E VALIDAÇÕES ====================
    
    def mascara_cpf(self, *args):
        valor = re.sub(r'\D', '', self.var_cpf.get())[:11]
        if len(valor) > 9: valor = f"{valor[:3]}.{valor[3:6]}.{valor[6:9]}-{valor[9:]}"
        elif len(valor) > 6: valor = f"{valor[:3]}.{valor[3:6]}.{valor[6:]}"
        elif len(valor) > 3: valor = f"{valor[:3]}.{valor[3:]}"
        self.var_cpf.set(valor)

    def mascara_telefone(self, *args):
        valor = re.sub(r'\D', '', self.var_telefone.get())[:11]
        if len(valor) == 11: valor = f"({valor[:2]}) {valor[2:7]}-{valor[7:]}"
        elif len(valor) > 2: valor = f"({valor[:2]}) {valor[2:]}"
        self.var_telefone.set(valor)

    def validar_nome(self, *args):
        # Remove números do nome automaticamente
        valor = re.sub(r'[0-9]', '', self.var_nome.get())
        self.var_nome.set(valor)

    # ==================== LÓGICA DE ENVIO ====================

    def executar_cadastro(self):
        # Coleta de dados
        dados = {
            "nome": self.var_nome.get().strip(),
            "login": self.var_login.get().strip(),
            "email": self.var_email.get().strip(),
            "cpf": re.sub(r'\D', '', self.var_cpf.get()),
            "senha": self.ent_senha.get().strip(),
            "tel": self.var_telefone.get().strip()
        }

        # Validação simples
        if not all([dados["nome"], dados["login"], dados["cpf"], dados["senha"]]):
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos com asterisco (*).")
            return

        if len(dados["cpf"]) != 11:
            messagebox.showerror("CPF Inválido", "O CPF deve conter 11 dígitos.")
            return

        # Chamada do CRUD (Mesma lógica que você já tinha)
        if cadastrar_usuario(dados["nome"], dados["login"], dados["senha"], 
                            dados["email"], dados["tel"], dados["cpf"]):
            messagebox.showinfo("Sucesso", f"Operador {dados['login']} cadastrado!")
            self.voltar()

    def voltar(self):
        from custompdv import mostrar_login
        mostrar_login(self.app)

def abrir_cadastro(app):
    TelaCadastroConta(app)











import customtkinter as ctk
from tkinter import messagebox
import data.sessao as sessao
import data.colors as colors
# Nomes corrigidos para importar exatamente o que está no seu CRUD
from crud.crud_cadastros import listar_funcionarios_da_loja, remover_funcionario, atualizar_perfil_funcionario

class TelaListarFuncionarios:
    def __init__(self, app):
        self.app = app
        self.cores = sessao.tema_loja if hasattr(sessao, 'tema_loja') and sessao.tema_loja else colors.get_colors()
        self.montar_tela()

    def montar_tela(self):
        for w in self.app.winfo_children(): w.destroy()

        # HEADER
        header = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND_2"], height=70, corner_radius=15)
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(header, text="⬅ Voltar", width=100, command=self.voltar, 
                      fg_color=self.cores["PRIMARY"]).pack(side="left", padx=20)
        
        ctk.CTkLabel(header, text=f"👥 Equipe: {sessao.nome_loja}", 
                     font=("Segoe UI", 20, "bold"), text_color=self.cores["TEXT_PRIMARY"]).pack(side="left")

        # CONTAINER DA TABELA
        container = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND"])
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        thead = ctk.CTkFrame(container, fg_color=self.cores["BACKGROUND_2"], height=40)
        thead.pack(fill="x", padx=10, pady=(10, 5))
        
        # Cabeçalhos
        ctk.CTkLabel(thead, text="NOME", font=("Segoe UI", 11, "bold"), text_color=self.cores["TEXT_SECONDARY"]).place(relx=0.03, rely=0.5, anchor="w")
        ctk.CTkLabel(thead, text="USUÁRIO", font=("Segoe UI", 11, "bold"), text_color=self.cores["TEXT_SECONDARY"]).place(relx=0.32, rely=0.5, anchor="w")
        ctk.CTkLabel(thead, text="ID_FUNC", font=("Segoe UI", 11, "bold"), text_color=self.cores["TEXT_SECONDARY"]).place(relx=0.52, rely=0.5, anchor="w")
        ctk.CTkLabel(thead, text="PERFIL (CLIQUE P/ ALTERAR)", font=("Segoe UI", 11, "bold"), text_color=self.cores["TEXT_SECONDARY"]).place(relx=0.70, rely=0.5, anchor="w")
        ctk.CTkLabel(thead, text="AÇÕES", font=("Segoe UI", 11, "bold"), text_color=self.cores["TEXT_SECONDARY"]).place(relx=0.92, rely=0.5, anchor="w")

        self.scroll = ctk.CTkScrollableFrame(container, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self.carregar_funcionarios()

    def carregar_funcionarios(self):
        for w in self.scroll.winfo_children(): w.destroy()
        
        dados = listar_funcionarios_da_loja(sessao.loja_id)
        # Ordena colocando Administradores no topo
        funcionarios = sorted(dados, key=lambda x: str(x.get('Nome_Perfil', '')).lower() == 'administrador', reverse=True)

        for func in funcionarios:
            nome_val = func.get('Nome', 'Erro')
            login_val = func.get('Login', '---')
            id_val = func.get('ID_Funcionario', '0')
            perfil_val = func.get('Nome_Perfil', 'Caixa')
            eh_adm = str(perfil_val).lower() == "administrador"
            
            line = ctk.CTkFrame(self.scroll, fg_color=self.cores["CARD_BG"], height=55, corner_radius=8)
            line.pack(fill="x", pady=2)

            # Informações Básicas
            ctk.CTkLabel(line, text=nome_val, font=("Segoe UI", 13, "bold" if eh_adm else "normal"), 
                         text_color=self.cores["PRIMARY"] if eh_adm else self.cores["TEXT_PRIMARY"]).place(relx=0.03, rely=0.5, anchor="w")
            
            ctk.CTkLabel(line, text=f"@{login_val}", text_color=self.cores["TEXT_SECONDARY"]).place(relx=0.32, rely=0.5, anchor="w")
            
            ctk.CTkLabel(line, text=str(id_val).zfill(4)).place(relx=0.52, rely=0.5, anchor="w")

            # SELEÇÃO DE PERFIL
            if eh_adm:
                # Gerente é fixo (não pode mudar o próprio cargo por aqui)
                ctk.CTkLabel(line, text="GERENTE", font=("Segoe UI", 10, "bold"), text_color="white", 
                             fg_color=self.cores["PRIMARY"], corner_radius=5, width=140, height=28).place(relx=0.70, rely=0.5, anchor="w")
            else:
                # Dropdown para mudar o cargo dos funcionários
                opcoes = ["Caixa", "Repositor", "Gestor de Dados"]
                menu_perfil = ctk.CTkOptionMenu(
                    line, values=opcoes, width=140, height=28,
                    font=("Segoe UI", 10, "bold"),
                    fg_color="#4A4A4A", button_color=self.cores["PRIMARY"],
                    command=lambda novo, f=func: self.mudar_cargo(f, novo)
                )
                menu_perfil.set(perfil_val)
                menu_perfil.place(relx=0.70, rely=0.5, anchor="w")

            # BOTÃO EXCLUIR
            if not eh_adm:
                ctk.CTkButton(line, text="✕", width=30, height=30, fg_color="#E74C3C", hover_color="#C0392B", 
                             command=lambda f=func: self.remover_equipe(f)).place(relx=0.92, rely=0.5, anchor="w")

    def mudar_cargo(self, func, novo_cargo):
        if atualizar_perfil_funcionario(func.get('ID_Funcionario'), novo_cargo):
            # Opcional: print("Cargo atualizado")
            pass
        else:
            messagebox.showerror("Erro", "Falha ao atualizar perfil no banco.")
            self.carregar_funcionarios()

    def remover_equipe(self, func):
        if messagebox.askyesno("Confirmar", f"Remover {func.get('Nome')} desta loja?"):
            if remover_funcionario(func.get('ID_Funcionario')):
                self.carregar_funcionarios()
            else:
                messagebox.showerror("Erro", "Não foi possível remover.")

    def voltar(self):
        from data.menu import mostrar_menu
        mostrar_menu(self.app, sessao.nome, sessao.perfil)

def listar_funcionarios(app):
    TelaListarFuncionarios(app)