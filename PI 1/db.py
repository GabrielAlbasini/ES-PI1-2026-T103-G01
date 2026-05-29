import mysql.connector
from criptografia import (
    criptografar_hill,
    descriptografar_hill
)


# CONEXÃO

conn = None
cursor = None

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lobo2404$",
        database="sistema_votacao"
    )
    cursor = conn.cursor(dictionary=True)

except mysql.connector.Error as erro:
    print("Erro ao conectar no banco:", erro)


# ELEITOR

def inserir_eleitor(nome, cpf, titulo, mesario, chave):
    """
    Insere um novo eleitor no banco de dados com dados sensíveis criptografados.

    Criptografa o CPF e a chave de acesso antes de persistir o registro.
    Realiza rollback automático em caso de falha na operação.

    Args:
        nome (str): Nome completo do eleitor.
        cpf (str): CPF do eleitor, será criptografado antes de salvar.
        titulo (str): Número do título eleitoral do eleitor.
        mesario (bool): Indica se o eleitor exerce função de mesário.
        chave (str): Chave de acesso do eleitor, será criptografada antes de salvar.

    Returns:
        bool: True se o eleitor foi inserido com sucesso, False em caso de erro.
    """
    if not conn or not cursor:
        print("Banco indisponível.")
        return False

    try:
        cursor.execute("""
            INSERT INTO eleitor
            (nome_completo,
             cpf,
             titulo_eleitor,
             mesario,
             chave_acesso)
            VALUES
            (%s,%s,%s,%s,%s)
        """, (
            nome,
            criptografar_hill(cpf),  # Criptografa dados sensíveis
            titulo,
            mesario,
            criptografar_hill(chave)
        ))

        conn.commit()
        return True

    except mysql.connector.Error as erro:
        print("Erro ao inserir eleitor:", erro)
        conn.rollback()
        return False


def buscar_por_titulo(titulo):
    """
    Busca um eleitor no banco de dados pelo número do título eleitoral.

    Após localizar o registro, descriptografa o CPF e a chave de
    acesso antes de retornar os dados ao chamador.

    Args:
        titulo (str): Número do título eleitoral a ser pesquisado.

    Returns:
        dict: Dicionário com os dados do eleitor descriptografados,
              ou None se não encontrado ou em caso de erro.
    """
    if not conn or not cursor:
        print("Banco indisponível.")
        return None

    try:
        cursor.execute(
            "SELECT * FROM eleitor WHERE titulo_eleitor = %s",
            (titulo,)
        )

        eleitor = cursor.fetchone()

        # Descriptografa dados
        if eleitor:
            eleitor["cpf"] = descriptografar_hill(eleitor["cpf"])
            eleitor["chave_acesso"] = descriptografar_hill(eleitor["chave_acesso"])

        return eleitor

    except mysql.connector.Error as erro:
        print("Erro ao buscar eleitor:", erro)
        return None


def buscar_por_cpf_ou_titulo(cpf, titulo):
    """
    Busca um eleitor pelo CPF ou pelo título eleitoral.

    Criptografa o CPF para comparação com os dados armazenados e
    descriptografa os dados sensíveis do registro encontrado antes
    de retorná-lo.

    Args:
        cpf (str): CPF do eleitor a ser pesquisado.
        titulo (str): Número do título eleitoral a ser pesquisado.

    Returns:
        dict: Dicionário com os dados do eleitor descriptografados,
              ou None se não encontrado ou em caso de erro.
    """
    if not conn or not cursor:
        print("Banco indisponível.")
        return None

    try:
        cursor.execute("""
            SELECT *
            FROM eleitor
            WHERE cpf = %s
            OR titulo_eleitor = %s
        """, (criptografar_hill(cpf), titulo))

        eleitor = cursor.fetchone()

        if eleitor:
            eleitor["cpf"] = descriptografar_hill(eleitor["cpf"])
            eleitor["chave_acesso"] = descriptografar_hill(eleitor["chave_acesso"])

        return eleitor

    except mysql.connector.Error as erro:
        print("Erro ao buscar eleitor:", erro)
        return None


def listar_todos():
    """
    Retorna todos os eleitores cadastrados no banco de dados.

    Descriptografa o CPF e a chave de acesso de cada registro
    antes de retornar a lista completa.

    Args:
        Nenhum.

    Returns:
        list: Lista de dicionários com os dados de todos os eleitores
              descriptografados, ou lista vazia em caso de erro.
    """
    if not conn or not cursor:
        print("Banco indisponível.")
        return []

    try:
        cursor.execute("SELECT * FROM eleitor")
        eleitores = cursor.fetchall()

        # Descriptografa registros
        for eleitor in eleitores:
            eleitor["cpf"] = descriptografar_hill(eleitor["cpf"])
            eleitor["chave_acesso"] = descriptografar_hill(eleitor["chave_acesso"])

        return eleitores

    except mysql.connector.Error as erro:
        print("Erro ao listar eleitores:", erro)
        return []


def atualizar_eleitor(nome, cpf, mesario, titulo):
    """
    Atualiza os dados cadastrais de um eleitor identificado pelo título.

    Criptografa o CPF antes de persistir a alteração e realiza
    rollback automático em caso de falha.

    Args:
        nome (str): Novo nome completo do eleitor.
        cpf (str): Novo CPF do eleitor, será criptografado antes de salvar.
        mesario (bool): Novo valor indicando se o eleitor é mesário.
        titulo (str): Título eleitoral usado para localizar o registro.

    Returns:
        bool: True se a atualização foi realizada com sucesso, False em caso de erro.
    """
    if not conn or not cursor:
        print("Banco indisponível.")
        return False

    try:
        cursor.execute("""
            UPDATE eleitor
            SET nome_completo = %s,
                cpf = %s,
                mesario = %s
            WHERE titulo_eleitor = %s
        """, (nome, criptografar_hill(cpf), mesario, titulo))

        conn.commit()
        return True

    except mysql.connector.Error as erro:
        print("Erro ao atualizar eleitor:", erro)
        conn.rollback()
        return False


def remover_por_titulo(titulo):
    """
    Remove um eleitor do banco de dados com base no título eleitoral.

    Realiza rollback automático caso ocorra algum erro durante
    a exclusão do registro.

    Args:
        titulo (str): Número do título eleitoral do eleitor a ser removido.

    Returns:
        bool: True se a remoção foi realizada com sucesso, False em caso de erro.
    """
    if not conn or not cursor:
        print("Banco indisponível.")
        return False

    try:
        cursor.execute(
            "DELETE FROM eleitor WHERE titulo_eleitor=%s",
            (titulo,)
        )
        conn.commit()
        return True

    except mysql.connector.Error as erro:
        print("Erro ao remover eleitor:", erro)
        conn.rollback()
        return False


# VOTAÇÃO

def listar_candidatos():
    """
    Retorna todos os candidatos cadastrados ordenados pelo número.

    Args:
        Nenhum.

    Returns:
        list: Lista de dicionários com id, número, nome e partido
              de cada candidato.
    """
    cursor.execute("""
        SELECT id, numero, nome, partido
        FROM candidato
        ORDER BY numero
    """)
    return cursor.fetchall()


def buscar_candidato(numero):
    """
    Busca um candidato pelo número de urna.

    Args:
        numero (int): Número do candidato na urna.

    Returns:
        dict: Dicionário com id, nome e partido do candidato,
              ou None se não encontrado.
    """
    cursor.execute("""
        SELECT id, nome, partido
        FROM candidato
        WHERE numero = %s
    """, (numero,))
    return cursor.fetchone()


def inserir_voto(id_candidato, data_hora, protocolo):
    """
    Registra um voto no banco de dados com o protocolo criptografado.

    Criptografa o protocolo antes de persistir e realiza rollback
    automático em caso de falha.

    Args:
        id_candidato (int): Identificador do candidato votado.
        data_hora (datetime): Data e hora em que o voto foi computado.
        protocolo (str): Código de protocolo do voto, será criptografado.

    Returns:
        bool: True se o voto foi registrado com sucesso, False em caso de erro.
    """
    try:
        cursor.execute("""
            INSERT INTO voto
            (id_candidato, data_hora, protocolo)
            VALUES (%s,%s,%s)
        """, (
            id_candidato,
            data_hora,
            criptografar_hill(protocolo)  # Criptografa protocolo
        ))

        conn.commit()
        return True

    except mysql.connector.Error as erro:
        print("Erro ao inserir voto:", erro)
        conn.rollback()
        return False


def atualizar_status_eleitor(id_eleitor):
    """
    Marca o eleitor como já tendo votado na sessão atual.

    Atualiza o campo status_voto para 'JA_VOTOU' no registro
    correspondente ao id informado.

    Args:
        id_eleitor (int): Identificador único do eleitor no banco.

    Returns:
        bool: True se o status foi atualizado com sucesso, False em caso de erro.
    """
    try:
        cursor.execute("""
            UPDATE eleitor
            SET status_voto = 'JA_VOTOU'
            WHERE id = %s
        """, (id_eleitor,))

        conn.commit()
        return True

    except mysql.connector.Error as erro:
        print("Erro ao atualizar status:", erro)
        conn.rollback()
        return False


def inserir_log(data_hora, descricao):
    """
    Registra uma ocorrência na tabela de logs do sistema.

    Args:
        data_hora (datetime): Data e hora em que o evento ocorreu.
        descricao (str): Texto descritivo do evento registrado.

    Returns:
        bool: True se o log foi inserido com sucesso, False em caso de erro.
    """
    try:
        cursor.execute("""
            INSERT INTO log_ocorrencias
            (data_hora, descricao)
            VALUES (%s,%s)
        """, (data_hora, descricao))

        conn.commit()
        return True

    except mysql.connector.Error as erro:
        print("Erro ao inserir log:", erro)
        conn.rollback()
        return False


def resetar_votacao():
    """
    Apaga todos os votos e redefine o status de todos os eleitores.

    Remove todos os registros da tabela de votos e atualiza o
    status_voto de todos os eleitores para 'NAO_VOTOU', permitindo
    reiniciar a sessão de votação.

    Args:
        Nenhum.

    Returns:
        bool: True se o reset foi concluído com sucesso, False em caso de erro.
    """
    try:
        # Limpa votos registrados
        cursor.execute("DELETE FROM voto")
        cursor.execute("UPDATE eleitor SET status_voto = 'NAO_VOTOU'")
        conn.commit()
        return True

    except mysql.connector.Error as erro:
        print("Erro ao resetar votação:", erro)
        conn.rollback()
        return False


# AUDITORIA

def listar_logs():
    """
    Retorna todos os logs de ocorrências ordenados do mais recente ao mais antigo.

    Args:
        Nenhum.

    Returns:
        list: Lista de dicionários com data_hora e descricao de cada log.
    """
    cursor.execute("""
        SELECT data_hora, descricao
        FROM log_ocorrencias
        ORDER BY data_hora DESC
    """)
    return cursor.fetchall()


def listar_protocolos():
    """
    Retorna todos os protocolos de votos com os dados descriptografados.

    Busca os votos registrados, descriptografa cada protocolo e
    retorna a lista ordenada do mais recente ao mais antigo.

    Args:
        Nenhum.

    Returns:
        list: Lista de dicionários com protocolo, data_hora e
              id_candidato de cada voto.
    """
    cursor.execute("""
        SELECT protocolo, data_hora, id_candidato
        FROM voto
        ORDER BY data_hora DESC
    """)

    votos = cursor.fetchall()

    # Descriptografa protocolos
    for voto in votos:
        voto["protocolo"] = descriptografar_hill(voto["protocolo"])

    return votos


# RESULTADOS

def buscar_resultados_boletim():
    """
    Retorna os totais de votos por candidato e o total de votos nulos.

    Realiza duas consultas: a primeira agrupa os votos por candidato
    com seus dados; a segunda conta os votos sem candidato associado.

    Args:
        Nenhum.

    Returns:
        tuple: Par contendo uma lista de dicionários com nome, número,
               partido e total_votos de cada candidato, e um inteiro
               com o total de votos nulos.
    """
    cursor.execute("""
        SELECT
            c.nome,
            c.numero,
            c.partido,
            COUNT(v.id) AS total_votos
        FROM candidato c
        LEFT JOIN voto v ON c.id = v.id_candidato
        GROUP BY c.id
        ORDER BY c.nome ASC
    """)

    resultados = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) AS total_nulos
        FROM voto
        WHERE id_candidato IS NULL
    """)

    row = cursor.fetchone()
    total_nulos = row["total_nulos"] if row else 0

    return resultados, total_nulos


def contar_eleitores():
    """
    Retorna o total de eleitores cadastrados no sistema.

    Args:
        Nenhum.

    Returns:
        int: Quantidade total de eleitores na tabela eleitor.
    """
    cursor.execute("SELECT COUNT(*) AS total FROM eleitor")
    return cursor.fetchone()["total"]


def contar_eleitores_votaram():
    """
    Retorna o total de eleitores que já votaram na sessão atual.

    Args:
        Nenhum.

    Returns:
        int: Quantidade de eleitores com status_voto igual a 'JA_VOTOU'.
    """
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM eleitor
        WHERE status_voto = 'JA_VOTOU'
    """)
    return cursor.fetchone()["total"]


def buscar_votos_por_partido():
    """
    Retorna o total de votos agrupados por partido, em ordem decrescente.

    Args:
        Nenhum.

    Returns:
        list: Lista de dicionários com partido e total_votos,
              ordenada do mais votado ao menos votado.
    """
    cursor.execute("""
        SELECT
            c.partido,
            COUNT(v.id) AS total_votos
        FROM candidato c
        LEFT JOIN voto v ON c.id = v.id_candidato
        GROUP BY c.partido
        ORDER BY total_votos DESC
    """)
    return cursor.fetchall()


def contar_votos():
    """
    Retorna o total de votos registrados na sessão atual.

    Args:
        Nenhum.

    Returns:
        int: Quantidade total de registros na tabela voto.
    """
    cursor.execute("SELECT COUNT(*) AS total FROM voto")
    return cursor.fetchone()["total"]


# TRANSAÇÃO

def salvar():
    """
    Confirma as transações pendentes no banco de dados.

    Args:
        Nenhum.

    Returns:
        None
    """
    conn.commit()


def desfazer():
    """
    Desfaz as transações pendentes não confirmadas no banco de dados.

    Args:
        Nenhum.

    Returns:
        None
    """
    conn.rollback()


# FECHAR CONEXÃO

def fechar_conexao():
    """
    Encerra o cursor e a conexão com o banco de dados.

    Verifica se cada recurso está aberto antes de fechá-lo,
    evitando erros caso já estejam encerrados.

    Args:
        Nenhum.

    Returns:
        None
    """
    if cursor:
        cursor.close()

    if conn:
        conn.close()