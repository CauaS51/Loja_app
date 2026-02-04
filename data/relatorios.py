import customtkinter as ctk
from tkinter import messagebox, filedialog
import data.colors as colors
import data.sessao as sessao
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Imports do CRUD
from crud.crud_relatorios import buscar_relatorio_vendas, buscar_status_caixas
from crud.crud_cadastros import listar_cadastros
from crud.crud_categorias import listar_categorias # Supondo que você tenha esta função

class RelatoriosApp:
    def __init__(self, app):
        self.app = app
        self.cores = colors.get_colors()
        
        # Carregamento de dados para combos
        try:
            self.usuarios_cadastrados = [u['nome'] for u in listar_cadastros()]
            self.categorias_db = [c['Nome'] for c in listar_categorias(sessao.loja_id)]
        except:
            self.usuarios_cadastrados = []
            self.categorias_db = ["Geral"]

        self.dados_filtrados = []
        self.canvas_grafico = None 
        self.gerar_tela_relatorios()

    def gerar_tela_relatorios(self):
        for w in self.app.winfo_children(): w.destroy()
        
        # HEADER
        header = ctk.CTkFrame(self.app, fg_color=self.cores["PRIMARY"], height=70, corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkButton(header, text="⬅", width=40, command=self.voltar_menu).pack(side="left", padx=20)
        ctk.CTkLabel(header, text="📊 DASHBOARD DE INTELIGÊNCIA", text_color="white", 
                     font=ctk.CTkFont(size=22, weight="bold")).pack(side="left")

        # SCROLL PRINCIPAL
        main_scroll = ctk.CTkScrollableFrame(self.app, fg_color=self.cores["BACKGROUND"])
        main_scroll.pack(fill="both", expand=True)

        # --- SEÇÃO: RESUMO DE CAIXA (ABERTURA/FECHAMENTO) ---
        self.render_sessao_caixa(main_scroll)

        # --- SEÇÃO: FILTROS DE VENDAS ---
        filtros_frame = ctk.CTkFrame(main_scroll, fg_color=self.cores["CARD_BG"], corner_radius=12)
        filtros_frame.pack(fill="x", padx=20, pady=10)
        
        # Grid de filtros
        self.entry_inicio = self.criar_campo_filtro(filtros_frame, "Início:", 0, 0, "2026-02-01")
        self.entry_fim = self.criar_campo_filtro(filtros_frame, "Fim:", 0, 2, "2026-02-28")
        
        self.combo_user = self.criar_combo_filtro(filtros_frame, "Funcionário:", 1, 0, ["Todos"] + self.usuarios_cadastrados)
        self.combo_cat = self.criar_combo_filtro(filtros_frame, "Categoria:", 1, 2, ["Todos"] + self.categorias_db)

        # BOTÕES DE AÇÃO
        btn_box = ctk.CTkFrame(main_scroll, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(btn_box, text="🔍 ATUALIZAR DADOS", fg_color=self.cores["PRIMARY"], 
                     command=self.processar_relatorio).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(btn_box, text="📄 EXPORTAR PDF", fg_color="#27ae60", 
                     command=self.exportar_pdf).pack(side="left", expand=True, fill="x", padx=5)

        # ÁREA VISUAL (GRÁFICO)
        self.chart_frame = ctk.CTkFrame(main_scroll, fg_color=self.cores["CARD_BG"], height=300)
        self.chart_frame.pack(fill="x", padx=20, pady=10)

        # TABELA DE RESULTADOS
        self.table_container = ctk.CTkFrame(main_scroll, fg_color=self.cores["CARD_BG"])
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)

    def render_sessao_caixa(self, master):
        frame = ctk.CTkFrame(master, fg_color="#2c3e50", corner_radius=12)
        frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame, text="ÚLTIMOS MOVIMENTOS DE CAIXA", text_color="white", font=("Arial", 14, "bold")).pack(pady=5)
        
        caixas = buscar_status_caixas()
        for c in caixas:
            status_color = "#2ecc71" if c['Status'] == 'ABERTO' else "#e74c3c"
            txt = f"ID: {c['ID_Caixa']} | {c['Operador']} | Início: R$ {c['Valor_Inicial']} | Status: {c['Status']}"
            ctk.CTkLabel(frame, text=txt, text_color=status_color).pack(anchor="w", padx=20)

    def processar_relatorio(self):
        # Limpar área anterior
        for w in self.table_container.winfo_children(): w.destroy()
        if self.canvas_grafico: self.canvas_grafico.get_tk_widget().destroy()

        # Buscar dados reais do banco
        self.dados_filtrados = buscar_relatorio_vendas(
            self.entry_inicio.get(), self.entry_fim.get(),
            self.combo_user.get(), self.combo_cat.get()
        )

        if not self.dados_filtrados:
            ctk.CTkLabel(self.table_container, text="Nenhuma venda encontrada para os filtros selecionados.").pack(pady=20)
            return

        self.plotar_grafico_vendas()
        self.renderizar_tabela()

    def plotar_grafico_vendas(self):
        resumo = {}
        for d in self.dados_filtrados:
            data_str = d['data'].strftime('%d/%m')
            resumo[data_str] = resumo.get(data_str, 0) + float(d['valor'])

        fig, ax = plt.subplots(figsize=(8, 3), facecolor=self.cores["CARD_BG"])
        ax.plot(list(resumo.keys()), list(resumo.values()), marker='o', color=self.cores["PRIMARY"], linewidth=2)
        ax.set_facecolor(self.cores["CARD_BG"])
        ax.set_title("Faturamento por Período (R$)", color="white")
        ax.tick_params(colors='white')
        
        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def renderizar_tabela(self):
        total_geral = sum(float(item['valor']) for item in self.dados_filtrados)
        ctk.CTkLabel(self.table_container, text=f"TOTAL ARRECADADO NO PERÍODO: R$ {total_geral:.2f}", 
                     font=("Arial", 16, "bold"), text_color="#2ecc71").pack(pady=10)
        
        header = "Data | Vendedor | Categoria | Valor"
        ctk.CTkLabel(self.table_container, text=header, font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        
        for d in self.dados_filtrados:
            txt = f"{d['data'].strftime('%d/%m/%y %H:%M')} | {d['vendedor']} | {d['categoria']} | R$ {d['valor']:.2f}"
            ctk.CTkLabel(self.table_container, text=txt).pack(anchor="w", padx=10)

    # --- FUNÇÕES AUXILIARES DE UI ---
    def criar_campo_filtro(self, master, label, row, col, default):
        ctk.CTkLabel(master, text=label).grid(row=row, column=col, padx=10, pady=5)
        entry = ctk.CTkEntry(master)
        entry.insert(0, default)
        entry.grid(row=row, column=col+1, padx=10, pady=5, sticky="ew")
        return entry

    def criar_combo_filtro(self, master, label, row, col, options):
        ctk.CTkLabel(master, text=label).grid(row=row, column=col, padx=10, pady=5)
        combo = ctk.CTkComboBox(master, values=options)
        combo.set(options[0])
        combo.grid(row=row, column=col+1, padx=10, pady=5, sticky="ew")
        return combo

    def exportar_pdf(self):
        if not self.dados_filtrados: return
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", title="Salvar Relatório")
        if not caminho: return
        
        c = canvas.Canvas(caminho, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "RELATÓRIO GERENCIAL DE VENDAS")
        c.setFont("Helvetica", 10)
        c.drawString(50, 730, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        y = 700
        for d in self.dados_filtrados:
            txt = f"{d['data']} - Operador: {d['vendedor']} - Valor: R$ {d['valor']}"
            c.drawString(50, y, txt)
            y -= 20
            if y < 50: c.showPage(); y = 750
            
        c.save()
        messagebox.showinfo("PDF", "Relatório exportado com sucesso!")

    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app, usuario=sessao.nome, perfil=sessao.perfil)

def mostrar_relatorios(app):
    RelatoriosApp(app)