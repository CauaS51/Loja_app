from data.conexao import conectar
from data.criptografia import hash_senha


# =========================
# CADASTRAR CONTA
# =========================
def cadastrar_usuario(nome, login, senha, email, telefone, cpf):
    con = conectar()
    if con is None:
        print("Erro ao conectar ao banco.")
        return False

    cursor = con.cursor()

    try:
        # 🔎 LOGIN duplicado
        cursor.execute("SELECT 1 FROM Contas WHERE Login=%s", (login,))
        if cursor.fetchone():
            print("Login já existe.")
            return False

        # 🔎 CPF duplicado
        cursor.execute("SELECT 1 FROM Contas WHERE CPF=%s", (cpf,))
        if cursor.fetchone():
            print("CPF já cadastrado.")
            return False

        # 🔐 Hash da senha
        senha_hash = hash_senha(senha)

        cursor.execute("""
            INSERT INTO Contas
            (Nome, Login, Senha, Email, Telefone, CPF)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, login, senha_hash, email, telefone, cpf))

        con.commit()
        print("Conta cadastrada com sucesso!")
        return True

    except Exception as e:
        print("Erro ao cadastrar conta:", e)
        return False

    finally:
        con.close()


# =========================
# LISTAR CONTAS
# =========================
def listar_cadastros():
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")
        return []

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ID_Conta AS id,
                Nome AS nome,
                Login AS login,
                Email AS email,
                Telefone AS telefone,
                CPF AS cpf
            FROM Contas
            ORDER BY ID_Conta
        """)
        return cursor.fetchall()

    except Exception as e:
        print("Erro ao listar contas:", e)
        return []

    finally:
        con.close()


# =========================
# EXCLUIR CONTA
# =========================
def excluir_usuario(id_conta):
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")
        return False

    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Contas WHERE ID_Conta=%s", (id_conta,))
        con.commit()
        print("Conta excluída com sucesso!")
        return True

    except Exception as e:
        print("Erro ao excluir conta:", e)
        return False

    finally:
        con.close()

# =========================
# LISTAR FUNCIONÁRIOS
# =========================

def listar_funcionarios_da_loja(id_loja):
    con = conectar()
    if con is None: return []
    try:
        cursor = con.cursor(dictionary=True)
        query = """
            SELECT 
                c.Nome, 
                c.Login, 
                fl.ID_Funcionario, 
                p.Nome_Perfil
            FROM Funcionarios_Loja fl
            JOIN Contas c ON fl.ID_Conta = c.ID_Conta
            JOIN Perfis p ON fl.ID_Perfil = p.ID_Perfil
            WHERE fl.ID_Loja = %s
        """
        cursor.execute(query, (id_loja,))
        return cursor.fetchall()
    finally:
        con.close()

# =========================
# ATUALIZAR PERFIL DO FUNCIONÁRIO
# =========================
def atualizar_perfil_funcionario(id_funcionario, novo_perfil_nome):
    con = conectar()
    if con is None: return False
    try:
        cursor = con.cursor()
        # Primeiro, buscamos o ID do perfil pelo nome (Caixa, Repositor, etc)
        cursor.execute("SELECT ID_Perfil FROM Perfis WHERE Nome_Perfil = %s", (novo_perfil_nome,))
        res = cursor.fetchone()
        if not res: return False
        
        id_perfil = res[0]

        # Atualizamos o vínculo na tabela Funcionarios_Loja
        cursor.execute("""
            UPDATE Funcionarios_Loja 
            SET ID_Perfil = %s 
            WHERE ID_Funcionario = %s
        """, (id_perfil, id_funcionario))
        
        con.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")
        return False
    finally:
        con.close()

# =========================
# REMOVER FUNCIONÁRIO DA LOJA
# =========================
def remover_funcionario(id_funcionario):
    """
    Exclui o registro do funcionário da tabela Funcionarios_Loja.
    O usuário permanece cadastrado na tabela Contas.
    """
    con = conectar()
    if con is None: return False
    try:
        cursor = con.cursor()
        # ID_Funcionario é a PK da tabela Funcionarios_Loja no seu SQL
        cursor.execute("DELETE FROM Funcionarios_Loja WHERE ID_Funcionario = %s", (id_funcionario,))
        con.commit()
        return True
    except Exception as e:
        print(f"Erro ao excluir funcionário da loja: {e}")
        return False
    finally:
        con.close()