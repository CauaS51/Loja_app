from data.conexao import conectar
import json


# ==========================
# CRIAR LOJA
# ==========================
def criar_loja(nome):
    con = conectar()
    if con is None:
        return None
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO Lojas (Nome_Loja) VALUES (%s)",
            (nome,)
        )
        con.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao criar loja:", e)
        return None
    finally:
        con.close()


# ==========================
# LISTAR TODAS AS LOJAS
# ==========================
def listar_lojas():
    con = conectar()
    if con is None:
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ID_Loja AS id,
                Nome_Loja AS nome,
                Img AS img
            FROM Lojas
            ORDER BY Nome_Loja
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar lojas:", e)
        return []
    finally:
        con.close()


# ==========================
# ATUALIZAR LOJA
# ==========================
def atualizar_loja(id_loja, nome=None, img=None):
    if not nome and not img:
        return False

    con = conectar()
    if con is None:
        return False

    try:
        cursor = con.cursor()
        campos = []
        valores = []

        if nome:
            campos.append("Nome_Loja = %s")
            valores.append(nome)

        if img:
            campos.append("Img = %s")
            valores.append(img)

        valores.append(id_loja)

        sql = f"UPDATE Lojas SET {', '.join(campos)} WHERE ID_Loja = %s"
        cursor.execute(sql, tuple(valores))
        con.commit()
        return True
    except Exception as e:
        print("Erro ao atualizar loja:", e)
        return False
    finally:
        con.close()


# ==========================
# EXCLUIR LOJA
# ==========================
def excluir_loja(id_loja):
    con = conectar()
    if con is None:
        return False
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Lojas WHERE ID_Loja = %s", (id_loja,))
        con.commit()
        return True
    except Exception as e:
        print("Erro ao excluir loja:", e)
        return False
    finally:
        con.close()

# ==========================
# LISTAR LOJAS DO FUNCIONÁRIO
# ==========================
def listar_lojas_usuario(id_conta):
    con = conectar()
    if con is None:
        return []

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                Lojas.ID_Loja AS id,
                Lojas.Nome_Loja AS nome,
                Lojas.Img AS img,
                Perfis.Nome_Perfil AS perfil,
                Funcionarios_Loja.ID_Funcionario AS id_funcionario
            FROM Funcionarios_Loja
            JOIN Lojas ON Lojas.ID_Loja = Funcionarios_Loja.ID_Loja
            JOIN Perfis ON Perfis.ID_Perfil = Funcionarios_Loja.ID_Perfil
            WHERE Funcionarios_Loja.ID_Conta = %s
            ORDER BY Lojas.Nome_Loja
        """, (id_conta,))

        return cursor.fetchall()

    except Exception as e:
        print("Erro ao listar lojas do usuário:", e)
        return []

    finally:
        con.close()




# ==========================
# ENTRAR EM UMA LOJA (VALIDADO)
# ==========================
def entrar_em_loja(id_loja, id_conta):
    con = conectar()
    if con is None:
        return None

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                Lojas.ID_Loja AS id,
                Lojas.Nome_Loja AS nome,
                Perfis.Nome_Perfil AS perfil,
                Funcionarios_Loja.ID_Funcionario AS id_funcionario
            FROM Funcionarios_Loja
            JOIN Lojas ON Lojas.ID_Loja = Funcionarios_Loja.ID_Loja
            JOIN Perfis ON Perfis.ID_Perfil = Funcionarios_Loja.ID_Perfil
            WHERE Funcionarios_Loja.ID_Loja = %s
              AND Funcionarios_Loja.ID_Conta = %s
        """, (id_loja, id_conta))

        return cursor.fetchone()

    except Exception as e:
        print("Erro ao entrar na loja:", e)
        return None

    finally:
        con.close()





# ==========================
# ASSOCIAR USUÁRIO À LOJA
# ==========================
def associar_usuario_a_loja(id_conta, id_loja, perfil="Administrador"):
    con = conectar()
    if con is None:
        return False

    try:
        cursor = con.cursor(dictionary=True)

        cursor.execute(
            "SELECT ID_Perfil FROM Perfis WHERE Nome_Perfil = %s",
            (perfil,)
        )
        perfil_row = cursor.fetchone()

        if not perfil_row:
            print(f"Perfil '{perfil}' não encontrado.")
            return False

        id_perfil = perfil_row["ID_Perfil"]

        cursor.execute("""
            INSERT INTO Funcionarios_Loja (ID_Conta, ID_Loja, ID_Perfil)
            VALUES (%s, %s, %s)
        """, (id_conta, id_loja, id_perfil))

        con.commit()
        return cursor.lastrowid  # ID_Funcionario

    except Exception as e:
        print("Erro ao associar usuário à loja:", e)
        return False

    finally:
        con.close()














# ==========================
# SALVAR TEMA DA LOJA
# ========================== 
def salvar_tema_loja(loja_id, tema):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Converte o dicionário do tema para JSON
        tema_json = json.dumps(tema)

        # UPDATE correto para MySQL
        cursor.execute("""
            UPDATE Lojas
            SET Tema = %s
            WHERE ID_Loja = %s
        """, (tema_json, loja_id))

        conn.commit()
    except Exception as e:
        print("Erro ao salvar tema da loja:", e)
        return False
    finally:
        conn.close()
    return True



