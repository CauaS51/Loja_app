import customtkinter as ctk
from tkinter import messagebox
import data.colors as colors
from data.colors import *
import data.sessao as sessao

class RelatoriosApp:
    def __init__(self, app):
        self.app = app
        self.gerar_tela_relatorios()

    def gerar_tela_relatorios(self):
        for w in self.app.winfo_children():
            w.destroy()

        self.app.title("Relatórios")
        cores = colors.get_colors()

        # === HEADER ===
        header = ctk.CTkFrame(self.app, fg_color=cores["PRIMARY"], height=80, corner_radius=0)
        header.pack(fill="x")
        header.grid_columnconfigure(0, weight=0)  # botão voltar
        header.grid_columnconfigure(1, weight=1)  # título
        header.grid_columnconfigure(2, weight=0)  # tema

        # BOTÃO VOLTAR
        btn_voltar = ctk.CTkButton(
            header, text="⬅", width=40, height=40, font=ctk.CTkFont(size=20),
            corner_radius=12, text_color=cores["TEXT_PRIMARY"], fg_color=cores["ENTRY_BG"], hover_color=cores["HOVER"],
            command=self.voltar_menu
        )
        btn_voltar.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # TÍTULO
        title_label = ctk.CTkLabel(
            header, text="📊 Relatórios de Vendas",
            text_color="white",
            font=ctk.CTkFont("Segoe UI", 26, "bold")
        )
        title_label.grid(row=0, column=1, padx=(0,30), pady=20, sticky="w")

        #  BOTÃO ALTERNAR TEMA 
        def alternar_tema():
            colors.alternar_tema()
            self.gerar_tela_relatorios()

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
        main_frame.grid_rowconfigure(3, weight=1) # Para o frame de resultados

        # Seleção de Período
        periodo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        periodo_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        periodo_frame.grid_columnconfigure(0, weight=1)
        periodo_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(periodo_frame, text="Data Início:", text_color=cores["TEXT_PRIMARY"]).grid(row=0, column=0, sticky="w", padx=5)
        self.entry_data_inicio = ctk.CTkEntry(periodo_frame, placeholder_text="DD/MM/AAAA", width=150)
        self.entry_data_inicio.grid(row=1, column=0, sticky="w", padx=5)

        ctk.CTkLabel(periodo_frame, text="Data Fim:", text_color=cores["TEXT_PRIMARY"]).grid(row=0, column=1, sticky="w", padx=5)
        self.entry_data_fim = ctk.CTkEntry(periodo_frame, placeholder_text="DD/MM/AAAA", width=150)
        self.entry_data_fim.grid(row=1, column=1, sticky="w", padx=5)

        # Botão Gerar Relatório
        btn_gerar_relatorio = ctk.CTkButton(
            main_frame, text="Gerar Relatório",
            fg_color=cores["PRIMARY"], hover_color=cores["HOVER"],
            text_color="white", font=ctk.CTkFont(size=16, weight="bold"),
            command=self.gerar_relatorio
        )
        btn_gerar_relatorio.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Área de exibição do relatório
        self.report_display_frame = ctk.CTkScrollableFrame(main_frame, fg_color=cores["CARD_BG"], corner_radius=12)
        self.report_display_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.report_display_frame, text="Nenhum relatório gerado ainda.",
            text_color=cores["TEXT_SECONDARY"], font=ctk.CTkFont(size=14)
        ).pack(pady=20)

    def voltar_menu(self):
        from data import menu
        menu.mostrar_menu(self.app, usuario=sessao.usuario, perfil=sessao.perfil)

    def gerar_relatorio(self):
        data_inicio_str = self.entry_data_inicio.get()
        data_fim_str = self.entry_data_fim.get()

        # Validação de datas (simplificada para o exemplo)
        if not data_inicio_str or not data_fim_str:
            messagebox.showwarning("Aviso", "Por favor, preencha as datas de início e fim.")
            return
        
        # Aqui você adicionaria a lógica para buscar os dados de vendas
        # e gerar o relatório com base nas datas. 
        # Por enquanto, vamos simular um relatório.

        # Limpa a área de exibição anterior
        for w in self.report_display_frame.winfo_children():
            w.destroy()

        cores = colors.get_colors()

        # Exemplo de conteúdo do relatório
        ctk.CTkLabel(
            self.report_display_frame, text=f"Relatório de Vendas de {data_inicio_str} a {data_fim_str}",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=cores["PRIMARY"]
        ).pack(pady=10)

        # Dados simulados
        relatorio_data = [
            {"produto": "Nenhum Produto Vendido", "quantidade": 0, "total": 0},
        ]

        total_geral = 0
        for item in relatorio_data:
            frame_item = ctk.CTkFrame(self.report_display_frame, fg_color=cores["BACKGROUND"], corner_radius=8)
            frame_item.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                frame_item, text=f"{item['produto']}: {item['quantidade']} unidades - R$ {item['total']:.2f}",
                text_color=cores["TEXT_PRIMARY"], font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=10, pady=5)
            total_geral += item['total']
        
        ctk.CTkLabel(
            self.report_display_frame, text=f"\nTotal de Vendas no Período: R$ {total_geral:.2f}",
            font=ctk.CTkFont(size=16, weight="bold"), text_color=cores["PRIMARY"]
        ).pack(pady=10)


def mostrar_relatorios(app):
    RelatoriosApp(app)

