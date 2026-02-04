# crud_relatorios.py
from data.conexao import conectar
from datetime import datetime
import matplotlib.pyplot as plt

# =========================================
# CRIAR RELATÓRIO
# =========================================
def criar_relatorio(id_loja, id_conta, tipo, data_inicio=None, data_fim=None):
    con = conectar()
    if con is None:
        return None

    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO Relatorios (ID_Loja, ID_Conta, Tipo, Data_inicio, Data_fim)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_loja, id_conta, tipo, data_inicio, data_fim))
        con.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao criar relatório:", e)
        return None
    finally:
        con.close()


# =========================================
# LISTAR RELATÓRIOS
# =========================================
def listar_relatorios(id_loja=None):
    con = conectar()
    if con is None:
        return []

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
            SELECT r.ID_Relatorio, r.Tipo, r.Data_inicio, r.Data_fim, c.Nome AS Usuario
            FROM Relatorios r
            LEFT JOIN Contas c ON r.ID_Conta = c.ID_Conta
        """
        params = []
        if id_loja:
            sql += " WHERE r.ID_Loja=%s"
            params.append(id_loja)
        sql += " ORDER BY r.ID_Relatorio DESC"
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar relatórios:", e)
        return []
    finally:
        con.close()


# =========================================
# EXCLUIR RELATÓRIO
# =========================================
def excluir_relatorio(id_relatorio):
    con = conectar()
    if con is None:
        return False

    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Relatorios WHERE ID_Relatorio=%s", (id_relatorio,))
        con.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao excluir relatório:", e)
        return False
    finally:
        con.close()


# =========================================
# TOTAL DE VENDAS (opcional por período e funcionário)
# =========================================
def total_vendas(id_loja, data_inicio=None, data_fim=None, id_funcionario=None):
    con = conectar()
    if con is None:
        return None

    try:
        cursor = con.cursor(dictionary=True)
        sql = "SELECT COUNT(*) AS total_vendas, SUM(Total) AS faturamento_total FROM Vendas WHERE ID_Loja=%s"
        params = [id_loja]

        if data_inicio:
            sql += " AND Data_Venda >= %s"
            params.append(data_inicio)
        if data_fim:
            sql += " AND Data_Venda <= %s"
            params.append(data_fim)
        if id_funcionario:
            sql += " AND ID_Funcionario=%s"
            params.append(id_funcionario)

        cursor.execute(sql, tuple(params))
        return cursor.fetchone()
    except Exception as e:
        print("Erro ao gerar relatório de vendas:", e)
        return None
    finally:
        con.close()


# =========================================
# TOTAL DE COMPRAS (opcional por período)
# =========================================
def total_compras(id_loja, data_inicio=None, data_fim=None):
    con = conectar()
    if con is None:
        return None

    try:
        cursor = con.cursor(dictionary=True)
        sql = "SELECT COUNT(*) AS total_compras, SUM(Total) AS gasto_total FROM Compras WHERE ID_Loja=%s"
        params = [id_loja]

        if data_inicio:
            sql += " AND Data_Compra >= %s"
            params.append(data_inicio)
        if data_fim:
            sql += " AND Data_Compra <= %s"
            params.append(data_fim)

        cursor.execute(sql, tuple(params))
        return cursor.fetchone()
    except Exception as e:
        print("Erro ao gerar relatório de compras:", e)
        return None
    finally:
        con.close()


# =========================================
# PRODUTOS COM ESTOQUE BAIXO
# =========================================
def produtos_estoque_baixo(id_loja):
    con = conectar()
    if con is None:
        return []

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT Nome, Estoque, Estoque_Minimo
            FROM Produtos
            WHERE ID_Loja=%s AND Estoque <= Estoque_Minimo AND Ativo=TRUE
        """, (id_loja,))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao gerar relatório de estoque baixo:", e)
        return []
    finally:
        con.close()


# =========================================
# VENDAS POR FUNCIONÁRIO
# =========================================
def vendas_por_funcionario(id_loja, data_inicio=None, data_fim=None):
    con = conectar()
    if con is None:
        return []

    try:
        cursor = con.cursor(dictionary=True)
        sql = """
            SELECT f.ID_Funcionario, fl.ID_Conta, c.Nome AS Nome_Funcionario,
                   COUNT(v.ID_Venda) AS total_vendas, SUM(v.Total) AS faturamento_total
            FROM Vendas v
            LEFT JOIN Funcionarios_Loja f ON v.ID_Funcionario = f.ID_Funcionario
            LEFT JOIN Contas c ON f.ID_Conta = c.ID_Conta
            WHERE v.ID_Loja=%s
        """
        params = [id_loja]

        if data_inicio:
            sql += " AND v.Data_Venda >= %s"
            params.append(data_inicio)
        if data_fim:
            sql += " AND v.Data_Venda <= %s"
            params.append(data_fim)

        sql += " GROUP BY f.ID_Funcionario, fl.ID_Conta, c.Nome"
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao gerar relatório de vendas por funcionário:", e)
        return []
    finally:
        con.close()


# =========================================
# GRÁFICO: VENDAS NO MÊS
# =========================================
def grafico_vendas_mes(id_loja, ano, mes):
    con = conectar()
    if con is None:
        return None

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT DAY(Data_Venda) AS dia, SUM(Total) AS faturamento
            FROM Vendas
            WHERE ID_Loja=%s AND YEAR(Data_Venda)=%s AND MONTH(Data_Venda)=%s
            GROUP BY DAY(Data_Venda)
            ORDER BY dia
        """, (id_loja, ano, mes))
        dados = cursor.fetchall()

        dias = [d["dia"] for d in dados]
        faturamento = [d["faturamento"] or 0 for d in dados]

        plt.figure(figsize=(10, 5))
        plt.bar(dias, faturamento, color="#4CAF50")
        plt.xlabel("Dia do Mês")
        plt.ylabel("Faturamento (R$)")
        plt.title(f"Vendas do Mês {mes}/{ano}")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.show()

    except Exception as e:
        print("Erro ao gerar gráfico de vendas:", e)
    finally:
        con.close()

# =========================================
# RELATÓRIOS DETALHADOS
# =========================================

def buscar_relatorio_vendas(id_loja, data_inicio, data_fim):
    """
    Retorna lista de vendas detalhadas por produto para a loja e período.
    """
    con = conectar()
    if con is None:
        return []

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.Data_Venda AS data,
                   p.Nome AS produto,
                   iv.Quantidade AS quantidade,
                   iv.Subtotal AS subtotal
            FROM Vendas v
            INNER JOIN Itens_Venda iv ON v.ID_Venda = iv.ID_Venda
            INNER JOIN Produtos p ON iv.ID_Produto = p.ID_Produto
            WHERE v.ID_Loja = %s AND v.Data_Venda BETWEEN %s AND %s
            ORDER BY v.Data_Venda ASC
        """, (id_loja, data_inicio, data_fim))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao buscar relatório de vendas:", e)
        return []
    finally:
        con.close()


def buscar_relatorio_estoque(id_loja):
    """
    Retorna produtos da loja com estoque e preço.
    """
    con = conectar()
    if con is None:
        return []

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT Nome AS produto, Estoque AS estoque, Preco AS preco
            FROM Produtos
            WHERE ID_Loja = %s AND Ativo = TRUE
            ORDER BY Nome ASC
        """, (id_loja,))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao buscar relatório de estoque:", e)
        return []
    finally:
        con.close()