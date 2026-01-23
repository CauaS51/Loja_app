from data.conexao import conectar
from crud.crud_categorias import buscar_id_por_nome

# CADASTRAR PRODUTO
def cadastrar_produto(nome, preco, img, categoria_nome):
    con = conectar()
    if con is None:
        return None

    categoria_id = buscar_id_por_nome(categoria_nome)

    cursor = con.cursor()
    try:
        cursor.execute(
            "INSERT INTO Produtos (Nome, Preco, Categoria_ID, Img) VALUES (%s, %s, %s, %s)",
            (nome, preco, categoria_id, img)
        )
        con.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao cadastrar produto:", e)
        return None
    finally:
        con.close()


# LISTAR PRODUTOS
def listar_produtos(filtro_categoria_id=None, pesquisa=None):
    con = conectar()
    if con is None:
        return []
    cursor = con.cursor(dictionary=True)
    try:
        comando = """
            SELECT p.ID_Produto AS codigo, p.Nome AS nome, p.Preco AS preco, p.Img AS img,
                   c.Nome AS categoria, c.Pai_ID AS categoria_pai
            FROM Produtos p
            LEFT JOIN Categorias c ON p.Categoria_ID = c.ID_Categoria
        """
        filtros = []
        valores = []

        if filtro_categoria_id:
            filtros.append("p.Categoria_ID=%s")
            valores.append(filtro_categoria_id)
        if pesquisa:
            filtros.append("p.Nome LIKE %s")
            valores.append(f"%{pesquisa}%")

        if filtros:
            comando += " WHERE " + " AND ".join(filtros)

        comando += " ORDER BY p.ID_Produto"
        cursor.execute(comando, tuple(valores))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar produtos:", e)
        return []
    finally:
        con.close()


# ATUALIZAR PRODUTOS
def atualizar_produto(codigo, nome, preco, img, categoria_nome):
    con = conectar()
    if con is None:
        return False

    categoria_id = buscar_id_por_nome(categoria_nome)
    cursor = con.cursor()
    try:
        cursor.execute(
            "UPDATE Produtos SET Nome=%s, Preco=%s, Categoria_ID=%s, Img=%s WHERE ID_Produto=%s",
            (nome, preco, categoria_id, img, codigo)
        )
        con.commit()
        return True
    except Exception as e:
        print("Erro ao atualizar produto:", e)
        return False
    finally:
        con.close()


# EXCLUIR PRODUTO
def excluir_produto(id_produto):
    con = conectar()
    if con is None:
        return False
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM Produtos WHERE ID_Produto=%s", (id_produto,))
        con.commit()
        return True
    except Exception as e:
        print("Erro ao excluir produto:", e)
        return False
    finally:
        con.close()
