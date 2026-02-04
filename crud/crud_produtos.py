from data.conexao import conectar
from crud.crud_categorias import buscar_id_por_nome
import data.sessao as sessao

# ==========================
# CADASTRAR PRODUTO
# ==========================
def cadastrar_produto(nome, preco, estoque, codigo_barras="", img=None, categoria_nome="Sem Categoria", custo=0.0, estoque_minimo=0, unidade=""):
    """
    Insere um novo produto vinculado à loja da sessão.
    O parâmetro 'img' agora deve receber os BYTES da imagem.
    """
    if sessao.loja_id is None: return None
    con = conectar()
    categoria_id = buscar_id_por_nome(categoria_nome)
    cursor = con.cursor()
    try:
        # Alterado de 'Img' para 'Foto_Binaria' conforme seu novo banco
        cursor.execute("""
            INSERT INTO Produtos (ID_Loja, Nome, Preco, Custo, Estoque, Estoque_Minimo, Unidade, Codigo_Barras, Categoria_ID, Foto_Binaria)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (sessao.loja_id, nome, preco, custo, estoque, estoque_minimo, unidade, codigo_barras, categoria_id, img))
        con.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao cadastrar produto:", e)
        return None
    finally:
        con.close()

# ==========================================================
# LISTAR PRODUTOS (Compatível com 'listar_produtos_por_loja')
# ==========================================================
def listar_produtos(apenas_ativos=False):
    """
    Lista produtos da loja da sessão. 
    Retorna a coluna Foto_Binaria como 'img'.
    """
    if sessao.loja_id is None: return []
    con = conectar()
    cursor = con.cursor(dictionary=True)
    
    filtro_ativo = "AND p.Ativo = TRUE" if apenas_ativos else ""
    
    try:
        cursor.execute(f"""
            SELECT 
                p.ID_Produto AS codigo, p.Nome AS nome, p.Preco AS preco,
                p.Custo AS custo, p.Estoque AS estoque, p.Estoque_Minimo AS estoque_minimo,
                p.Unidade AS unidade, p.Codigo_Barras AS codigo_barras,
                p.Foto_Binaria AS img, p.Ativo AS ativo, c.Nome AS categoria
            FROM Produtos p
            LEFT JOIN Categorias c ON p.Categoria_ID = c.ID_Categoria
            WHERE p.ID_Loja = %s {filtro_ativo}
            ORDER BY p.Nome
        """, (sessao.loja_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar produtos:", e)
        return []
    finally:
        con.close()

# Apelido para evitar o erro de AttributeError na sua interface
listar_produtos_por_loja = lambda id_loja: listar_produtos(apenas_ativos=True)

# ==========================
# ATUALIZAR PRODUTO
# ==========================
def atualizar_produto(codigo, nome, preco, estoque, codigo_barras="", img=None, categoria_nome="Sem Categoria", custo=0.0, estoque_minimo=0, unidade="", ativo=True):
    """Atualiza todos os dados de um produto específico usando bytes para imagem."""
    if sessao.loja_id is None: return False
    con = conectar()
    categoria_id = buscar_id_por_nome(categoria_nome)
    cursor = con.cursor()
    try:
        cursor.execute("""
            UPDATE Produtos SET Nome=%s, Preco=%s, Custo=%s, Estoque=%s, Estoque_Minimo=%s, 
            Unidade=%s, Codigo_Barras=%s, Categoria_ID=%s, Foto_Binaria=%s, Ativo=%s
            WHERE ID_Produto=%s AND ID_Loja=%s
        """, (nome, preco, custo, estoque, estoque_minimo, unidade, codigo_barras, categoria_id, img, ativo, codigo, sessao.loja_id))
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
    """Remove o produto do banco de dados filtrando pela loja."""
    if sessao.loja_id is None: return False
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

# =====================================================
# BAIXAR ESTOQUE (Compatível com 'atualizar_estoque')
# =====================================================
def baixar_estoque(id_produto, quantidade):
    """Subtrai a quantidade vendida do estoque atual."""
    if sessao.loja_id is None: return False
    con = conectar()
    cursor = con.cursor()
    try:
        cursor.execute("""
            UPDATE Produtos 
            SET Estoque = Estoque - %s 
            WHERE ID_Produto = %s AND ID_Loja = %s
        """, (quantidade, id_produto, sessao.loja_id))
        con.commit()
        return True
    except Exception as e:
        print("Erro ao baixar estoque:", e)
        return False
    finally:
        con.close()

# Apelido para suportar a chamada de atualização negativa da interface
def atualizar_estoque(id_p, qtd): return baixar_estoque(id_p, -qtd)

# ==========================
# BUSCAR POR CODIGO BARRAS
# ==========================
def buscar_por_codigo_barras(codigo):
    """Busca um produto ativo para o PDV via leitor."""
    if sessao.loja_id is None: return None
    con = conectar()
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                ID_Produto AS codigo, Nome AS nome, Preco AS preco, 
                Estoque AS estoque, Foto_Binaria AS img, Codigo_Barras AS codigo_barras
            FROM Produtos 
            WHERE Codigo_Barras = %s AND ID_Loja = %s AND Ativo = TRUE
        """, (codigo, sessao.loja_id))
        return cursor.fetchone()
    finally:
        con.close()