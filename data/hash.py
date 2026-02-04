import bcrypt

def hash_senha(senha: str) -> str:
    """Gera hash seguro da senha"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
    """Verifica senha digitada contra hash"""
    return bcrypt.checkpw(
        senha_digitada.encode("utf-8"),
        senha_hash.encode("utf-8")
    )
