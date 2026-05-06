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


# ELEITOR

def inserir_eleitor(nome, cpf, titulo, mesario, chave):
    try:
        cursor.execute("""
            INSERT INTO eleitor 
            (nome_completo, cpf, titulo_eleitor, mesario, chave_acesso)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, cpf, titulo, mesario, chave))
        return True
    except:
        return False


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
    try:
        cursor.execute("""
            UPDATE eleitor
            SET nome_completo = %s,
                cpf = %s,
                mesario = %s
            WHERE titulo_eleitor = %s
        """, (nome, cpf, mesario, titulo))
        return True
    except:
        return False


def remover_por_titulo(titulo):
    try:
        cursor.execute(
            "DELETE FROM eleitor WHERE titulo_eleitor = %s",
            (titulo,)
        )
        return True
    except:
        return False


# VOTAÇÃO

def buscar_eleitor_login(titulo, chave):
    cursor.execute("""
        SELECT id, nome_completo, status_voto 
        FROM eleitor 
        WHERE titulo_eleitor = %s AND chave_acesso = %s
    """, (titulo, chave))
    return cursor.fetchone()


def listar_candidatos():
    cursor.execute("SELECT id, numero, nome, partido FROM candidato ORDER BY numero")
    return cursor.fetchall()


def buscar_candidato(numero):
    cursor.execute("SELECT id, nome FROM candidato WHERE numero = %s", (numero,))
    return cursor.fetchone()


def inserir_voto(id_candidato, data_hora, protocolo):
    cursor.execute("""
        INSERT INTO voto (id_candidato, data_hora, protocolo)
        VALUES (%s, %s, %s)
    """, (id_candidato, data_hora, protocolo))


def atualizar_status_eleitor(id_eleitor):
    cursor.execute(
        "UPDATE eleitor SET status_voto = 'JA_VOTOU' WHERE id = %s",
        (id_eleitor,)
    )


def inserir_log(data_hora, descricao):
    cursor.execute("""
        INSERT INTO log_ocorrencias (data_hora, descricao)
        VALUES (%s, %s)
    """, (data_hora, descricao))


def resetar_votacao():
    cursor.execute("DELETE FROM voto")
    cursor.execute("UPDATE eleitor SET status_voto = 'NAO_VOTOU'")


# CONTROLE DA VOTAÇÃO


def abrir_votacao():
    cursor.execute("UPDATE controle_votacao SET status = 'ABERTA' WHERE id = 1")


def fechar_votacao():
    cursor.execute("UPDATE controle_votacao SET status = 'FECHADA' WHERE id = 1")


def obter_status_votacao():
    cursor.execute("SELECT status FROM controle_votacao WHERE id = 1")
    resultado = cursor.fetchone()
    return resultado["status"] if resultado else "FECHADA"


# AUDITORIA

def listar_logs():
    cursor.execute("""
        SELECT data_hora, descricao 
        FROM log_ocorrencias 
        ORDER BY data_hora DESC
    """)
    return cursor.fetchall()


def listar_protocolos():
    cursor.execute("""
        SELECT protocolo, data_hora, id_candidato 
        FROM voto 
        ORDER BY data_hora DESC
    """)
    return cursor.fetchall()


# TRANSAÇÃO

def salvar():
    conn.commit()


def desfazer():
    conn.rollback()