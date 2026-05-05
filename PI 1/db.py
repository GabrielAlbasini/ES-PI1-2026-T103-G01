import mysql.connector

# CONEXÃO

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
    cursor.execute(
        """
        INSERT INTO eleitor 
        (nome_completo, cpf, titulo_eleitor, mesario, chave_acesso)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nome, cpf, titulo, mesario, chave)
    )


def buscar_por_titulo(titulo):
    cursor.execute(
        "SELECT * FROM eleitor WHERE titulo_eleitor = %s",
        (titulo,)
    )
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
    cursor.execute(
        """
        UPDATE eleitor
        SET nome_completo = %s,
            cpf = %s,
            mesario = %s
        WHERE titulo_eleitor = %s
        """,
        (nome, cpf, mesario, titulo)
    )


def remover_por_titulo(titulo):
    cursor.execute(
        "DELETE FROM eleitor WHERE titulo_eleitor = %s",
        (titulo,)
    )

# VOTAÇÃO

def buscar_eleitor_login(titulo, chave):
    cursor.execute(
        """
        SELECT id, nome_completo, status_voto 
        FROM eleitor 
        WHERE titulo_eleitor = %s AND chave_acesso = %s
        """,
        (titulo, chave)
    )
    return cursor.fetchone()


def listar_candidatos():
    cursor.execute(
        "SELECT id, numero, nome, partido FROM candidato ORDER BY numero"
    )
    return cursor.fetchall()


def buscar_candidato(numero):
    cursor.execute(
        "SELECT id, nome FROM candidato WHERE numero = %s",
        (numero,)
    )
    return cursor.fetchone()


def inserir_voto(id_candidato, data_hora, protocolo):
    cursor.execute(
        """
        INSERT INTO voto (id_candidato, data_hora, protocolo)
        VALUES (%s, %s, %s)
        """,
        (id_candidato, data_hora, protocolo)
    )


def atualizar_status_eleitor(id_eleitor):
    cursor.execute(
        "UPDATE eleitor SET status_voto = 'JA_VOTOU' WHERE id = %s",
        (id_eleitor,)
    )


def inserir_log(data_hora, descricao):
    cursor.execute(
        """
        INSERT INTO log_ocorrencias (data_hora, descricao)
        VALUES (%s, %s)
        """,
        (data_hora, descricao)
    )


def resetar_votacao():
    cursor.execute("DELETE FROM voto")
    cursor.execute("UPDATE eleitor SET status_voto = 'NAO_VOTOU'")


# CONTROLE (TRANSAÇÃO)

def salvar():
    conn.commit()


def desfazer():
    conn.rollback()