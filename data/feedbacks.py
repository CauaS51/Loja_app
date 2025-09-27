import customtkinter as ctk
from tkinter import messagebox
import os
from datetime import datetime

# === FUNÇÃO: COLETAR SATISFAÇÃO DO CLIENTE ===
def coletar_satisfacao():
    satisfacao_win = ctk.CTkToplevel()
    satisfacao_win.title("Sua Opinião é Importante!")
    satisfacao_win.geometry("500x450")
    satisfacao_win.transient() # Torna a janela de satisfação modal
    satisfacao_win.grab_set()  # Garante que o foco esteja nesta janela

    ctk.CTkLabel(
        satisfacao_win,
        text="Descreva sua experiência com a loja:",
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(pady=20)

    text_satisfacao = ctk.CTkTextbox(
        satisfacao_win,
        width=400, height=150,
        corner_radius=10,
        font=ctk.CTkFont(size=14)
    )
    text_satisfacao.pack(pady=10)

    def salvar_feedback(feedback):
        """Salva o feedback em um arquivo de texto com data e hora"""
        try:
            # Cria o diretório se não existir
            if not os.path.exists("feedbacks"):
                os.makedirs("feedbacks")
            
            # Nome do arquivo com data
            arquivo = "feedbacks/feedbacks_clientes.txt"
            
            # Data e hora atual
            agora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            
            # Salva no arquivo
            with open(arquivo, "a", encoding="utf-8") as f:
                f.write(f"=== FEEDBACK - {agora} ===\n")
                f.write(f"{feedback}\n")
                f.write("-" * 50 + "\n\n")
            
            return True
        except Exception as e:
            print(f"Erro ao salvar feedback: {e}")
            return False

    def enviar_satisfacao():
        feedback = text_satisfacao.get("1.0", "end-1c").strip()
        if feedback:
            if salvar_feedback(feedback):
                messagebox.showinfo("Obrigado!", "Seu feedback foi salvo com sucesso!\nObrigado por sua opinião!")
                print(f"Feedback salvo: {feedback}") # Para fins de demonstração
                satisfacao_win.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível salvar o feedback. Tente novamente.")
        else:
            messagebox.showwarning("Atenção", "Por favor, escreva seu feedback antes de enviar.")

    # Botões
    botoes_frame = ctk.CTkFrame(satisfacao_win, fg_color="transparent")
    botoes_frame.pack(pady=20)

    ctk.CTkButton(
        botoes_frame,
        text="Enviar Feedback",
        width=150, height=40,
        fg_color="#4CAF50",
        hover_color="#388E3C",
        text_color="#FFFFFF",
        corner_radius=10,
        font=ctk.CTkFont(size=14),
        command=enviar_satisfacao
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        botoes_frame,
        text="Ver Feedbacks",
        width=150, height=40,
        fg_color="#2196F3",
        hover_color="#1976D2",
        text_color="#FFFFFF",
        corner_radius=10,
        font=ctk.CTkFont(size=14),
        command=lambda: visualizar_feedbacks()
    ).pack(side="right", padx=10)

# === FUNÇÃO: VISUALIZAR FEEDBACKS SALVOS ===
def visualizar_feedbacks():
    feedbacks_win = ctk.CTkToplevel()
    feedbacks_win.title("Feedbacks dos Clientes")
    feedbacks_win.geometry("600x500")
    feedbacks_win.transient()
    feedbacks_win.grab_set()

    ctk.CTkLabel(
        feedbacks_win,
        text="Feedbacks dos Clientes",
        font=ctk.CTkFont(size=20, weight="bold")
    ).pack(pady=20)

    # Área de texto para mostrar os feedbacks
    text_feedbacks = ctk.CTkTextbox(
        feedbacks_win,
        width=550, height=350,
        corner_radius=10,
        font=ctk.CTkFont(size=12)
    )
    text_feedbacks.pack(pady=10, padx=20)

    # Carregar feedbacks do arquivo
    try:
        arquivo = "feedbacks/feedbacks_clientes.txt"
        if os.path.exists(arquivo):
            with open(arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()
                if conteudo.strip():
                    text_feedbacks.insert("1.0", conteudo)
                else:
                    text_feedbacks.insert("1.0", "Nenhum feedback encontrado ainda.")
        else:
            text_feedbacks.insert("1.0", "Nenhum feedback encontrado ainda.\nO arquivo será criado quando o primeiro feedback for enviado.")
    except Exception as e:
        text_feedbacks.insert("1.0", f"Erro ao carregar feedbacks: {e}")

    # Tornar o texto somente leitura
    text_feedbacks.configure(state="disabled")

    ctk.CTkButton(
        feedbacks_win,
        text="Fechar",
        width=100, height=35,
        fg_color="#757575",
        hover_color="#616161",
        text_color="#FFFFFF",
        corner_radius=10,
        command=feedbacks_win.destroy).pack(pady=20)