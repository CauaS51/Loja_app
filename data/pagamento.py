import customtkinter as ctk
from tkinter import messagebox
from decimal import Decimal, ROUND_HALF_UP
import data.colors as colors

class JanelaPagamento(ctk.CTkToplevel):
    def __init__(self, parent, valor_total, callback_finalizar):
        super().__init__(parent)
        self.title("Finalizar Pagamento")
        self.geometry("400x500")
        self.grab_set()  # Bloqueia a janela principal até fechar esta
        
        self.valor_total = Decimal(str(valor_total))
        self.callback_finalizar = callback_finalizar
        self.cores = colors.get_colors()
        self.configure(fg_color=self.cores["BACKGROUND"])
        
        self.criar_layout()

    def criar_layout(self):
        # Valor Total
        ctk.CTkLabel(self, text="TOTAL A PAGAR", font=("Segoe UI", 16)).pack(pady=(20, 0))
        ctk.CTkLabel(self, text=f"R$ {self.valor_total:.2f}", 
                     font=("Segoe UI", 32, "bold"), text_color=self.cores["PRIMARY"]).pack(pady=10)

        # Seleção de Método
        ctk.CTkLabel(self, text="Forma de Pagamento:").pack(pady=5)
        self.metodo_var = ctk.StringVar(value="Dinheiro")
        metodos = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX"]
        self.combo_metodo = ctk.CTkComboBox(self, values=metodos, variable=self.metodo_var, command=self.verificar_metodo)
        self.combo_metodo.pack(pady=10)

        # Campo de valor recebido (apenas para dinheiro)
        self.frame_dinheiro = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_dinheiro.pack(pady=10, fill="x", padx=40)
        
        ctk.CTkLabel(self.frame_dinheiro, text="Valor Recebido:").pack()
        self.entry_recebido = ctk.CTkEntry(self.frame_dinheiro, placeholder_text="0,00")
        self.entry_recebido.pack(pady=5)
        self.entry_recebido.bind("<KeyRelease>", self.calcular_troco)

        self.lbl_troco = ctk.CTkLabel(self.frame_dinheiro, text="Troco: R$ 0,00", font=("Segoe UI", 14, "bold"))
        self.lbl_troco.pack(pady=5)

        # Botão Finalizar
        self.btn_confirmar = ctk.CTkButton(self, text="CONFIRMAR (F10)", 
                                          fg_color=self.cores["PRIMARY"],
                                          command=self.processar_pagamento, height=50)
        self.btn_confirmar.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.bind("<Return>", lambda e: self.processar_pagamento())

    def verificar_metodo(self, escolha):
        if escolha == "Dinheiro":
            self.frame_dinheiro.pack(pady=10, fill="x", padx=40)
        else:
            self.frame_dinheiro.pack_forget()

    def calcular_troco(self, event=None):
        try:
            recebido = Decimal(self.entry_recebido.get().replace(",", "."))
            troco = recebido - self.valor_total
            if troco >= 0:
                self.lbl_troco.configure(text=f"Troco: R$ {troco:.2f}", text_color="green")
            else:
                self.lbl_troco.configure(text="Valor Insuficiente", text_color="red")
        except:
            self.lbl_troco.configure(text="Troco: R$ 0,00", text_color=self.cores["TEXT_PRIMARY"])

    def processar_pagamento(self):
        metodo = self.metodo_var.get()
        
        if metodo == "Dinheiro":
            try:
                recebido = Decimal(self.entry_recebido.get().replace(",", "."))
                if recebido < self.valor_total:
                    messagebox.showwarning("Erro", "Valor recebido é menor que o total.")
                    return
            except:
                messagebox.showerror("Erro", "Insira um valor válido.")
                return

        messagebox.showinfo("Sucesso", f"Venda finalizada com {metodo}!")
        self.callback_finalizar() # Limpa o carrinho no caixa.py
        self.destroy()

def abrir_pagamento(parent, valor_total, callback_finalizar):
    JanelaPagamento(parent, valor_total, callback_finalizar)