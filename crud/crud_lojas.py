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

        # 1️⃣ Verifica se a loja existe
        cursor.execute("SELECT ID_Loja, Nome_Loja FROM Lojas WHERE ID_Loja = %s", (id_loja,))
        loja = cursor.fetchone()

        if not loja:
            return None  # Loja não existe

        # 2️⃣ Verifica se usuário já pertence à loja
        cursor.execute("""
            SELECT 
                Funcionarios_Loja.ID_Funcionario AS id_funcionario,
                Perfis.Nome_Perfil AS perfil
            FROM Funcionarios_Loja
            JOIN Perfis ON Perfis.ID_Perfil = Funcionarios_Loja.ID_Perfil
            WHERE Funcionarios_Loja.ID_Loja = %s
              AND Funcionarios_Loja.ID_Conta = %s
        """, (id_loja, id_conta))

        vinculo = cursor.fetchone()

        # 3️⃣ Se NÃO estiver vinculado, adiciona como CAIXA automaticamente
        if not vinculo:
            cursor.execute("SELECT ID_Perfil FROM Perfis WHERE Nome_Perfil='Caixa'")
            perfil = cursor.fetchone()

            cursor.execute("""
                INSERT INTO Funcionarios_Loja (ID_Conta, ID_Loja, ID_Perfil)
                VALUES (%s, %s, %s)
            """, (id_conta, id_loja, perfil["ID_Perfil"]))
            con.commit()

            id_funcionario = cursor.lastrowid
            nome_perfil = "Caixa"
        else:
            id_funcionario = vinculo["id_funcionario"]
            nome_perfil = vinculo["perfil"]

        # 4️⃣ Retorna dados para a sessão
        return {
            "id": loja["ID_Loja"],
            "nome": loja["Nome_Loja"],
            "id_funcionario": id_funcionario,
            "perfil": nome_perfil
        }

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
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao associar usuário à loja:", e)
        return False
    finally:
        con.close()


# ==========================
# SALVAR TEMA DA LOJA
# ==========================
def salvar_tema_loja(loja_id, tema):
    con = conectar()
    if con is None:
        return False

    try:
        cursor = con.cursor()
        tema_json = json.dumps(tema, ensure_ascii=False)
        cursor.execute("""
            INSERT INTO Temas_Lojas (ID_Loja, Tema_JSON)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE Tema_JSON = VALUES(Tema_JSON)
        """, (loja_id, tema_json))
        con.commit()
        return True
    except Exception as e:
        print("Erro ao salvar tema da loja:", e)
        return False
    finally:
        con.close()


# ==========================
# BUSCAR DADOS VISUAIS DA LOJA
# ==========================
def buscar_dados_visuais(loja_id):
    """
    Retorna os dados visuais de uma loja pelo ID,
    incluindo Tema_JSON, logo, id_funcionario e perfil.
    """
    con = conectar()
    if con is None:
        return None

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                Lojas.ID_Loja AS id,
                Lojas.Img AS img,
                Funcionarios_Loja.ID_Funcionario AS id_funcionario,
                Perfis.Nome_Perfil AS perfil,
                Temas_Lojas.Tema_JSON AS Tema_JSON
            FROM Lojas
            LEFT JOIN Funcionarios_Loja ON Funcionarios_Loja.ID_Loja = Lojas.ID_Loja
            LEFT JOIN Perfis ON Perfis.ID_Perfil = Funcionarios_Loja.ID_Perfil
            LEFT JOIN Temas_Lojas ON Temas_Lojas.ID_Loja = Lojas.ID_Loja
            WHERE Lojas.ID_Loja = %s
        """, (loja_id,))
        return cursor.fetchone()
    except Exception as e:
        print("Erro ao buscar dados visuais:", e)
        return None
    finally:
        con.close()
