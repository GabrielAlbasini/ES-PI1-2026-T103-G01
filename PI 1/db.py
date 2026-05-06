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
    try:
        cursor.execute("""
            INSERT INTO eleitor 
            (nome_completo, cpf, titulo_eleitor, mesario, chave_acesso)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, cpf, titulo, mesario, chave))

        conn.commit()
        return True

    except Exception as e:
        print("Erro ao inserir eleitor:", e)
        return False


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
    try:
        cursor.execute("""
            UPDATE eleitor
            SET nome_completo = %s,
                cpf = %s,
                mesario = %s
            WHERE titulo_eleitor = %s
        """, (nome, cpf, mesario, titulo))

        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print("Erro ao atualizar eleitor:", e)
        return False


def remover_por_titulo(titulo):
    try:
        cursor.execute(
            "DELETE FROM eleitor WHERE titulo_eleitor = %s",
            (titulo,)
        )

        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print("ERRO REAL AO REMOVER:", e)
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
    try:
        cursor.execute("""
            INSERT INTO voto (id_candidato, data_hora, protocolo)
            VALUES (%s, %s, %s)
        """, (id_candidato, data_hora, protocolo))

        conn.commit()
        return True

    except Exception as e:
        print("Erro ao inserir voto:", e)
        return False


def atualizar_status_eleitor(id_eleitor):
    try:
        cursor.execute(
            "UPDATE eleitor SET status_voto = 'JA_VOTOU' WHERE id = %s",
            (id_eleitor,)
        )

        conn.commit()
        return True

    except Exception as e:
        print("Erro ao atualizar status:", e)
        return False


def inserir_log(data_hora, descricao):
    try:
        cursor.execute("""
            INSERT INTO log_ocorrencias (data_hora, descricao)
            VALUES (%s, %s)
        """, (data_hora, descricao))

        conn.commit()
        return True

    except Exception as e:
        print("Erro ao inserir log:", e)
        return False


def resetar_votacao():
    try:
        cursor.execute("DELETE FROM voto")
        cursor.execute("UPDATE eleitor SET status_voto = 'NAO_VOTOU'")

        conn.commit()
        return True

    except Exception as e:
        print("Erro ao resetar votação:", e)
        return False


# CONTROLE


def salvar():
    conn.commit()


def desfazer():
    conn.rollback()