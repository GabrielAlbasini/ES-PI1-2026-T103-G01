from db import (
    buscar_eleitor_login,
    listar_candidatos,
    buscar_candidato,
    inserir_voto,
    atualizar_status_eleitor,
    inserir_log,
    salvar,
    desfazer
)

from datetime import datetime
import secrets


def gerar_protocolo():
    return secrets.token_hex(8).upper()


def registrar_voto():
    print("\n--- REGISTRO DE VOTO ---")

    titulo = input("Título de eleitor: ").strip()
    chave = input("Chave de acesso: ").strip()

    if not titulo or not chave:
        print("Preencha título e chave.")
        return

    try:
        eleitor = buscar_eleitor_login(titulo, chave)

        if not eleitor:
            print("Eleitor não encontrado ou chave incorreta.")
            return

        if eleitor["status_voto"] == "JA_VOTOU":
            print("Esse eleitor já votou.")
            return

        candidatos = listar_candidatos()

        if not candidatos:
            print("Nenhum candidato cadastrado.")
            return

        print("\nCandidatos:")
        for c in candidatos:
            print(f"{c['numero']} - {c['nome']} ({c['partido']})")

        numero = input("Digite o número do candidato: ").strip()

        if not numero.isdigit():
            print("Número inválido.")
            return

        candidato = buscar_candidato(int(numero))

        if not candidato:
            print("Candidato não existe.")
            return

        agora = datetime.now()
        protocolo = gerar_protocolo()

        inserir_voto(candidato["id"], agora, protocolo)
        atualizar_status_eleitor(eleitor["id"])
        inserir_log(agora, f"SUCESSO: voto registrado para {eleitor['nome_completo']}")

        salvar()

        print(f"Voto registrado com sucesso! Protocolo: {protocolo}")

    except Exception as erro:
        desfazer()
        print("Erro ao registrar voto:", erro)