# === CORES ===
PRIMARY_COLOR         = "#E98C41"
HOVER_COLOR           = "#E2B539"
BACKGROUND_COLOR      = "#F8F8F8"
TEXT_COLOR            = "#333333"
CARD_CAIXA_COLOR      = "#36A84A"
CARD_ESTOQUE_COLOR    = "#2F80ED"
CARD_RELATORIOS_COLOR = "#F2994A"
CARD_CADASTROS_COLOR  = "#7C4DFF"
CARD_COLOR            = "#FFFFFF"

# CORES PARA MODO CLARO E ESCURO
def get_colors(app):
    if app.modo_escuro:
        return {
            "PRIMARY": "#FF7043",
            "HOVER": "#FF5722",
            "BACKGROUND": "#121212",
            "CARD_BG": "#1E1E1E",
            "TEXT_PRIMARY": "white",
            "TEXT_SECONDARY": "#BBBBBB",
            "ENTRY_BG": "#333333",
        }
    else:
        return {
            "PRIMARY": "#FF7043",
            "HOVER": "#FF5722",
            "BACKGROUND": "#F5F5F5",
            "CARD_BG": "#FFFFFF",
            "TEXT_PRIMARY": "black",
            "TEXT_SECONDARY": "#666666",
            "ENTRY_BG": "#E0E0E0",
        }