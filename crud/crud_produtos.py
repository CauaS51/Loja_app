from data.conexao import conectar

# ===================== CADASTRAR PRODUTO =====================
def cadastrar_produto(nome, preco, img):
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")
        return False

    cursor = con.cursor()
    cursor.execute("SELECT * FROM Produtos WHERE Nome=%s", (nome,))
    if cursor.fetchone():
        print(f"Produto '{nome}' já existe!")
        return False

    comando = "INSERT INTO Produtos (Nome, Preco, Img) VALUES (%s, %s, %s)"
    try:
        cursor.execute(comando, (nome, preco, img))
        con.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao cadastrar produto:", e)
        return None
    finally:
        con.close()


# ===================== LISTAR PRODUTOS =====================
def listar_produtos():
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")
        return []
    
    try:
        cursor = con.cursor(dictionary=True)
        comando = """
            SELECT 
                ID_Produto AS codigo, 
                Nome AS nome, 
                Preco AS preco, 
                Categoria AS categoria,
                Img AS img
            FROM Produtos
            ORDER BY ID_Produto
        """
        cursor.execute(comando)
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar produtos:", e)
        return []
    finally:
        con.close()

# ===================== EXCLUIR PRODUTO =====================
def excluir_produto(id_produto):
    """
    Exclui um produto pelo seu ID
    """
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")
        return False

    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM Produtos WHERE ID_Produto = %s", (id_produto,))
        con.commit()
        print(f"Produto com ID {id_produto} excluído com sucesso!")
        return True
    except Exception as e:
        print("Erro ao excluir produto:", e)
        return False
    finally:
        con.close()


# ===================== ATUALIZAR PRODUTO =====================
def atualizar_produto(id_produto, nome=None, preco=None, img=None):
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")
        return False

    cursor = con.cursor()
    try:
        campos = []
        valores = []

        if nome is not None:
            campos.append("Nome=%s")
            valores.append(nome)
        if preco is not None:
            campos.append("Preco=%s")
            valores.append(preco)
        if img is not None:
            campos.append("Img=%s")
            valores.append(img)

        if not campos:
            print("Nenhum campo para atualizar")
            return False

        valores.append(id_produto)
        comando = f"UPDATE Produtos SET {', '.join(campos)} WHERE ID_Produto=%s"
        cursor.execute(comando, valores)
        con.commit()
        print(f"Produto com ID {id_produto} atualizado com sucesso!")
        return True
    except Exception as e:
        print("Erro ao atualizar produto:", e)
        return False
    finally:
        con.close()
