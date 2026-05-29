from datetime import datetime
from db import (
    listar_logs,
    listar_protocolos,
    inserir_log
)

arquivo_atual = None


# INICIAR ARQUIVO DE AUDITORIA

def iniciar_auditoria():

    global arquivo_atual

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    arquivo_atual = (
        f"auditoria_{timestamp}.txt"
    )

    with open(
        arquivo_atual,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            f"=== INÍCIO DA "
            f"VOTAÇÃO {timestamp} ===\n"
        )


# REGISTRAR EVENTO

def registrar(mensagem):

    global arquivo_atual

    # Cria arquivo se não existir
    if arquivo_atual is None:

        iniciar_auditoria()

    agora = datetime.now()

    data_hora = agora.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        arquivo_atual,
        "a",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            f"[{data_hora}] "
            f"{mensagem}\n"
        )

    # Salva log no banco
    inserir_log(
        agora,
        mensagem
    )


# EXIBIR LOGS

def exibir_logs():

    print(
        "\n=== LOGS DO "
        "SISTEMA ==="
    )

    logs = listar_logs()

    if not logs:

        print(
            "Nenhum log encontrado."
        )

        return

    # Exibe todos os logs
    for log in logs:

        print("\n----------")

        print(
            f"Data/Hora: "
            f"{log['data_hora']}"
        )

        print(
            f"Descrição: "
            f"{log['descricao']}"
        )


# EXIBIR PROTOCOLOS

def exibir_protocolos():

    print(
        "\n=== PROTOCOLOS "
        "DE VOTAÇÃO ==="
    )

    protocolos = listar_protocolos()

    if not protocolos:

        print(
            "Nenhum protocolo "
            "encontrado."
        )

        return

    # Exibe protocolos registrados
    for p in protocolos:

        print("\n----------")

        print(
            f"Protocolo: "
            f"{p['protocolo']}"
        )