import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import data.colors as colors
import data.sessao as sessao
from crud import crud_relatorios

class RelatoriosApp:
    def __init__(self, app):
        self.app = app
        # Usa as variáveis existentes na sessão
        self.loja_atual = {
            "id": sessao.loja_id,
            "nome": sessao.nome_loja if sessao.nome_loja else "Loja Padrão"
        }

        self.dados_filtrados = []
        self.canvas_grafico = None

        self.gerar_tela_relatorios()

    def gerar_tela_relatorios(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title(f"Sistema PDV - Relatórios ({self.loja_atual['nome']})")
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
            header, text="📊 Relatórios e BI",
            text_color="white", font=ctk.CTkFont("Segoe UI", 26, "bold")
        ).pack(side="left", pady=20)

        # === SCROLLABLE FRAME ===
        main_scroll = ctk.CTkScrollableFrame(self.app, fg_color=cores["BACKGROUND"], corner_radius=0)
        main_scroll.pack(fill="both", expand=True)

        # === FILTROS ===
        filtros_frame = ctk.CTkFrame(main_scroll, fg_color=cores["CARD_BG"], corner_radius=12)
        filtros_frame.pack(fill="x", padx=20, pady=15)
        filtros_frame.grid_columnconfigure((1, 3, 5), weight=1)

        # Tipo Relatório
        ctk.CTkLabel(filtros_frame, text="Relatório:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=10)
        self.combo_tipo_relatorio = ctk.CTkComboBox(filtros_frame, values=["Vendas", "Estoque"], command=self.ajustar_filtros)
        self.combo_tipo_relatorio.set("Vendas")
        self.combo_tipo_relatorio.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Datas
        ctk.CTkLabel(filtros_frame, text="Início:").grid(row=0, column=2, padx=5, pady=10)
        self.entry_data_inicio = ctk.CTkEntry(filtros_frame, placeholder_text="DD/MM/AAAA")
        self.entry_data_inicio.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

        ctk.CTkLabel(filtros_frame, text="Fim:").grid(row=0, column=4, padx=5, pady=10)
        self.entry_data_fim = ctk.CTkEntry(filtros_frame, placeholder_text="DD/MM/AAAA")
        self.entry_data_fim.grid(row=0, column=5, padx=5, pady=10, sticky="ew")

        # Botões
        btn_container = ctk.CTkFrame(main_scroll, fg_color="transparent")
        btn_container.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(btn_container, text="🔍 Gerar Relatório", fg_color=cores["PRIMARY"], command=self.gerar_relatorio).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(btn_container, text="📄 Exportar PDF", fg_color="#27ae60", command=self.exportar_pdf).pack(side="left", expand=True, fill="x", padx=5)

        # Gráfico
        self.chart_frame = ctk.CTkFrame(main_scroll, fg_color=cores["CARD_BG"], height=300, corner_radius=12)
        self.chart_frame.pack(fill="x", padx=20, pady=10)

        # Tabela
        self.table_frame = ctk.CTkFrame(main_scroll, fg_color=cores["CARD_BG"], corner_radius=12)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.data_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.data_container.pack(fill="both", expand=True, padx=10, pady=10)

    def ajustar_filtros(self, escolha):
        if escolha == "Estoque":
            self.entry_data_inicio.configure(state="disabled")
            self.entry_data_fim.configure(state="disabled")
        else:
            self.entry_data_inicio.configure(state="normal")
            self.entry_data_fim.configure(state="normal")

    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app, usuario=sessao.nome, perfil=sessao.perfil)

    def gerar_relatorio(self):
        for w in self.data_container.winfo_children(): w.destroy()
        if self.canvas_grafico: self.canvas_grafico.get_tk_widget().destroy()

        tipo = self.combo_tipo_relatorio.get()

        if tipo == "Vendas":
            try:
                dt_inicio = datetime.strptime(self.entry_data_inicio.get(), "%d/%m/%Y")
                dt_fim = datetime.strptime(self.entry_data_fim.get(), "%d/%m/%Y")
            except:
                messagebox.showerror("Erro", "Datas inválidas")
                return

            # Puxa os dados do crud_relatorios
            dados_brutos = crud_relatorios.buscar_relatorio_vendas(self.loja_atual['id'], dt_inicio, dt_fim)
            self.dados_filtrados = dados_brutos

        else:  # Estoque
            dados_brutos = crud_relatorios.buscar_relatorio_estoque(self.loja_atual['id'])
            self.dados_filtrados = dados_brutos

        if not self.dados_filtrados:
            ctk.CTkLabel(self.data_container, text="Nenhum dado encontrado.").pack(pady=20)
            return

        self.plotar_grafico(self.dados_filtrados, tipo)
        self.renderizar_tabela_tela(tipo)

    def renderizar_tabela_tela(self, tipo):
        cores = colors.get_colors()
        if tipo == "Vendas":
            header = "Data | Produto | Quantidade | Total"
            ctk.CTkLabel(self.data_container, text=header, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
            for d in self.dados_filtrados:
                txt = f"{d['data']} | {d['produto']} | {d['quantidade']} | R$ {d['subtotal']:.2f}"
                ctk.CTkLabel(self.data_container, text=txt, text_color=cores["TEXT_PRIMARY"]).pack(anchor="w", padx=20)
        else:  # Estoque
            header = "Produto | Estoque | Valor Unitário"
            ctk.CTkLabel(self.data_container, text=header, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
            for d in self.dados_filtrados:
                txt = f"{d['produto']} | {d['estoque']} | R$ {d['preco']:.2f}"
                ctk.CTkLabel(self.data_container, text=txt, text_color=cores["TEXT_PRIMARY"]).pack(anchor="w", padx=20)

    def plotar_grafico(self, dados, tipo):
        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        if tipo == "Vendas":
            resumo = {}
            for d in dados: resumo[d['produto']] = resumo.get(d['produto'], 0) + d['subtotal']
            produtos = list(resumo.keys())
            valores = list(resumo.values())
            ax.barh(produtos[::-1], valores[::-1], color='#3b8ed0')
            ax.set_title("Total Vendido por Produto")
        else:
            produtos = [d['produto'] for d in dados]
            estoque = [d['estoque'] for d in dados]
            ax.barh(produtos[::-1], estoque[::-1], color='#27ae60')
            ax.set_title("Estoque Atual por Produto")

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
                    txt = f"{d['data']} - {d['produto']} - Qtde: {d['quantidade']} - Total: R$ {d['subtotal']:.2f}"
                else:
                    txt = f"{d['produto']} - Estoque: {d['estoque']} - R$ {d['preco']:.2f}"
                c.drawString(100, y, txt)
                y -= 20
                if y < 50: c.showPage(); y = 750
            
            c.save()
            messagebox.showinfo("Sucesso", "PDF exportado!")

def mostrar_relatorios(app):
    RelatoriosApp(app)