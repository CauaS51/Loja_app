import customtkinter as ctk
from tkinter import messagebox, filedialog
import data.colors as colors
from data.colors import *
import data.sessao as sessao
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# Importação para buscar usuários reais do banco
from crud.crud_cadastros import listar_cadastros

# Bibliotecas para o Gráfico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RelatoriosApp:
    def __init__(self, app):
        self.app = app
        
        # 1. Busca dinâmica de usuários cadastrados
        try:
            usuarios_db = listar_cadastros()
            self.usuarios_cadastrados = [u['nome'] for u in usuarios_db]
        except Exception:
            self.usuarios_cadastrados = []

        # 2. Categorias vindas do repositorio.py
        self.lista_categorias = [
            "Hortifruti", "Açougue", "Peixaria", "Padaria", "Laticínios", 
            "Mercearia", "Temperos", "Bebidas", "Biscoitos & Snacks", 
            "Doces & Chocolates", "Congelados", "Limpeza", "Higiene Pessoal", 
            "Bebês", "Pet Shop", "Utilidades Domésticas"
        ]
            
        self.dados_filtrados = []
        self.canvas_grafico = None 
        self.gerar_tela_relatorios()

    def gerar_tela_relatorios(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Sistema de Gestão - Relatórios & BI")
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], 
            hover_color=cores["HOVER"], command=self.voltar_menu
        )
        btn_voltar.pack(side="left", padx=20, pady=20)

        ctk.CTkLabel(
            header, text="📊 Inteligência e Relatórios",
            text_color="white", font=ctk.CTkFont("Segoe UI", 26, "bold")
        ).pack(side="left", pady=20)

        # === CONTEÚDO PRINCIPAL (SCROLLABLE) ===
        main_scroll = ctk.CTkScrollableFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=0)
        main_scroll.pack(fill="both", expand=True)

        # SEÇÃO DE FILTROS
        filtros_frame = ctk.CTkFrame(main_scroll, fg_color=cores["CARD_BG"], corner_radius=12)
        filtros_frame.pack(fill="x", padx=20, pady=15)
        filtros_frame.grid_columnconfigure((1, 3, 5), weight=1)

        # Seleção do Tipo de Relatório (Vendas ou Estoque)
        ctk.CTkLabel(filtros_frame, text="Relatório:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=10)
        self.combo_tipo_relatorio = ctk.CTkComboBox(filtros_frame, values=["Vendas", "Estoque"], command=self.ajustar_filtros)
        self.combo_tipo_relatorio.set("Vendas")
        self.combo_tipo_relatorio.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Filtros de Data (Desativados se for Estoque)
        ctk.CTkLabel(filtros_frame, text="Início:").grid(row=0, column=2, padx=5, pady=10)
        self.entry_data_inicio = ctk.CTkEntry(filtros_frame, placeholder_text="DD/MM/AAAA")
        self.entry_data_inicio.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        ctk.CTkLabel(filtros_frame, text="Fim:").grid(row=0, column=4, padx=5, pady=10)
        self.entry_data_fim = ctk.CTkEntry(filtros_frame, placeholder_text="DD/MM/AAAA")
        self.entry_data_fim.grid(row=0, column=5, padx=5, pady=10, sticky="ew")

        # Vendedor
        ctk.CTkLabel(filtros_frame, text="Vendedor:").grid(row=1, column=0, padx=5, pady=10)
        self.combo_usuario = ctk.CTkComboBox(filtros_frame, values=["Todos"] + self.usuarios_cadastrados)
        self.combo_usuario.set("Todos")
        self.combo_usuario.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        # Pagamento
        ctk.CTkLabel(filtros_frame, text="Pagamento:").grid(row=1, column=2, padx=5, pady=10)
        self.combo_pagamento = ctk.CTkComboBox(filtros_frame, values=[
            "Todos", "PIX", "Crédito", "Débito", "Dinheiro em espécie", 
            "Ticket Alimentação (VA)", "Vale-Refeição (VR)"
        ])
        self.combo_pagamento.set("Todos")
        self.combo_pagamento.grid(row=1, column=3, padx=5, pady=10, sticky="ew")

        # Categoria (Importante para ambos os relatórios)
        ctk.CTkLabel(filtros_frame, text="Categoria:").grid(row=1, column=4, padx=5, pady=10)
        self.combo_categoria = ctk.CTkComboBox(filtros_frame, values=["Todos"] + self.lista_categorias)
        self.combo_categoria.set("Todos")
        self.combo_categoria.grid(row=1, column=5, padx=5, pady=10, sticky="ew")

        # BOTÕES
        btn_container = ctk.CTkFrame(main_scroll, fg_color="transparent")
        btn_container.pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(btn_container, text="🔍 Gerar Relatório", fg_color=cores["PRIMARY"], command=self.gerar_relatorio).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(btn_container, text="📄 Exportar PDF", fg_color="#27ae60", command=self.exportar_pdf).pack(side="left", expand=True, fill="x", padx=5)

        # GRÁFICO E TABELA
        self.chart_frame = ctk.CTkFrame(main_scroll, fg_color=cores["CARD_BG"], height=300, corner_radius=12)
        self.chart_frame.pack(fill="x", padx=20, pady=10)

        self.table_frame = ctk.CTkFrame(main_scroll, fg_color=cores["CARD_BG"], corner_radius=12)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.data_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.data_container.pack(fill="both", expand=True, padx=10, pady=10)

    def ajustar_filtros(self, escolha):
        """Desativa filtros irrelevantes para o relatório de estoque."""
        if escolha == "Estoque":
            self.entry_data_inicio.configure(state="disabled")
            self.entry_data_fim.configure(state="disabled")
            self.combo_usuario.configure(state="disabled")
            self.combo_pagamento.configure(state="disabled")
        else:
            self.entry_data_inicio.configure(state="normal")
            self.entry_data_fim.configure(state="normal")
            self.combo_usuario.configure(state="normal")
            self.combo_pagamento.configure(state="normal")

    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app, usuario=sessao.nome, perfil=sessao.perfil)

    def obter_dados_base(self, tipo):
        """Simula base de dados para Vendas ou Estoque."""
        if tipo == "Vendas":
            vendedor_padrao = self.usuarios_cadastrados[0] if self.usuarios_cadastrados else "Vendedor"
            return [
                {"data": "01/01", "valor": 450.0, "tipo": "PIX", "vendedor": vendedor_padrao, "categoria": "Hortifruti"},
                {"data": "02/01", "valor": 890.0, "tipo": "Crédito", "vendedor": vendedor_padrao, "categoria": "Limpeza"},
                {"data": "04/01", "valor": 1200.0, "tipo": "Ticket Alimentação (VA)", "vendedor": "Administrador", "categoria": "Açougue"},
                {"data": "05/01", "valor": 600.0, "tipo": "Vale-Refeição (VR)", "vendedor": "Gerente", "categoria": "Padaria"},
            ]
        else: # Tipo Estoque
            return [
                {"produto": "Alface Hidropônica", "qtd": 50, "categoria": "Hortifruti", "valor_un": 3.50},
                {"produto": "Pão Francês", "qtd": 200, "categoria": "Padaria", "valor_un": 0.50},
                {"produto": "Detergente 500ml", "qtd": 15, "categoria": "Limpeza", "valor_un": 2.20},
                {"produto": "Picanha KG", "qtd": 8, "categoria": "Açougue", "valor_un": 85.90},
                {"produto": "Leite Integral", "qtd": 120, "categoria": "Laticínios", "valor_un": 5.40},
            ]

    def gerar_relatorio(self):
        for w in self.data_container.winfo_children(): w.destroy()
        if self.canvas_grafico: self.canvas_grafico.get_tk_widget().destroy()

        tipo_rel = self.combo_tipo_relatorio.get()
        categoria_sel = self.combo_categoria.get()
        dados_brutos = self.obter_dados_base(tipo_rel)

        # Lógica de Filtragem
        if tipo_rel == "Vendas":
            vendedor_sel = self.combo_usuario.get()
            pagamento_sel = self.combo_pagamento.get()
            self.dados_filtrados = [
                item for item in dados_brutos
                if (vendedor_sel == "Todos" or item['vendedor'] == vendedor_sel) and
                   (pagamento_sel == "Todos" or item['tipo'] == pagamento_sel) and
                   (categoria_sel == "Todos" or item['categoria'] == categoria_sel)
            ]
        else: # Estoque
            self.dados_filtrados = [
                item for item in dados_brutos
                if (categoria_sel == "Todos" or item['categoria'] == categoria_sel)
            ]

        if not self.dados_filtrados:
            ctk.CTkLabel(self.data_container, text="Nenhum dado encontrado.").pack(pady=20)
            return

        self.plotar_grafico(self.dados_filtrados, tipo_rel)
        self.renderizar_tabela_tela(tipo_rel)

    def renderizar_tabela_tela(self, tipo):
        cores = colors.get_colors()
        if tipo == "Vendas":
            header = "Data | Vendedor | Pagamento | Categoria | Valor"
            ctk.CTkLabel(self.data_container, text=header, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
            for d in self.dados_filtrados:
                txt = f"{d['data']} | {d['vendedor']} | {d['tipo']} | {d['categoria']} | R$ {d['valor']:.2f}"
                ctk.CTkLabel(self.data_container, text=txt, text_color=cores["TEXT_PRIMARY"]).pack(anchor="w", padx=20)
        else: # Estoque
            header = "Produto | Categoria | Quantidade | Valor Un. | Total"
            ctk.CTkLabel(self.data_container, text=header, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
            for d in self.dados_filtrados:
                total = d['qtd'] * d['valor_un']
                txt = f"{d['produto']} | {d['categoria']} | {d['qtd']} un | R$ {d['valor_un']:.2f} | R$ {total:.2f}"
                ctk.CTkLabel(self.data_container, text=txt, text_color=cores["TEXT_PRIMARY"]).pack(anchor="w", padx=20)

    def plotar_grafico(self, dados, tipo):
        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        
        if tipo == "Vendas":
            resumo = {}
            for d in dados: resumo[d['data']] = resumo.get(d['data'], 0) + d['valor']
            ax.plot(list(resumo.keys()), list(resumo.values()), marker='o', color='#3b8ed0')
            ax.set_title("Evolução de Vendas")
        else: # Estoque - Gráfico de Barras por Produto
            produtos = [d['produto'] for d in dados]
            quantidades = [d['qtd'] for d in dados]
            ax.bar(produtos, quantidades, color='#27ae60')
            ax.set_title("Nível de Estoque por Produto")
            plt.xticks(rotation=15)

        ax.grid(True, alpha=0.3)
        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)

    def exportar_pdf(self):
        if not self.dados_filtrados:
            messagebox.showwarning("Aviso", "Não há dados para exportar.")
            return
        
        tipo = self.combo_tipo_relatorio.get()
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf")
        if caminho:
            c = canvas.Canvas(caminho, pagesize=letter)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, 750, f"RELATÓRIO DE {tipo.upper()} - {datetime.now().strftime('%d/%m/%Y')}")
            c.setFont("Helvetica", 10)
            y = 720
            
            for d in self.dados_filtrados:
                if tipo == "Vendas":
                    txt = f"{d['data']} - {d['vendedor']} - {d['categoria']} - R$ {d['valor']:.2f}"
                else:
                    txt = f"{d['produto']} ({d['categoria']}) - Qtd: {d['qtd']} - Un: R$ {d['valor_un']:.2f}"
                
                c.drawString(100, y, txt)
                y -= 20
                if y < 50: c.showPage(); y = 750
            
            c.save()
            messagebox.showinfo("Sucesso", "PDF exportado!")

def mostrar_relatorios(app):
    RelatoriosApp(app)