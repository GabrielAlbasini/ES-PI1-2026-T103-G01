from db import (
    buscar_eleitor_login,
    listar_candidatos,
    buscar_candidato,
    inserir_voto,
    atualizar_status_eleitor,
    inserir_log,
    resetar_votacao,
    salvar,
    desfazer
)
from auditoria import registrar
from datetime import datetime
import secrets


def gerar_protocolo():
    return secrets.token_hex(8).upper()


def iniciar_votacao():
    print("\n--- INICIAR VOTAÇÃO ---")

    confirm = input("Deseja iniciar uma nova votação? (s/n): ").lower()

    if confirm == 's':
        resetar_votacao()
        salvar()
        registrar("votação reiniciada")
        print("Votação reiniciada com sucesso!")
    else:
        print("Operação cancelada.")


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
            registrar(f"Tentativa de login inválido - título: {titulo}")
            print("Eleitor não encontrado ou chave incorreta.")
            return

        if eleitor["status_voto"] == "JA_VOTOU":
            registrar(f"Tentativa de voto duplicado - eleitor {eleitor['nome_completo']}")
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
            registrar(f"Candidato inválido - número {numero}")
            print("Candidato não existe.")
            return

        agora = datetime.now()
        protocolo = gerar_protocolo()

        inserir_voto(candidato["id"], agora, protocolo)
        atualizar_status_eleitor(eleitor["id"])
        inserir_log(agora, f"SUCESSO: voto registrado para {eleitor['nome_completo']}")
        registrar(f"Voto registrado - eleitor: {eleitor['nome_completo']}, candidato: {candidato['nome']}")
        salvar()

        print(f"Voto registrado com sucesso! Protocolo: {protocolo}")

    except Exception as erro:
        desfazer()
        registrar(f"Erro ao registrar voto: {erro}")
        print("Erro ao registrar voto:", erro)