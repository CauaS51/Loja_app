from data.conexao import conectar
from crud.crud_categorias import buscar_id_por_nome
import data.sessao as sessao

# ==========================
# CADASTRAR PRODUTO
# ==========================
def cadastrar_produto(
    nome,
    preco,
    estoque,
    codigo_barras="",
    img="",
    categoria_nome="Sem Categoria",
    custo=0.0,
    estoque_minimo=0,
    unidade=""
):
    """
    Cadastra um novo produto na loja.
    Alguns campos têm valor padrão: custo, estoque_minimo, unidade.
    """
    if sessao.loja_id is None:
        print("Sessão sem loja.")
        return None

    con = conectar()
    categoria_id = buscar_id_por_nome(categoria_nome)
    cursor = con.cursor()

    try:
        cursor.execute("""
            INSERT INTO Produtos (
                ID_Loja, Nome, Preco, Custo,
                Estoque, Estoque_Minimo,
                Unidade, Codigo_Barras,
                Categoria_ID, Img
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            sessao.loja_id,
            nome,
            preco,
            custo,
            estoque,
            estoque_minimo,
            unidade,
            codigo_barras,
            categoria_id,
            img
        ))
        con.commit()
        return cursor.lastrowid

    except Exception as e:
        print("Erro ao cadastrar produto:", e)
        return None
    finally:
        con.close()


# ==========================
# LISTAR PRODUTOS
# ==========================
def listar_produtos():
    if sessao.loja_id is None:
        return []

    con = conectar()
    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                p.ID_Produto AS codigo,
                p.Nome AS nome,
                p.Preco AS preco,
                p.Custo AS custo,
                p.Estoque AS estoque,
                p.Estoque_Minimo AS estoque_minimo,
                p.Unidade AS unidade,
                p.Codigo_Barras AS codigo_barras,
                p.Img AS img,
                p.Ativo AS ativo,
                c.Nome AS categoria
            FROM Produtos p
            LEFT JOIN Categorias c ON p.Categoria_ID = c.ID_Categoria
            WHERE p.ID_Loja = %s
            ORDER BY p.Nome
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
def atualizar_produto(
    codigo,
    nome,
    preco,
    estoque,
    codigo_barras="",
    img="",
    categoria_nome="Sem Categoria",
    custo=0.0,
    estoque_minimo=0,
    unidade="",
    ativo=True
):
    """
    Atualiza um produto existente.
    """
    if sessao.loja_id is None:
        return False

    con = conectar()
    categoria_id = buscar_id_por_nome(categoria_nome)
    cursor = con.cursor()

    try:
        cursor.execute("""
            UPDATE Produtos SET
                Nome=%s,
                Preco=%s,
                Custo=%s,
                Estoque=%s,
                Estoque_Minimo=%s,
                Unidade=%s,
                Codigo_Barras=%s,
                Categoria_ID=%s,
                Img=%s,
                Ativo=%s
            WHERE ID_Produto=%s AND ID_Loja=%s
        """, (
            nome,
            preco,
            custo,
            estoque,
            estoque_minimo,
            unidade,
            codigo_barras,
            categoria_id,
            img,
            ativo,
            codigo,
            sessao.loja_id
        ))
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


# ==========================
# BAIXAR ESTOQUE (VENDA)
# ==========================
def baixar_estoque(id_produto, quantidade):
    con = conectar()
    cursor = con.cursor()

    try:
        cursor.execute("""
            UPDATE Produtos
            SET Estoque = Estoque - %s
            WHERE ID_Produto=%s AND ID_Loja=%s
        """, (quantidade, id_produto, sessao.loja_id))
        con.commit()
    except Exception as e:
        print("Erro ao baixar estoque:", e)
    finally:
        con.close()


# ==========================
# ADICIONAR ESTOQUE (COMPRA)
# ==========================
def adicionar_estoque(id_produto, quantidade):
    con = conectar()
    cursor = con.cursor()

    try:
        cursor.execute("""
            UPDATE Produtos
            SET Estoque = Estoque + %s
            WHERE ID_Produto=%s AND ID_Loja=%s
        """, (quantidade, id_produto, sessao.loja_id))
        con.commit()
    except Exception as e:
        print("Erro ao adicionar estoque:", e)
    finally:
        con.close()


# ==========================
# BUSCAR POR CÓDIGO DE BARRAS
# ==========================
def buscar_por_codigo_barras(codigo):
    con = conectar()
    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM Produtos
            WHERE Codigo_Barras=%s AND ID_Loja=%s
        """, (codigo, sessao.loja_id))
        return cursor.fetchone()
    except Exception as e:
        print("Erro ao buscar produto:", e)
        return None
    finally:
        con.close()


# ==========================
# ESTOQUE BAIXO
# ==========================
def listar_estoque_baixo():
    con = conectar()
    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT Nome, Estoque, Estoque_Minimo
            FROM Produtos
            WHERE ID_Loja=%s
            AND Estoque <= Estoque_Minimo
            AND Ativo = TRUE
        """, (sessao.loja_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao verificar estoque baixo:", e)
        return []
    finally:
        con.close()
