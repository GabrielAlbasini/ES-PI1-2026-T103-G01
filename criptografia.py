from cryptography.fernet import Fernet
import os
import bcrypt

def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as f:
        f.write(chave)

def carregar_chave():
    if not os.path.exists("chave.key"):
        gerar_chave()
    with open("chave.key", "rb") as f:
        return f.read()

def criptografar(texto):
    chave = carregar_chave()
    fernet = Fernet(chave)
    return fernet.encrypt(texto.encode())

def descriptografar(dado):
    chave = carregar_chave()
    fernet = Fernet(chave)
    return fernet.decrypt(dado).decode()

def gerar_hash(texto):
    return bcrypt.hashpw(texto.encode(), bcrypt.gensalt())

def verificar_hash(texto, hash_guardado):
    return bcrypt.checkpw(texto.encode(), hash_guardado)