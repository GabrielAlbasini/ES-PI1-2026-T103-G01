from datetime import datetime 

def registrar(mensagem):
    with open("auditoria.txt", "a") as arquivo:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        arquivo.write(f"[{data_hora}] {mensagem}\n")
        
from db import listar_logs, listar_protocolos


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
        print(f"Candidato ID: {p['candidato_id']}")


