from db import (
    buscar_eleitor_login,
    listar_candidatos,
    buscar_candidato,
    inserir_voto,
    atualizar_status_eleitor,
    inserir_log,
    resetar_votacao,
    buscar_por_titulo,
    salvar,
    desfazer
)
from validações import solicitar_cpf_parcial
from auditoria import registrar
from datetime import datetime
import secrets

votacao_aberta = False


def gerar_protocolo():
    return secrets.token_hex(8).upper()


# INICIAR VOTAÇÃO

def iniciar_votacao():
    global votacao_aberta

    print("\n--- INICIAR VOTAÇÃO ---")

    titulo = input("Título do mesário: ").strip()
    cpf_parcial = solicitar_cpf_parcial()

    eleitor = buscar_por_titulo(titulo)

    if not eleitor:
        registrar("ALERTA: Tentativa de acesso negado")
        print("Mesário não encontrado.")
        return

    if eleitor["cpf"][:4] != cpf_parcial:
        registrar("ALERTA: Tentativa de acesso negado")
        print("CPF incorreto.")
        return

    if not eleitor["mesario"]:
        registrar("ALERTA: Tentativa de acesso negado")
        print("Apenas mesários podem iniciar a votação.")
        return

    confirm = input("Deseja iniciar uma nova votação? (s/n): ").lower()

    if confirm == 's':
        try:
            resetar_votacao()
            salvar()
            votacao_aberta = True

            registrar("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")

            print("Votação iniciada com sucesso!")

        except Exception as erro:
            desfazer()
            print("Erro ao iniciar votação:", erro)

    else:
        print("Operação cancelada.")

# ENCERRAR VOTAÇÃO

def encerrar_votacao():
    global votacao_aberta

    print("\n--- ENCERRAR VOTAÇÃO ---")

    if not votacao_aberta:
        print("A votação já está encerrada.")
        return

    titulo = input("Título do mesário: ").strip()
    cpf_parcial = solicitar_cpf_parcial()

    eleitor = buscar_por_titulo(titulo)

    if not eleitor:
        registrar("ALERTA: Tentativa de acesso negado")
        print("Mesário não encontrado.")
        return

    if eleitor["cpf"][:4] != cpf_parcial:
        registrar("ALERTA: Tentativa de acesso negado")
        print("CPF incorreto.")
        return

    if not eleitor["mesario"]:
        registrar("ALERTA: Tentativa de acesso negado")
        print("Apenas mesários podem encerrar a votação.")
        return

    confirm = input("Deseja realmente encerrar a votação? (s/n): ").lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    votacao_aberta = False

    registrar("ENCERRAMENTO: Votação finalizada com sucesso.")

    print("Votação encerrada com sucesso!")

# REGISTRAR VOTO

def registrar_voto():
    print("\n--- REGISTRO DE VOTO ---")

    if not votacao_aberta:
        print("A votação está encerrada!")
        return

    titulo = input("Título de eleitor: ").strip()
    cpf_parcial = solicitar_cpf_parcial()

    if not titulo or not cpf_parcial:
        return

    try:
        eleitor = buscar_eleitor_login(titulo)

        if not eleitor:
            registrar("ALERTA: Tentativa de acesso negado")
            print("Eleitor não encontrado.")
            return

        if eleitor["cpf"][:4] != cpf_parcial:
            registrar("ALERTA: Tentativa de acesso negado")
            print("CPF incorreto.")
            return

        if eleitor["status_voto"] == "JA_VOTOU":
            registrar("ALERTA: Tentativa de voto duplo")
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

        confirm = input(f"Confirmar voto em {candidato['nome']}? (s/n): ").lower()

        if confirm != "s":
            print("Voto cancelado.")
            return

        agora = datetime.now()
        protocolo = gerar_protocolo()

        inserir_voto(candidato["id"], agora, protocolo)
        atualizar_status_eleitor(eleitor["id"])
        inserir_log(agora, f"SUCESSO: voto registrado para {eleitor['nome_completo']}")
        registrar("SUCESSO: Voto realizado com sucesso")
        salvar()

        print(f"\nVoto registrado com sucesso!")
        print(f"Protocolo: {protocolo}")

    except Exception as erro:
        desfazer()
        print("Erro ao registrar voto:", erro)