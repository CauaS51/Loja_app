import customtkinter as ctk
import json
import os

# ==========================
# TEMA PADRÃO (FALLBACK)
# ==========================
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

# Tema customizado da loja (vem do banco ou arquivo)
TEMA_ATUAL = None

# ==========================
# CARREGAR TEMA DE ARQUIVO
# ==========================
def carregar_tema(path):
    global TEMA_ATUAL

    if not os.path.exists(path):
        print("Tema não encontrado, usando apenas padrão.")
        TEMA_ATUAL = None
        return

    with open(path, "r", encoding="utf-8") as f:
        TEMA_ATUAL = json.load(f)


# ==========================
# SALVAR TEMA EM ARQUIVO
# ==========================
def salvar_tema(path, tema_dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tema_dict, f, indent=4, ensure_ascii=False)


# ==========================
# OBTER CORES ATUAIS
# ==========================
def get_colors():
    modo = ctk.get_appearance_mode()  # "Light" ou "Dark"

    # Sempre começa com o tema padrão
    cores_base = TEMA_PADRAO[modo].copy()

    # Se houver tema customizado da loja, faz merge
    if TEMA_ATUAL and modo in TEMA_ATUAL:
        cores_base.update(TEMA_ATUAL[modo])

    return cores_base

# ==========================
# ALTERNAR MODO LIGHT/DARK
# ==========================
def alternar_tema():
    modo_atual = ctk.get_appearance_mode()
    ctk.set_appearance_mode("Light" if modo_atual == "Dark" else "Dark")

# ==========================
# APLICAR TEMA VINDO DO BANCO
# ==========================
def aplicar_tema_customizado(tema_dict):
    global TEMA_ATUAL

    try:
        # Se vier como string JSON do banco
        if isinstance(tema_dict, str):
            tema_dict = json.loads(tema_dict)

        # Se já vier no formato Light/Dark
        if "Light" in tema_dict or "Dark" in tema_dict:
            TEMA_ATUAL = tema_dict
        else:
            # Se vier só um dicionário simples de cores
            modo = ctk.get_appearance_mode()
            TEMA_ATUAL = {modo: tema_dict}

    except Exception as e:
        print("Erro ao aplicar tema customizado:", e)
        TEMA_ATUAL = None

# ==========================
# RESETAR TEMA PARA PADRÃO
# ==========================
def resetar_tema():
    global TEMA_ATUAL
    TEMA_ATUAL = None
    modo_atual = ctk.get_appearance_mode()  
    ctk.set_appearance_mode(modo_atual)
