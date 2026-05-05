import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lobo2404$",
        database="sistema_votacao"
    )

    cursor = conn.cursor(dictionary=True)

except mysql.connector.Error as err:
    print("Erro ao conectar no banco:", err)

def inserir_eleitor(nome, cpf, titulo, mesario, chave):
    sql = """
    INSERT INTO eleitor 
    (nome_completo, cpf, titulo_eleitor, mesario, chave_acesso)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (nome, cpf, titulo, mesario, chave))
    conn.commit()
    
def buscar_por_titulo(titulo):
    cursor.execute("SELECT * FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
    return cursor.fetchone()


def buscar_por_cpf_ou_titulo(cpf, titulo):
    cursor.execute(
        "SELECT * FROM eleitor WHERE cpf = %s OR titulo_eleitor = %s",
        (cpf, titulo)
    )
    return cursor.fetchone()


def listar_todos():
    cursor.execute("SELECT * FROM eleitor")
    return cursor.fetchall()


def atualizar_eleitor(nome, cpf, mesario, titulo):
    sql = """
    UPDATE eleitor
    SET nome_completo = %s,
        cpf = %s,
        mesario = %s
    WHERE titulo_eleitor = %s
    """
    cursor.execute(sql, (nome, cpf, mesario, titulo))
    conn.commit()


def remover_por_titulo(titulo):
    cursor.execute("DELETE FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
    conn.commit()

# =========================
# VOTO
# =========================

def buscar_eleitor_login(titulo, chave):
    cursor.execute(
        "SELECT id, nome_completo, status_voto FROM eleitor WHERE titulo_eleitor=%s AND chave_acesso=%s",
        (titulo, chave)
    )
    return cursor.fetchone()


def listar_candidatos():
    cursor.execute("SELECT id, numero, nome, partido FROM candidato ORDER BY numero")
    return cursor.fetchall()


def buscar_candidato(numero):
    cursor.execute("SELECT id, nome FROM candidato WHERE numero = %s", (numero,))
    return cursor.fetchone()


def registrar_voto_db(id_candidato, data, protocolo):
    cursor.execute(
        "INSERT INTO voto (id_candidato, data_hora, protocolo) VALUES (%s, %s, %s)",
        (id_candidato, data, protocolo)
    )


def atualizar_status(id_eleitor):
    cursor.execute(
        "UPDATE eleitor SET status_voto='JA_VOTOU' WHERE id=%s",
        (id_eleitor,)
    )


def registrar_log(data, descricao):
    cursor.execute(
        "INSERT INTO log_ocorrencias (data_hora, descricao) VALUES (%s, %s)",
        (data, descricao)
    )


def commit():
    conn.commit()


def rollback():
    conn.rollback()