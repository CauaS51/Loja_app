import json
import os
from datetime import datetime, timedelta
import customtkinter as ctk
from tkinter import messagebox


ARQUIVO_PRODUTOS = "data/produtos.json"
ARQUIVO_MOV = "data/movimentacoes.json"


class RepositorioApp:
    def __init__(self):
        # Configuração principal da janela
        self.app = ctk.CTk()
        self.app.title("📦 Repositório / Controle de Estoque")
        self.app.geometry("1100x750")
        ctk.set_appearance_mode("dark")

        os.makedirs("data", exist_ok=True)
        self.produtos = self.carregar_produtos()
        self.movimentacoes = self.carregar_mov()

        self._build_ui()
        self.atualizar_lista()

    # -------------------------------------------------------------------------
    # Carregamento e salvamento de dados
    # -------------------------------------------------------------------------
    def carregar_produtos(self):
        if os.path.exists(ARQUIVO_PRODUTOS):
            with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def salvar_produtos(self):
        with open(ARQUIVO_PRODUTOS, "w", encoding="utf-8") as f:
            json.dump(self.produtos, f, ensure_ascii=False, indent=2)

    def carregar_mov(self):
        if os.path.exists(ARQUIVO_MOV):
            with open(ARQUIVO_MOV, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def salvar_mov(self):
        with open(ARQUIVO_MOV, "w", encoding="utf-8") as f:
            json.dump(self.movimentacoes, f, ensure_ascii=False, indent=2)

    # -------------------------------------------------------------------------
    # Construção da Interface
    # -------------------------------------------------------------------------
    def _build_ui(self):
        self.app.grid_rowconfigure(2, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        # Topo: Botões de ação
        header = ctk.CTkFrame(self.app)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        ctk.CTkButton(header, text="➕ Cadastrar Produto", command=self.cadastrar_produto).pack(side="left", padx=10)
        ctk.CTkButton(header, text="📥 Entrada", command=self.registrar_entrada).pack(side="left", padx=10)
        ctk.CTkButton(header, text="📤 Saída", command=self.registrar_saida).pack(side="left", padx=10)
        ctk.CTkButton(header, text="📊 Relatórios", command=self.abrir_relatorios).pack(side="left", padx=10)

        # Campo de busca
        busca_frame = ctk.CTkFrame(self.app)
        busca_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        ctk.CTkLabel(busca_frame, text="🔍 Buscar produto:").pack(side="left", padx=10)
        self.busca_entry = ctk.CTkEntry(busca_frame, placeholder_text="Digite nome ou código...")
        self.busca_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.busca_entry.bind("<KeyRelease>", lambda e: self.atualizar_lista(self.busca_entry.get()))

        # Lista de produtos
        self.prod_frame = ctk.CTkScrollableFrame(self.app)
        self.prod_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

    # -------------------------------------------------------------------------
    # Atualiza lista de produtos (com busca)
    # -------------------------------------------------------------------------
    def atualizar_lista(self, termo_busca=""):
        for w in self.prod_frame.winfo_children():
            w.destroy()

        produtos = self.produtos
        if termo_busca:
            termo = termo_busca.lower()
            produtos = {
                c: p for c, p in produtos.items()
                if termo in c.lower() or termo in p["nome"].lower()
            }

        if not produtos:
            ctk.CTkLabel(self.prod_frame, text="Nenhum produto encontrado.").pack(pady=20)
            return

        for codigo, prod in produtos.items():
            f = ctk.CTkFrame(self.prod_frame, height=80)
            f.pack(fill="x", pady=4, padx=5)

            ctk.CTkLabel(f, text=f"{codigo} — {prod['nome']}", font=ctk.CTkFont(size=15, weight="bold")).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=f"Categoria: {prod.get('categoria', '-')}", width=150).pack(side="left")
            ctk.CTkLabel(f, text=f"Qtd: {prod['quantidade']}", width=80).pack(side="left")
            ctk.CTkLabel(f, text=f"R$ {prod['valor']:.2f}", width=100).pack(side="left")

            ctk.CTkButton(f, text="Editar", width=80, command=lambda c=codigo: self.editar_produto(c)).pack(side="right", padx=5)
            ctk.CTkButton(f, text="Excluir", width=80, fg_color="#b22222",
                          hover_color="#cc3232", command=lambda c=codigo: self.excluir_produto(c)).pack(side="right", padx=5)

    # -------------------------------------------------------------------------
    # Cadastro de produto
    # -------------------------------------------------------------------------
    def cadastrar_produto(self):
        win = ctk.CTkToplevel(self.app)
        win.title("Cadastrar Produto")
        win.geometry("400x500")

        campos = {}
        labels = ["Código", "Nome", "Categoria", "Valor", "Quantidade Inicial"]
        for label in labels:
            ctk.CTkLabel(win, text=label).pack(pady=(10, 2))
            entry = ctk.CTkEntry(win)
            entry.pack(pady=4)
            campos[label.lower()] = entry

        def salvar():
            codigo = campos["código"].get().strip()
            nome = campos["nome"].get().strip()
            cat = campos["categoria"].get().strip()
            if not codigo or not nome:
                messagebox.showwarning("Aviso", "Preencha código e nome.")
                return
            if codigo in self.produtos:
                messagebox.showerror("Erro", "Código já existente.")
                return
            try:
                valor = float(campos["valor"].get())
                qtd = int(campos["quantidade inicial"].get())
            except ValueError:
                messagebox.showerror("Erro", "Valor ou quantidade inválidos.")
                return
            self.produtos[codigo] = {
                "nome": nome,
                "categoria": cat,
                "valor": valor,
                "quantidade": qtd
            }
            self.salvar_produtos()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
            win.destroy()

        ctk.CTkButton(win, text="Salvar", command=salvar).pack(pady=20)

    # -------------------------------------------------------------------------
    # Editar / Excluir produto
    # -------------------------------------------------------------------------
    def editar_produto(self, codigo):
        prod = self.produtos[codigo]
        win = ctk.CTkToplevel(self.app)
        win.title("Editar Produto")
        win.geometry("400x500")

        ctk.CTkLabel(win, text=f"Código: {codigo}").pack(pady=6)
        nome_entry = ctk.CTkEntry(win)
        nome_entry.insert(0, prod["nome"])
        nome_entry.pack(pady=6)

        cat_entry = ctk.CTkEntry(win)
        cat_entry.insert(0, prod.get("categoria", ""))
        cat_entry.pack(pady=6)

        valor_entry = ctk.CTkEntry(win)
        valor_entry.insert(0, str(prod["valor"]))
        valor_entry.pack(pady=6)

        qtd_entry = ctk.CTkEntry(win)
        qtd_entry.insert(0, str(prod["quantidade"]))
        qtd_entry.pack(pady=6)

        def salvar():
            try:
                prod["nome"] = nome_entry.get()
                prod["categoria"] = cat_entry.get()
                prod["valor"] = float(valor_entry.get())
                prod["quantidade"] = int(qtd_entry.get())
                self.salvar_produtos()
                self.atualizar_lista()
                messagebox.showinfo("Editado", "Produto atualizado.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ctk.CTkButton(win, text="Salvar", command=salvar).pack(pady=20)

    def excluir_produto(self, codigo):
        if messagebox.askyesno("Excluir", f"Excluir produto {codigo}?"):
            del self.produtos[codigo]
            self.salvar_produtos()
            self.atualizar_lista()

    # -------------------------------------------------------------------------
    # Entradas e Saídas
    # -------------------------------------------------------------------------
    def registrar_entrada(self):
        self.registrar_movimento("entrada")

    def registrar_saida(self):
        self.registrar_movimento("saida")

    def registrar_movimento(self, tipo):
        win = ctk.CTkToplevel(self.app)
        win.title(f"Registrar {tipo.capitalize()}")
        win.geometry("400x400")

        ctk.CTkLabel(win, text="Código do produto").pack(pady=6)
        codigo_entry = ctk.CTkEntry(win)
        codigo_entry.pack(pady=6)

        ctk.CTkLabel(win, text="Quantidade").pack(pady=6)
        qtd_entry = ctk.CTkEntry(win)
        qtd_entry.pack(pady=6)

        def confirmar():
            codigo = codigo_entry.get().strip()
            if codigo not in self.produtos:
                messagebox.showerror("Erro", "Produto não encontrado.")
                return
            try:
                qtd = int(qtd_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Quantidade inválida.")
                return

            if tipo == "saida" and self.produtos[codigo]["quantidade"] < qtd:
                messagebox.showerror("Erro", "Estoque insuficiente.")
                return

            if tipo == "entrada":
                self.produtos[codigo]["quantidade"] += qtd
            else:
                self.produtos[codigo]["quantidade"] -= qtd

            self.movimentacoes.append({
                "codigo": codigo,
                "tipo": tipo,
                "quantidade": qtd,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.salvar_mov()
            self.salvar_produtos()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", f"{tipo.capitalize()} registrada.")
            win.destroy()

        ctk.CTkButton(win, text="Confirmar", command=confirmar).pack(pady=20)

    # -------------------------------------------------------------------------
    # Relatórios (Dia / Semana / Mês)
    # -------------------------------------------------------------------------
    def abrir_relatorios(self):
        win = ctk.CTkToplevel(self.app)
        win.title("📊 Relatórios de Movimentação")
        win.geometry("600x600")

        relatorio_frame = ctk.CTkScrollableFrame(win)
        relatorio_frame.pack(fill="both", expand=True, padx=10, pady=10)

        hoje = datetime.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        inicio_mes = hoje.replace(day=1)

        totais = {"entrada": 0, "saida": 0}

        def filtrar_movimentos(inicio):
            entradas = sum(m["quantidade"] for m in self.movimentacoes
                           if m["tipo"] == "entrada" and datetime.strptime(m["data"], "%Y-%m-%d %H:%M:%S").date() >= inicio)
            saidas = sum(m["quantidade"] for m in self.movimentacoes
                         if m["tipo"] == "saida" and datetime.strptime(m["data"], "%Y-%m-%d %H:%M:%S").date() >= inicio)
            return entradas, saidas

        # Relatórios
        for nome, inicio in [("Hoje", hoje), ("Semana", inicio_semana), ("Mês", inicio_mes)]:
            ent, sai = filtrar_movimentos(inicio)
            frame = ctk.CTkFrame(relatorio_frame)
            frame.pack(fill="x", pady=8)
            ctk.CTkLabel(frame, text=f"📅 {nome}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=f"Entradas: {ent} itens").pack(anchor="w", padx=20)
            ctk.CTkLabel(frame, text=f"Saídas: {sai} itens").pack(anchor="w", padx=20)

    # -------------------------------------------------------------------------
    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    RepositorioApp().run()
