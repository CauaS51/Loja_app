import mysql.connector
from mysql.connector import Error

# =======================
# CONEXÃO COM BANCO MYSQL
# =======================
def conectar():
    """
    Tenta estabelecer uma conexão com o banco de dados MySQL.
    Retorna a conexão se bem-sucedida.
    Lança mysql.connector.Error se houver falha.
    """
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",      # altere conforme seu MySQL
            password="",      # troque pela sua senha real
            database="loja_db"
        )
        return conexao
    except Error as e:
        # Apenas levanta a exceção para ser tratada externamente
        raise e
    
# =======================
# FUNÇÃO EXECUTE SQL
# =======================
def execute_sql(query, params=()):
    """
    Executa uma consulta SQL no banco de dados MySQL.
    Retorna o resultado para SELECT ou None para outros comandos (INSERT, UPDATE, DELETE).
    """
    try:
        # Estabelece a conexão com o banco
        conexao = conectar()
        cursor = conexao.cursor()

        # Executa a consulta SQL com parâmetros
        cursor.execute(query, params)
        
        # Se a query for um comando SELECT, retornamos os resultados
        if query.strip().upper().startswith("SELECT"):
            resultado = cursor.fetchall()
            return resultado
        
        # Se for um comando INSERT, UPDATE ou DELETE, fazemos o commit
        conexao.commit()
        
        # Fechando o cursor e a conexão
        cursor.close()
        conexao.close()
        
    except Error as e:
        # Levanta uma exceção se houver erro na execução
        raise Exception(f"Erro ao executar SQL: {e}")