import customtkinter as ctk
import json
import os

# Tema padrão interno (fallback)
TEMA_PADRAO = {
    "Light": {
        "PRIMARY": "#E98C41",
        "SECONDARY": "#E98C41",
        "HOVER": "#E2B539",
        "BACKGROUND": "#F5F5F5",
        "BACKGROUND_2": "#F5F5F5",
        "CARD_BG": "#FFFFFF",
        "TEXT_PRIMARY": "#3A3A3A",
        "TEXT_SECONDARY": "#666666",
        "ENTRY_BG": "#E0E0E0",

        "CARD_CAIXA": "#36A84A",
        "CARD_ESTOQUE": "#2F80ED",
        "CARD_RELATORIOS": "#F2994A",
        "CARD_CADASTROS": "#7C4DFF"
    },
    "Dark": {
        "PRIMARY": "#3F71A6",
        "SECONDARY": "#1856FF",
        "HOVER": "#00388D",
        "BACKGROUND": "#2C2C2C",
        "BACKGROUND_2": "#4D80B9",
        "CARD_BG": "#1E1E1E",
        "TEXT_PRIMARY": "#FFFFFF",
        "TEXT_SECONDARY": "#BBBBBB",
        "ENTRY_BG": "#333333",

        "CARD_CAIXA": "#36A84A",
        "CARD_ESTOQUE": "#2F80ED",
        "CARD_RELATORIOS": "#F2994A",
        "CARD_CADASTROS": "#7C4DFF"
    }
}

# Tema ativo
TEMA_ATUAL = TEMA_PADRAO


# ==========================
# CARREGAR TEMA DE ARQUIVO
# ==========================
def carregar_tema(path):
    global TEMA_ATUAL

    if not os.path.exists(path):
        print("Tema não encontrado, usando padrão.")
        TEMA_ATUAL = TEMA_PADRAO
        return

    with open(path, "r", encoding="utf-8") as f:
        TEMA_ATUAL = json.load(f)


# ==========================
# SALVAR TEMA DA LOJA
# ==========================
def salvar_tema(path, tema_dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tema_dict, f, indent=4)


# ==========================
# CORES ATUAIS
# ==========================
def get_colors():
    modo = ctk.get_appearance_mode()  # "Light" ou "Dark"
    return TEMA_ATUAL.get(modo, TEMA_PADRAO[modo])


# ==========================
# ALTERNAR TEMA LIGHT/DARK
# ==========================
def alternar_tema():
    modo_atual = ctk.get_appearance_mode()
    ctk.set_appearance_mode("Light" if modo_atual == "Dark" else "Dark")

