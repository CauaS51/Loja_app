from data.conexao import conectar
import data.sessao as sessao

# ==========================
# CADASTRAR CATEGORIA
# ==========================
def cadastrar_categoria(nome, pai_id=None):
    conn = conectar()
    cursor = conn.cursor()
    sql = """
        INSERT INTO Categorias (ID_Loja, Nome, Pai_ID)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (sessao.loja_id, nome, pai_id))
    conn.commit()
    cursor.close()
    conn.close()


# ==========================
# LISTAR CATEGORIAS (RAIZ)
# ==========================
def listar_categorias():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT ID_Categoria, Nome
        FROM Categorias
        WHERE ID_Loja = %s AND Pai_ID IS NULL
        ORDER BY Nome
    """
    cursor.execute(sql, (sessao.loja_id,))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row["Nome"] for row in resultado]


# ==========================
# LISTAR HIERARQUIA
# ==========================
def listar_categorias_hierarquia():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT ID_Categoria, Nome, Pai_ID
        FROM Categorias
        WHERE ID_Loja = %s
        ORDER BY Nome
    """
    cursor.execute(sql, (sessao.loja_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    id_to_nome = {row["ID_Categoria"]: row["Nome"] for row in rows}
    hierarquia = []
    for row in rows:
        if row["Pai_ID"] is None:
            hierarquia.append(row["Nome"])
        else:
            pai_nome = id_to_nome.get(row["Pai_ID"], "Sem Categoria")
            hierarquia.append(f"{pai_nome} > {row['Nome']}")
    return hierarquia


# ==========================
# BUSCAR ID POR NOME
# ==========================
def buscar_id_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    if " > " in nome:
        pai_nome, sub_nome = nome.split(" > ")
        sql = """
            SELECT c2.ID_Categoria
            FROM Categorias c1
            JOIN Categorias c2 ON c2.Pai_ID = c1.ID_Categoria
            WHERE c1.Nome = %s AND c2.Nome = %s
              AND c1.ID_Loja = %s
        """
        cursor.execute(sql, (pai_nome, sub_nome, sessao.loja_id))
    else:
        sql = """
            SELECT ID_Categoria
            FROM Categorias
            WHERE Nome = %s AND Pai_ID IS NULL AND ID_Loja = %s
        """
        cursor.execute(sql, (nome, sessao.loja_id))

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result["ID_Categoria"]
    return None


# ==========================
# EXCLUIR CATEGORIA
# ==========================
def excluir_categoria(id_categoria):
    conn = conectar()
    cursor = conn.cursor()
    sql = """
        DELETE FROM Categorias
        WHERE ID_Categoria = %s AND ID_Loja = %s
    """
    cursor.execute(sql, (id_categoria, sessao.loja_id))
    conn.commit()
    cursor.close()
    conn.close()
