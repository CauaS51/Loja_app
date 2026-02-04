from data.conexao import conectar
import data.sessao as sessao
from datetime import datetime # Importante: Adicione esta linha

def buscar_relatorio_vendas(inicio, fim, funcionario="Todos", categoria="Todos", pagamento="Todos"):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    try:
        query = """
            SELECT DISTINCT 
                v.ID_Venda, 
                v.Data_Venda as data, 
                c.Nome as vendedor, 
                v.Forma_Pagamento as tipo, 
                v.Total as valor
            FROM Vendas v
            JOIN Funcionarios_Loja f ON v.ID_Funcionario = f.ID_Funcionario
            JOIN Contas c ON f.ID_Conta = c.ID_Conta
            LEFT JOIN Itens_Venda iv ON v.ID_Venda = iv.ID_Venda
            LEFT JOIN Produtos p ON iv.ID_Produto = p.ID_Produto
            LEFT JOIN Categorias cat ON p.Categoria_ID = cat.ID_Categoria
            WHERE v.ID_Loja = %s 
            AND DATE(v.Data_Venda) BETWEEN %s AND %s
        """
        params = [sessao.loja_id, inicio, fim]
        
        if funcionario != "Todos":
            query += " AND c.Nome = %s"; params.append(funcionario)
        if pagamento != "Todos":
            query += " AND v.Forma_Pagamento = %s"; params.append(pagamento)
        if categoria != "Todos":
            query += " AND cat.Nome = %s"; params.append(categoria)

        query += " ORDER BY v.Data_Venda DESC"
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        con.close()

def buscar_status_caixas():
    if not sessao.loja_id: return []
    con = conectar()
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.ID_Caixa, c.Status, c.Valor_Inicial, c.Valor_Final, 
                   u.Nome as Operador, c.Data_Abertura, c.Data_Fechamento
            FROM Caixas c
            JOIN Funcionarios_Loja f ON c.ID_Funcionario = f.ID_Funcionario
            JOIN Contas u ON f.ID_Conta = u.ID_Conta
            WHERE c.ID_Loja = %s 
            ORDER BY c.Data_Abertura DESC LIMIT 10
        """, (sessao.loja_id,))
        return cursor.fetchall()
    finally:
        con.close()

def resumo_faturamento_mes():
    con = conectar()
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT IFNULL(SUM(Total), 0) as total_mes, COUNT(ID_Venda) as qtd_vendas
            FROM Vendas 
            WHERE ID_Loja = %s 
            AND MONTH(Data_Venda) = MONTH(CURRENT_DATE())
            AND YEAR(Data_Venda) = YEAR(CURRENT_DATE())
        """, (sessao.loja_id,))
        return cursor.fetchone()
    finally:
        con.close()

def salvar_venda_completa(total, forma_pagamento, itens_carrinho):
    """
    Grava a venda e baixa o estoque usando os nomes de variáveis do seu sessao.py
    """
    # Validação de segurança usando seus nomes de variáveis
    if not sessao.funcionario_id or not sessao.loja_id:
        print(f"ERRO: Sessão inválida. Funcionario: {sessao.funcionario_id}, Loja: {sessao.loja_id}")
        return False

    con = conectar()
    cursor = con.cursor()
    
    try:
        con.start_transaction()
        agora = datetime.now()

        # 1. Inserir a Venda
        # O ID_Funcionario no banco recebe o sessao.funcionario_id
        sql_venda = """
            INSERT INTO Vendas (ID_Loja, ID_Funcionario, Data_Venda, Total, Forma_Pagamento)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_venda, (
            int(sessao.loja_id), 
            int(sessao.funcionario_id), 
            agora, 
            float(total), 
            str(forma_pagamento)
        ))
        venda_id = cursor.lastrowid

        # 2. Inserir Itens e Baixar Estoque
        sql_itens = "INSERT INTO Itens_Venda (ID_Venda, ID_Produto, Quantidade, Preco_Unitario, Subtotal) VALUES (%s, %s, %s, %s, %s)"
        sql_estoque = "UPDATE Produtos SET Estoque = Estoque - %s WHERE ID_Produto = %s"
        
        for dados in itens_carrinho.values():
            p = dados["produto"]
            id_pro = p["codigo"] 
            qtd = int(dados["quantidade"])
            preco = float(p["preco"])
            subtotal = qtd * preco

            cursor.execute(sql_itens, (venda_id, id_pro, qtd, preco, subtotal))
            cursor.execute(sql_estoque, (qtd, id_pro))

        con.commit()
        return True

    except Exception as e:
        con.rollback()
        print(f"Erro Crítico no Banco: {e}")
        return False
    finally:
        con.close()