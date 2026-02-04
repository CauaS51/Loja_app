import customtkinter as ctk
from tkinter import messagebox
import data.colors as colors
import data.sessao as sessao
from decimal import Decimal
import datetime
import random
import string
import os
# Importação da função do CRUD atualizada
from crud.crud_relatorios import salvar_venda_completa

# === CLASSE DE PERSISTÊNCIA (LOGS EM TXT) ===
class HistoricoVendas:
    @staticmethod
    def salvar_venda_txt(dados_venda):
        """Grava backup físico da venda em /logs"""
        pasta_logs = "logs"
        if not os.path.exists(pasta_logs):
            os.makedirs(pasta_logs)
            
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
        arquivo_nome = f"{pasta_logs}/vendas_{data_atual}.txt"
        hora_venda = datetime.datetime.now().strftime("%H:%M:%S")
        
        try:
            with open(arquivo_nome, "a", encoding="utf-8") as f:
                f.write("="*60 + "\n")
                f.write(f"VENDA: {data_atual} | HORA: {hora_venda}\n")
                f.write(f"OPERADOR: {dados_venda.get('operador', 'N/A')}\n")
                f.write(f"MÉTODO: {dados_venda.get('metodo')}\n")
                f.write(f"TOTAL: R$ {dados_venda.get('total'):.2f}\n")
                f.write("="*60 + "\n\n")
            return True
        except Exception as e:
            print(f"Erro backup TXT: {e}")
            return False

# === CLASSE DE INTERFACE DE PAGAMENTO ===
class AbrirPagamento:
    def __init__(self, app, total_venda, itens_carrinho, callback_sucesso):
        self.app = app
        # Conversão segura para Decimal
        self.total_venda = Decimal(str(total_venda))
        self.itens_carrinho = itens_carrinho
        self.callback_sucesso = callback_sucesso
        
        self.forma_pagamento = None
        self.payment_buttons = {}
        self.valor_recebido_var = ctk.StringVar(value="")
        self.parcelas_var = ctk.StringVar(value="1x (Sem Juros)")
        
        # Inicia a interface
        self.cores = colors.get_colors()
        self.janela = ctk.CTkToplevel(self.app)
        self.janela.title("Finalizar Venda")
        self.janela.geometry("600x820")
        self.janela.grab_set()  # Mantém o foco nesta janela
        self.janela.configure(fg_color=self.cores["BACKGROUND"])
        
        # Garante que a janela fique no topo
        self.janela.attributes("-topmost", True)
        
        self.montar_tela()

    def montar_tela(self):
        # Header com Valor Total
        header = ctk.CTkFrame(self.janela, fg_color=self.cores["PRIMARY"], height=120, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="TOTAL A PAGAR", font=("Segoe UI", 14), text_color="white").pack(pady=(20, 0))
        ctk.CTkLabel(header, text=f"R$ {self.total_venda:.2f}", font=("Segoe UI", 48, "bold"), text_color="white").pack(pady=(0, 20))

        self.container = ctk.CTkFrame(self.janela, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(self.container, text="FORMA DE PAGAMENTO", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        
        frame_metodos = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_metodos.pack(fill="x", pady=10)
        frame_metodos.grid_columnconfigure((0, 1), weight=1)

        metodos = [("💵 DINHEIRO", "DINHEIRO"), ("📱 PIX", "PIX"), ("💳 CRÉDITO", "CREDITO"), ("💳 DÉBITO", "DEBITO")]
        for i, (label, valor) in enumerate(metodos):
            btn = ctk.CTkButton(frame_metodos, text=label, height=55, font=("Segoe UI", 14, "bold"),
                                fg_color=self.cores["CARD_BG"], text_color=self.cores["TEXT_PRIMARY"],
                                border_width=2, border_color=self.cores["PRIMARY"],
                                command=lambda v=valor: self.selecionar_pagamento(v))
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
            self.payment_buttons[valor] = btn

        self.frame_detalhes = ctk.CTkFrame(self.container, fg_color=self.cores["CARD_BG"], corner_radius=15)
        self.frame_detalhes.pack(fill="x", pady=15)
        self.container_dinamico = ctk.CTkFrame(self.frame_detalhes, fg_color="transparent")
        self.container_dinamico.pack(padx=25, pady=25, fill="both", expand=True)

        self.lbl_placeholder = ctk.CTkLabel(self.container_dinamico, text="Selecione um método de pagamento", font=("Segoe UI", 13, "italic"), text_color="gray")
        self.lbl_placeholder.pack(pady=20)

        ctk.CTkLabel(self.container, text="OBSERVAÇÕES", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.txt_obs = ctk.CTkEntry(self.container, height=45, placeholder_text="Notas extras...", fg_color=self.cores["ENTRY_BG"])
        self.txt_obs.pack(fill="x", pady=5)

        self.btn_confirmar = ctk.CTkButton(self.container, text="FINALIZAR E REGISTRAR", height=65,
                                           font=("Segoe UI", 22, "bold"), fg_color="#10B981", 
                                           command=self.processar_venda)
        self.btn_confirmar.pack(side="bottom", fill="x", pady=20)

    def selecionar_pagamento(self, forma):
        self.forma_pagamento = forma
        for v, btn in self.payment_buttons.items():
            btn.configure(fg_color=self.cores["PRIMARY"] if v == forma else self.cores["CARD_BG"],
                          text_color="white" if v == forma else self.cores["TEXT_PRIMARY"])
        for widget in self.container_dinamico.winfo_children(): widget.destroy()

        if forma == "DINHEIRO": self.montar_ui_dinheiro()
        elif forma == "PIX": self.montar_ui_pix()
        elif forma == "CREDITO": self.montar_ui_credito()
        else: ctk.CTkLabel(self.container_dinamico, text="💳 Aguardando cartão de DÉBITO...", font=("Segoe UI", 14, "bold")).pack()

    def montar_ui_dinheiro(self):
        ctk.CTkLabel(self.container_dinamico, text="VALOR RECEBIDO:", font=("Segoe UI", 12, "bold")).pack()
        self.ent_recebido = ctk.CTkEntry(self.container_dinamico, textvariable=self.valor_recebido_var, width=200, height=45, font=("Segoe UI", 20))
        self.ent_recebido.pack(pady=10)
        self.ent_recebido.focus()
        self.lbl_troco = ctk.CTkLabel(self.container_dinamico, text="TROCO: R$ 0,00", font=("Segoe UI", 18, "bold"), text_color="#10B981")
        self.lbl_troco.pack()
        self.ent_recebido.bind("<KeyRelease>", self.calcular_troco)

    def montar_ui_pix(self):
        chave = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        ctk.CTkLabel(self.container_dinamico, text="ESCANEIE O QR CODE", font=("Segoe UI", 14, "bold")).pack()
        ctk.CTkLabel(self.container_dinamico, text="🔳", font=("Segoe UI", 80)).pack()
        entry_chave = ctk.CTkEntry(self.container_dinamico, width=350, font=("Consolas", 10), justify="center")
        entry_chave.insert(0, f"PIX_PAY_{chave}")
        entry_chave.configure(state="readonly")
        entry_chave.pack(pady=5)

    def montar_ui_credito(self):
        opcoes = [f"{i}x de R$ {(self.total_venda/i):.2f}" for i in range(1, 13)]
        self.combo_parcelas = ctk.CTkComboBox(self.container_dinamico, values=opcoes, variable=self.parcelas_var, width=350, height=40)
        self.combo_parcelas.pack(pady=10)

    def calcular_troco(self, event=None):
        try:
            recebido_str = self.valor_recebido_var.get().replace(",", ".")
            if not recebido_str: return
            recebido = Decimal(recebido_str)
            troco = recebido - self.total_venda
            self.lbl_troco.configure(text=f"TROCO: R$ {max(0, troco):.2f}", 
                                     text_color="#10B981" if troco >= 0 else "#EF4444")
        except: pass

    def processar_venda(self):
        if not self.forma_pagamento:
            messagebox.showwarning("Aviso", "Selecione a forma de pagamento!")
            return

        sucesso_banco = salvar_venda_completa(
            total=float(self.total_venda),
            forma_pagamento=self.forma_pagamento,
            itens_carrinho=self.itens_carrinho
        )

        if sucesso_banco:
            dados_log = {
                "total": float(self.total_venda),
                "metodo": self.forma_pagamento,
                "operador": getattr(sessao, 'nome', 'N/A'),
                "obs": self.txt_obs.get()
            }
            HistoricoVendas.salvar_venda_txt(dados_log)

            messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
            self.janela.destroy()
       
        else:
            # Se cair aqui, o erro 1452 foi capturado ou os IDs na sessão estão nulos
            messagebox.showerror("Erro de Banco", 
                               "Não foi possível registrar a venda.\n\n"
                               "Motivo: Falha de autenticação do funcionário ou loja.\n"
                               "Por favor, verifique se o login foi realizado corretamente.")

# === FUNÇÃO DE ENTRADA ===
def abrir_pagamento(app, total, itens, callback):
    AbrirPagamento(app, total, itens, callback)