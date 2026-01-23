# === crud/crud_categorias.py ===
from data.conexao import conectar  # usa a função existente no seu projeto

# CADASTRAR CATEGORIA 
def cadastrar_categoria(nome, pai_id=None):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO Categorias (Nome, Pai_ID) VALUES (%s, %s)"
    cursor.execute(sql, (nome, pai_id))
    conn.commit()
    cursor.close()
    conn.close()

# LISTAR CATEGORIA
def listar_categorias():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT ID_Categoria, Nome FROM Categorias WHERE Pai_ID IS NULL ORDER BY Nome"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row["Nome"] for row in resultado]


def listar_categorias_hierarquia():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT ID_Categoria, Nome, Pai_ID FROM Categorias ORDER BY Nome"
    cursor.execute(sql)
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
        """
        cursor.execute(sql, (pai_nome, sub_nome))
    else:
        sql = "SELECT ID_Categoria FROM Categorias WHERE Nome = %s AND Pai_ID IS NULL"
        cursor.execute(sql, (nome,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result["ID_Categoria"]
    return None

# ATUALIZAR CATEGORIA



# EXCLUIR CATEGORIA
def excluir_categoria(id_categoria):
    conn = conectar()
    cursor = conn.cursor()
    sql = "DELETE FROM Categorias WHERE ID_Categoria = %s"
    cursor.execute(sql, (id_categoria,))
    conn.commit()
    cursor.close()
    conn.close()
