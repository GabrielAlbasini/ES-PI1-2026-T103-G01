from datetime import datetime 
from db import listar_logs, listar_protocolos

arquivo_atual = None

def iniciar_auditoria():
    global arquivo_atual

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    arquivo_atual = f"auditoria_{timestamp}.txt"

    with open(arquivo_atual, "w") as arquivo:
        arquivo.write(f"=== INÍCIO DA VOTAÇÃO {timestamp} ===\n")

def registrar(mensagem):
    global arquivo_atual

    # garante que existe arquivo de auditoria
    if arquivo_atual is None:
        iniciar_auditoria()

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open(arquivo_atual, "a") as arquivo:
        arquivo.write(f"[{data_hora}] {mensagem}\n")

def exibir_logs():
    print("\n--- LOGS DO SISTEMA ---")

    logs = listar_logs()

    if not logs:
        print("Nenhum log encontrado.")
        return

    for log in logs:
        print("\n----------")
        print(f"Data/Hora: {log['data_hora']}")
        print(f"Descrição: {log['descricao']}")


def exibir_protocolos():
    print("\n--- PROTOCOLOS DE VOTAÇÃO ---")

    protocolos = listar_protocolos()

    if not protocolos:
        print("Nenhum protocolo encontrado.")
        return

    for p in protocolos:
        print("\n----------")
        print(f"Protocolo: {p['protocolo']}")
        print(f"Data/Hora: {p['data_hora']}")
        print(f"Candidato ID: {p['id_candidato']}")
