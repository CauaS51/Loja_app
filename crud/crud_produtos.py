from data.conexao import conectar
from crud.crud_categorias import buscar_id_por_nome
import data.sessao as sessao

# ==========================
# CADASTRAR PRODUTO
# ==========================
def cadastrar_produto(nome, preco, img, categoria_nome):
    if sessao.loja_id is None:
        print("Sessão sem loja.")
        return None

    con = conectar()
    categoria_id = buscar_id_por_nome(categoria_nome)
    cursor = con.cursor()

    try:
        cursor.execute("""
            INSERT INTO Produtos (ID_Loja, Nome, Preco, Categoria_ID, Img)
            VALUES (%s, %s, %s, %s, %s)
        """, (sessao.loja_id, nome, preco, categoria_id, img))
        con.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao cadastrar produto:", e)
        return None
    finally:
        con.close()


# ==========================
# LISTAR PRODUTOS DA LOJA
# ==========================
def listar_produtos():
    if sessao.loja_id is None:
        return []

    con = conectar()
    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT p.ID_Produto AS codigo,
                   p.Nome AS nome,
                   p.Preco AS preco,
                   p.Img AS img,
                   c.Nome AS categoria
            FROM Produtos p
            LEFT JOIN Categorias c ON p.Categoria_ID = c.ID_Categoria
            WHERE p.ID_Loja = %s
            ORDER BY p.ID_Produto
        """, (sessao.loja_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar produtos:", e)
        return []
    finally:
        con.close()


# ==========================
# ATUALIZAR PRODUTO
# ==========================
def atualizar_produto(codigo, nome, preco, img, categoria_nome):
    if sessao.loja_id is None:
        return False

    con = conectar()
    categoria_id = buscar_id_por_nome(categoria_nome)
    cursor = con.cursor()

    try:
        cursor.execute("""
            UPDATE Produtos
            SET Nome=%s, Preco=%s, Categoria_ID=%s, Img=%s
            WHERE ID_Produto=%s AND ID_Loja=%s
        """, (nome, preco, categoria_id, img, codigo, sessao.loja_id))
        con.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao atualizar produto:", e)
        return False
    finally:
        con.close()


# ==========================
# EXCLUIR PRODUTO
# ==========================
def excluir_produto(id_produto):
    if sessao.loja_id is None:
        return False

    con = conectar()
    cursor = con.cursor()

    try:
        cursor.execute(
            "DELETE FROM Produtos WHERE ID_Produto=%s AND ID_Loja=%s",
            (id_produto, sessao.loja_id)
        )
        con.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao excluir produto:", e)
        return False
    finally:
        con.close()
