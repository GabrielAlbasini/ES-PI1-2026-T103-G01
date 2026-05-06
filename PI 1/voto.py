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

votacao_aberta = False


def gerar_protocolo():
    return secrets.token_hex(8).upper()


# =========================
# INICIAR VOTAÇÃO
# =========================
def iniciar_votacao():
    global votacao_aberta

    print("\n--- INICIAR VOTAÇÃO ---")

    confirm = input("Deseja iniciar uma nova votação? (s/n): ").lower()

    if confirm == 's':
        try:
            resetar_votacao()
            salvar()
            votacao_aberta = True
            registrar("votação iniciada")
            print("Votação iniciada com sucesso!")
        except Exception as erro:
            desfazer()
            print("Erro ao iniciar votação:", erro)
    else:
        print("Operação cancelada.")


# =========================
# ENCERRAR VOTAÇÃO
# =========================
def encerrar_votacao():
    global votacao_aberta

    print("\n--- ENCERRAR VOTAÇÃO ---")

    if not votacao_aberta:
        print("A votação já está encerrada.")
        return

    confirm = input("Deseja realmente encerrar a votação? (s/n): ").lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    votacao_aberta = False
    registrar("votação encerrada")
    print("Votação encerrada com sucesso!")


# =========================
# REGISTRAR VOTO
# =========================
def registrar_voto():
    print("\n--- REGISTRO DE VOTO ---")

    # 🔒 BLOQUEIO
    if not votacao_aberta:
        print("A votação está encerrada!")
        return

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

        confirm = input(f"Confirmar voto em {candidato['nome']}? (s/n): ").lower()

        if confirm != "s":
            print("Voto cancelado.")
            return

        agora = datetime.now()
        protocolo = gerar_protocolo()

        inserir_voto(candidato["id"], agora, protocolo)
        atualizar_status_eleitor(eleitor["id"])
        inserir_log(agora, f"SUCESSO: voto registrado para {eleitor['nome_completo']}")
        registrar(f"Voto registrado - eleitor: {eleitor['nome_completo']}, candidato: {candidato['nome']}")
        salvar()

        print(f"\nVoto registrado com sucesso!")
        print(f"Protocolo: {protocolo}")

    except Exception as erro:
        desfazer()
        registrar(f"Erro ao registrar voto: {erro}")
        print("Erro ao registrar voto:", erro)