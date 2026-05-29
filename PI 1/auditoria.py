from datetime import datetime
from db import (
    listar_logs,
    listar_protocolos,
    inserir_log
)

arquivo_atual = None


# INICIAR ARQUIVO DE AUDITORIA

def iniciar_auditoria():
    """
    Cria e inicializa o arquivo de auditoria da sessão de votação.

    Gera um arquivo .txt com timestamp no nome e escreve o cabeçalho
    de início da votação. O caminho do arquivo é armazenado na
    variável global arquivo_atual.

    Args:
        Nenhum.

    Returns:
        None
    """
    global arquivo_atual
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    arquivo_atual = f"auditoria_{timestamp}.txt"

    with open(arquivo_atual, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"=== INÍCIO DA VOTAÇÃO {timestamp} ===\n")


# REGISTRAR EVENTO

def registrar(mensagem):
    """
    Registra um evento no arquivo de auditoria e no banco de dados.

    Caso o arquivo de auditoria ainda não tenha sido criado,
    inicializa um automaticamente antes de gravar. A mensagem é
    salva com data e hora no arquivo .txt e também inserida
    na tabela de logs do banco.

    Args:
        mensagem (str): Texto descritivo do evento a ser registrado.

    Returns:
        None
    """
    global arquivo_atual

    # Cria arquivo se não existir
    if arquivo_atual is None:
        iniciar_auditoria()

    agora = datetime.now()
    data_hora = agora.strftime("%Y-%m-%d %H:%M:%S")

    with open(arquivo_atual, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{data_hora}] {mensagem}\n")

    # Salva log no banco
    inserir_log(agora, mensagem)


# EXIBIR LOGS

def exibir_logs():
    """
    Busca e exibe no terminal todos os logs registrados no banco.

    Consulta a tabela de logs via listar_logs() e imprime cada
    entrada com data/hora e descrição formatadas. Caso não haja
    registros, exibe uma mensagem informativa.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== LOGS DO SISTEMA ===")
    logs = listar_logs()

    if not logs:
        print("Nenhum log encontrado.")
        return

    # Exibe todos os logs
    for log in logs:
        print("\n----------")
        print(f"Data/Hora: {log['data_hora']}")
        print(f"Descrição: {log['descricao']}")


# EXIBIR PROTOCOLOS

def exibir_protocolos():
    """
    Busca e exibe no terminal todos os protocolos de votação registrados.

    Consulta os protocolos via listar_protocolos() e imprime cada
    número de protocolo encontrado. Caso não haja registros,
    exibe uma mensagem informativa.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== PROTOCOLOS DE VOTAÇÃO ===")
    protocolos = listar_protocolos()

    if not protocolos:
        print("Nenhum protocolo encontrado.")
        return

    # Exibe protocolos registrados
    for p in protocolos:
        print("\n----------")
        print(f"Protocolo: {p['protocolo']}")