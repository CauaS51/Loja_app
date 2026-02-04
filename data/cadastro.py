import customtkinter as ctk
from tkinter import messagebox
import data.colors as colors
import data.sessao as sessao
import re
from crud.crud_cadastros import cadastrar_usuario
from crud.crud_cadastros import (listar_funcionarios_da_loja, remover_funcionario, atualizar_perfil_funcionario)


# ====================================================================================
# ======================== TELA CADASTRO CONTA =======================================
# ====================================================================================
class TelaCadastroConta:
    def __init__(self, app):
        self.app = app

        self.var_nome = ctk.StringVar()
        self.var_login = ctk.StringVar()
        self.var_email = ctk.StringVar()
        self.var_telefone = ctk.StringVar()
        self.var_cpf = ctk.StringVar()

        self.var_cpf.trace_add("write", self.mascara_cpf)
        self.var_telefone.trace_add("write", self.mascara_telefone)
        self.var_nome.trace_add("write", self.validar_nome)

        # 🔥 SINCRONIZA TEMA ANTES DE CONSTRUIR
        self.app.after(20, self._iniciar_tela)

    def _iniciar_tela(self):
        self.app.update_idletasks()
        self.app.update()

        self.cores = colors.get_colors()
        
        self.app.configure(fg_color=self.cores["BACKGROUND"])
        self.montar_tela()

    def montar_tela(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Sistema PDV | Cadastro de Operador")
        self.criar_header()

        main_container = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND"])
        main_container.pack(fill="both", expand=True)

        card = ctk.CTkFrame(main_container, width=550, corner_radius=20, fg_color=self.cores["CARD_BG"])
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="📝 Registro de Funcionário",
                     font=("Segoe UI", 24, "bold"),
                     text_color=self.cores["PRIMARY"]).pack(pady=(30, 5))

        ctk.CTkLabel(card, text="Informe os dados para acesso ao terminal",
                     font=("Segoe UI", 13),
                     text_color=self.cores["TEXT_SECONDARY"]).pack(pady=(0, 25))

        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(fill="x", padx=40)
        form_frame.grid_columnconfigure((0, 1), weight=1, pad=20)

        self.ent_nome = self.criar_campo(form_frame, "Nome Completo*", self.var_nome, 0, 0, colspan=2)
        self.ent_email = self.criar_campo(form_frame, "E-mail Corporativo*", self.var_email, 1, 0, colspan=2)
        self.ent_login = self.criar_campo(form_frame, "Usuário (Login)*", self.var_login, 2, 0)
        self.ent_cpf = self.criar_campo(form_frame, "CPF (Somente números)*", self.var_cpf, 2, 1)
        self.ent_tel = self.criar_campo(form_frame, "Telefone", self.var_telefone, 3, 0)
        self.ent_senha = self.criar_campo(form_frame, "Senha*", None, 3, 1, senha=True)

        ctk.CTkButton(card, text="CONFIRMAR CADASTRO", height=50,
                      font=("Segoe UI", 16, "bold"),
                      fg_color=self.cores["PRIMARY"],
                      hover_color=self.cores["HOVER"],
                      command=self.executar_cadastro).pack(pady=(30, 10), padx=40, fill="x")

        ctk.CTkButton(card, text="CANCELAR", height=40,
                      fg_color="transparent", border_width=2,
                      border_color="#FF4B4B", text_color="#FF4B4B",
                      command=self.voltar).pack(pady=(0, 30), padx=40, fill="x")

    def criar_header(self):
        header = ctk.CTkFrame(self.app, fg_color=self.cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")

        ctk.CTkButton(header, text="⬅", width=40, height=40,
                      font=ctk.CTkFont(size=20), corner_radius=12,
                      fg_color=self.cores["ENTRY_BG"], hover_color=self.cores["HOVER"],
                      text_color=self.cores["TEXT_PRIMARY"],
                      command=self.voltar).pack(side="left", padx=20, pady=20)

        ctk.CTkLabel(header, text="🛡️ Cadastro de Operador",
                     text_color="white",
                     font=ctk.CTkFont("Segoe UI", 26, "bold")).pack(side="left", pady=20)

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=20, pady=20)

        icone = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"
        ctk.CTkButton(right, text=icone, width=40, height=40,
                      corner_radius=12,
                      fg_color=self.cores["ENTRY_BG"],
                      hover_color=self.cores["HOVER"],
                      text_color=self.cores["TEXT_PRIMARY"],
                      font=ctk.CTkFont(size=22),
                      command=self.alternar_tema).pack(side="left")

    def alternar_tema(self):
        colors.alternar_tema()
        self.app.after(30, self._iniciar_tela)

    def criar_campo(self, master, texto, variavel, row, col, colspan=1, senha=False):
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=10)

        ctk.CTkLabel(frame, text=texto, font=("Segoe UI", 12, "bold"),
                     text_color=self.cores["TEXT_PRIMARY"]).pack(anchor="w")

        entry = ctk.CTkEntry(frame, height=40, textvariable=variavel,
                             show="*" if senha else "", fg_color=self.cores["ENTRY_BG"])
        entry.pack(fill="x", pady=2)
        return entry

    def mascara_cpf(self, *args):
        valor = re.sub(r'\D', '', self.var_cpf.get())[:11]
        if len(valor) > 9:
            valor = f"{valor[:3]}.{valor[3:6]}.{valor[6:9]}-{valor[9:]}"
        elif len(valor) > 6:
            valor = f"{valor[:3]}.{valor[3:6]}.{valor[6:]}"
        elif len(valor) > 3:
            valor = f"{valor[:3]}.{valor[3:]}"
        self.var_cpf.set(valor)

    def mascara_telefone(self, *args):
        valor = re.sub(r'\D', '', self.var_telefone.get())[:11]
        if len(valor) == 11:
            valor = f"({valor[:2]}) {valor[2:7]}-{valor[7:]}"
        elif len(valor) > 2:
            valor = f"({valor[:2]}) {valor[2:]}"
        self.var_telefone.set(valor)

    def validar_nome(self, *args):
        self.var_nome.set(re.sub(r'[0-9]', '', self.var_nome.get()))

    def executar_cadastro(self):
        dados = {
            "nome": self.var_nome.get().strip(),
            "login": self.var_login.get().strip(),
            "email": self.var_email.get().strip(),
            "cpf": re.sub(r'\D', '', self.var_cpf.get()),
            "senha": self.ent_senha.get().strip(),
            "tel": self.var_telefone.get().strip()
        }

        if not all([dados["nome"], dados["login"], dados["cpf"], dados["senha"]]):
            messagebox.showwarning("Campos Obrigatórios", "Preencha todos os campos obrigatórios.")
            return

        if len(dados["cpf"]) != 11:
            messagebox.showerror("CPF Inválido", "CPF deve conter 11 dígitos.")
            return

        if cadastrar_usuario(dados["nome"], dados["login"], dados["senha"],
                             dados["email"], dados["tel"], dados["cpf"]):
            messagebox.showinfo("Sucesso", f"Operador {dados['login']} cadastrado!")
            self.voltar()

    def voltar(self):
        from custompdv import mostrar_login
        mostrar_login(self.app)


def abrir_cadastro(app):
    TelaCadastroConta(app)
class TelaListarFuncionarios:
    def __init__(self, app):
        self.app = app
        self.app.after(10, self._iniciar_tela)

    # ================= INICIALIZAÇÃO SEGURA DO TEMA =================
    def _iniciar_tela(self):
        self.app.update_idletasks()
        self.app.update()

        # Recarrega cores após o modo aplicar
        self.cores = colors.get_colors()

        self.app.configure(fg_color=self.cores["BACKGROUND"])
        self.montar_tela()

    # ================= CONSTRUÇÃO =================
    def montar_tela(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.criar_header()

        container = ctk.CTkFrame(self.app, fg_color=self.cores["BACKGROUND"])
        container.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        thead = ctk.CTkFrame(container, fg_color=self.cores["BACKGROUND_2"], height=40)
        thead.pack(fill="x", padx=10, pady=(10, 5))

        labels = ["NOME", "USUÁRIO", "ID_FUNC", "PERFIL (CLIQUE P/ ALTERAR)", "AÇÕES"]
        pos = [0.03, 0.32, 0.52, 0.70, 0.92]
        for t, p in zip(labels, pos):
            ctk.CTkLabel(thead, text=t, font=("Segoe UI", 11, "bold"),
                         text_color=self.cores["TEXT_SECONDARY"]
                         ).place(relx=p, rely=0.5, anchor="w")

        # ⚠ NÃO usar transparent aqui
        self.scroll = ctk.CTkScrollableFrame(container, fg_color=self.cores["BACKGROUND"])
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self.carregar_funcionarios()

    # ================= HEADER =================
    def criar_header(self):
        header = ctk.CTkFrame(self.app, fg_color=self.cores["PRIMARY"], height=80)
        header.pack(fill="x")

        ctk.CTkButton(header, text="⬅", width=40, height=40,
                      fg_color=self.cores["ENTRY_BG"],
                      hover_color=self.cores["HOVER"],
                      text_color=self.cores["TEXT_PRIMARY"],
                      command=self.voltar).pack(side="left", padx=20, pady=20)

        ctk.CTkLabel(header, text=f"👥 Equipe · {sessao.nome_loja}",
                     text_color="white",
                     font=ctk.CTkFont("Segoe UI", 26, "bold")).pack(side="left", pady=20)

        icone = "🌙" if ctk.get_appearance_mode() == "Dark" else "🔆"

        ctk.CTkButton(header, text=icone,
                      width=40, height=40,
                      fg_color=self.cores["ENTRY_BG"],
                      hover_color=self.cores["HOVER"],
                      text_color=self.cores["TEXT_PRIMARY"],
                      command=self.alternar_tema).pack(side="right", padx=20, pady=20)

    # ================= TROCA DE TEMA REAL =================
    def alternar_tema(self):
        colors.alternar_tema()

        self.app.update_idletasks()
        self.app.update()

        self.app.after(10, self._iniciar_tela)

    # ================= LISTAGEM =================
    def carregar_funcionarios(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        dados = listar_funcionarios_da_loja(sessao.loja_id)

        for func in dados:
            perfil_val = func.get('Nome_Perfil', 'Caixa')
            eh_adm = str(perfil_val).lower() == "administrador"

            line = ctk.CTkFrame(self.scroll, fg_color=self.cores["CARD_BG"], height=55)
            line.pack(fill="x", pady=2)

            ctk.CTkLabel(line, text=func.get('Nome', ''),
                         text_color=self.cores["PRIMARY"] if eh_adm else self.cores["TEXT_PRIMARY"]
                         ).place(relx=0.03, rely=0.5, anchor="w")

            ctk.CTkLabel(line, text=f"@{func.get('Login','')}",
                         text_color=self.cores["TEXT_SECONDARY"]
                         ).place(relx=0.32, rely=0.5, anchor="w")

            ctk.CTkLabel(line, text=str(func.get('ID_Funcionario','')).zfill(4)
                         ).place(relx=0.52, rely=0.5, anchor="w")

            if eh_adm:
                ctk.CTkLabel(line, text="GERENTE",
                             text_color="white",
                             fg_color=self.cores["PRIMARY"],
                             corner_radius=5,
                             width=140,
                             height=28).place(relx=0.70, rely=0.5, anchor="w")
            else:
                menu = ctk.CTkOptionMenu(
                    line,
                    values=["Caixa", "Repositor", "Gestor de Dados"],
                    text_color=self.cores["TEXT_PRIMARY"],
                    fg_color=self.cores["ENTRY_BG"],
                    button_color=self.cores["PRIMARY"],
                    dropdown_fg_color=self.cores["CARD_BG"],
                    dropdown_hover_color=self.cores["HOVER"],
                    command=lambda novo, f=func: self.mudar_cargo(f, novo)
                )
                menu.set(perfil_val)
                menu.place(relx=0.70, rely=0.5, anchor="w")

    # ================= AÇÕES =================
    def mudar_cargo(self, func, novo):
        atualizar_perfil_funcionario(func.get('ID_Funcionario'), novo)

    def voltar(self):
        from data.menu import mostrar_menu
        mostrar_menu(self.app, sessao.nome, sessao.perfil)

def listar_funcionarios(app):
    TelaListarFuncionarios(app)