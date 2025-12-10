from data.conexao import conectar

# FUNÇÃO CADASTRAR USUÁRIO
def cadastrar_usuario(Nome, Login, Senha, ID_Perfil):
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")
        return False

    cursor = con.cursor()

    # Verifica login duplicado
    cursor.execute("SELECT * FROM Funcionarios WHERE Login=%s", (Login,))
    if cursor.fetchone():
        print(f"Login '{Login}' já existe!")
        return False

    comando = """
        INSERT INTO Funcionarios (Nome, Login, Senha, ID_Perfil)
        VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(comando, (Nome, Login, Senha, ID_Perfil))
        con.commit()
        print(f"Usuário '{Nome}' cadastrado com sucesso!")
        return True

    except Exception as e:
        print("Erro ao cadastrar:", e)
        return False

    finally:
        con.close()


# FUNÇÃO LISTAR USUÁRIOS
def listar_cadastros():
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")    
        return []
    
    try:
        cursor = con.cursor(dictionary=True)
        comando = """
            SELECT 
                f.ID_Funcionario AS id,
                f.Nome AS nome,
                f.Login AS login,
                p.Nome_Perfil AS perfil
            FROM Funcionarios f
            JOIN Perfis p ON f.ID_Perfil = p.ID_Perfil
            ORDER BY f.ID_Funcionario;
        """
        cursor.execute(comando)
        resultados = cursor.fetchall()
        return resultados
    
    except Exception as e:
        print("Erro ao listar usuários:", e)
        return []

    finally:
        con.close()

# FUNÇÃO EXCLUIR USUÁRIO
def excluir_usuario(id_funcionario):
    con = conectar()
    if con is None:
        print("Falha ao conectar ao banco")
        return False
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM Funcionarios WHERE ID_Funcionario = %s", (id_funcionario,))
        con.commit()
        print(f"Usuário com ID {id_funcionario} excluído com sucesso!")
        return True
    except Exception as e:
        print("Erro ao excluir usuário:", e)
        return False
    finally:
        con.close()

    