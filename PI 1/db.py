import mysql.connector
from criptografia import criptografar_hill, descriptografar_hill

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_votacao"
    )
    cursor = conn.cursor(dictionary=True)
except mysql.connector.Error as erro:
    print("Erro ao conectar no banco:", erro)


# ========================
# ELEITOR
# ========================

def inserir_eleitor(nome, cpf, titulo, mesario, chave):
    try:
        cursor.execute("""
            INSERT INTO eleitor 
            (nome_completo, cpf, titulo_eleitor, mesario, chave_acesso)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, criptografar_hill(cpf), titulo, mesario, criptografar_hill(chave)))
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao inserir eleitor:", erro)
        conn.rollback()
        return False


def buscar_por_titulo(titulo):
    cursor.execute("SELECT * FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
    eleitor = cursor.fetchone()
    if eleitor:
        eleitor["cpf"] = descriptografar_hill(eleitor["cpf"])
        eleitor["chave_acesso"] = descriptografar_hill(eleitor["chave_acesso"])
    return eleitor


def buscar_por_cpf_ou_titulo(cpf, titulo):
    cursor.execute("""
        SELECT * FROM eleitor WHERE cpf = %s OR titulo_eleitor = %s
    """, (criptografar_hill(cpf), titulo))
    eleitor = cursor.fetchone()
    if eleitor:
        eleitor["cpf"] = descriptografar_hill(eleitor["cpf"])
        eleitor["chave_acesso"] = descriptografar_hill(eleitor["chave_acesso"])
    return eleitor


def listar_todos():
    cursor.execute("SELECT * FROM eleitor")
    eleitores = cursor.fetchall()
    for eleitor in eleitores:
        eleitor["cpf"] = descriptografar_hill(eleitor["cpf"])
        eleitor["chave_acesso"] = descriptografar_hill(eleitor["chave_acesso"])
    return eleitores


def atualizar_eleitor(nome, cpf, mesario, titulo):
    try:
        cursor.execute("""
            UPDATE eleitor SET nome_completo = %s, cpf = %s, mesario = %s
            WHERE titulo_eleitor = %s
        """, (nome, criptografar_hill(cpf), mesario, titulo))
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao atualizar eleitor:", erro)
        conn.rollback()
        return False


def remover_por_titulo(titulo):
    try:
        cursor.execute("DELETE FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao remover eleitor:", erro)
        conn.rollback()
        return False


# ========================
# VOTAÇÃO
# ========================

def listar_candidatos():
    cursor.execute("SELECT id, numero, nome, partido FROM candidato ORDER BY numero")
    return cursor.fetchall()


def buscar_candidato(numero):
    cursor.execute("SELECT id, nome, partido FROM candidato WHERE numero = %s", (numero,))
    return cursor.fetchone()


def inserir_voto(id_candidato, data_hora, protocolo):
    try:
        cursor.execute("""
            INSERT INTO voto (id_candidato, data_hora, protocolo) VALUES (%s, %s, %s)
        """, (id_candidato, data_hora, criptografar_hill(protocolo)))
        conn.commit()
        return True
    except mysql.connector.Error as erro:
        print("Erro ao inserir voto:", erro)
        conn.rollback()
        return False


def atualizar_status_eleitor(id_eleitor):
    cursor.execute("UPDATE eleitor SET status_voto = 'JA_VOTOU' WHERE id = %s", (id_eleitor,))
    conn.commit()


def inserir_log(data_hora, descricao):
    cursor.execute("""
        INSERT INTO log_ocorrencias (data_hora, descricao) VALUES (%s, %s)
    """, (data_hora, descricao))
    conn.commit()


def resetar_votacao():
    cursor.execute("DELETE FROM voto")
    cursor.execute("UPDATE eleitor SET status_voto = 'NAO_VOTOU'")
    conn.commit()


# ========================
# AUDITORIA
# ========================

def listar_logs():
    cursor.execute("SELECT data_hora, descricao FROM log_ocorrencias ORDER BY data_hora DESC")
    return cursor.fetchall()


def listar_protocolos():
    cursor.execute("SELECT protocolo, data_hora, id_candidato FROM voto ORDER BY data_hora DESC")
    votos = cursor.fetchall()
    for voto in votos:
        voto["protocolo"] = descriptografar_hill(voto["protocolo"])
    return votos


# ========================
# RESULTADOS
# ========================

def buscar_resultados_boletim():
    cursor.execute("""
        SELECT c.nome, c.numero, c.partido, COUNT(v.id) AS total_votos
        FROM candidato c
        LEFT JOIN voto v ON c.id = v.id_candidato
        GROUP BY c.id ORDER BY c.nome ASC
    """)
    return cursor.fetchall()


def contar_eleitores():
    cursor.execute("SELECT COUNT(*) AS total FROM eleitor")
    return cursor.fetchone()["total"]


def contar_eleitores_votaram():
    cursor.execute("SELECT COUNT(*) AS total FROM eleitor WHERE status_voto = 'JA_VOTOU'")
    return cursor.fetchone()["total"]


def buscar_votos_por_partido():
    cursor.execute("""
        SELECT c.partido, COUNT(v.id) AS total_votos
        FROM candidato c
        LEFT JOIN voto v ON c.id = v.id_candidato
        GROUP BY c.partido ORDER BY total_votos DESC
    """)
    return cursor.fetchall()


def contar_votos():
    cursor.execute("SELECT COUNT(*) AS total FROM voto")
    return cursor.fetchone()["total"]


# ========================
# TRANSAÇÃO
# ========================

def salvar():

    conn.commit() # Salva as alterações no banco de dados


def desfazer():

    conn.rollback() # Desfaz as alterações não salvas no banco de dados