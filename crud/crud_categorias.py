from data.conexao import conectar
import data.sessao as sessao


# ==========================
# CADASTRAR CATEGORIA
# ==========================
def cadastrar_categoria(nome, pai_id=None):
    conn = conectar()
    if conn is None:
        return False

    loja_id = sessao.loja_id
    cursor = conn.cursor()

    try:
        sql = """
            INSERT INTO Categorias (ID_Loja, Nome, Pai_ID)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (loja_id, nome, pai_id))
        conn.commit()
        return True
    except Exception as e:
        print("Erro ao cadastrar categoria:", e)
        return False
    finally:
        conn.close()


# ==========================
# LISTAR CATEGORIAS PRINCIPAIS DA LOJA
# ==========================
def listar_categorias():
    conn = conectar()
    if conn is None:
        return []

    loja_id = sessao.loja_id
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
            SELECT ID_Categoria, Nome
            FROM Categorias
            WHERE Pai_ID IS NULL AND ID_Loja = %s
            ORDER BY Nome
        """
        cursor.execute(sql, (loja_id,))
        resultado = cursor.fetchall()
        return [row["Nome"] for row in resultado]
    finally:
        conn.close()


# ==========================
# LISTAR CATEGORIAS COM HIERARQUIA
# ==========================
def listar_categorias_hierarquia():
    conn = conectar()
    if conn is None:
        return []

    loja_id = sessao.loja_id
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
            SELECT ID_Categoria, Nome, Pai_ID
            FROM Categorias
            WHERE ID_Loja = %s
            ORDER BY Nome
        """
        cursor.execute(sql, (loja_id,))
        rows = cursor.fetchall()

        id_to_nome = {row["ID_Categoria"]: row["Nome"] for row in rows}
        hierarquia = []

        for row in rows:
            if row["Pai_ID"] is None:
                hierarquia.append(row["Nome"])
            else:
                pai_nome = id_to_nome.get(row["Pai_ID"], "Sem Categoria")
                hierarquia.append(f"{pai_nome} > {row['Nome']}")

        return hierarquia

    finally:
        conn.close()


# ==========================
# BUSCAR ID POR NOME (RESPEITANDO A LOJA)
# ==========================
def buscar_id_por_nome(nome):
    conn = conectar()
    if conn is None:
        return None

    loja_id = sessao.loja_id
    cursor = conn.cursor(dictionary=True)

    try:
        if " > " in nome:
            pai_nome, sub_nome = nome.split(" > ")
            sql = """
                SELECT c2.ID_Categoria
                FROM Categorias c1
                JOIN Categorias c2 ON c2.Pai_ID = c1.ID_Categoria
                WHERE c1.Nome = %s
                AND c2.Nome = %s
                AND c1.ID_Loja = %s
                AND c2.ID_Loja = %s
            """
            cursor.execute(sql, (pai_nome, sub_nome, loja_id, loja_id))
        else:
            sql = """
                SELECT ID_Categoria
                FROM Categorias
                WHERE Nome = %s
                AND Pai_ID IS NULL
                AND ID_Loja = %s
            """
            cursor.execute(sql, (nome, loja_id))

        result = cursor.fetchone()
        return result["ID_Categoria"] if result else None

    finally:
        conn.close()


# ==========================
# EXCLUIR CATEGORIA DA LOJA
# ==========================
def excluir_categoria(id_categoria):
    conn = conectar()
    if conn is None:
        return False

    loja_id = sessao.loja_id
    cursor = conn.cursor()

    try:
        sql = "DELETE FROM Categorias WHERE ID_Categoria = %s AND ID_Loja = %s"
        cursor.execute(sql, (id_categoria, loja_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao excluir categoria:", e)
        return False
    finally:
        conn.close()
