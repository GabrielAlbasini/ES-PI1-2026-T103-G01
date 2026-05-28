from db import (
    buscar_candidato,
    listar_candidatos,
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
import string

votacao_aberta = False


def gerar_protocolo(numero_candidato):
    letras = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(2))
    ano = datetime.now().strftime("%y")
    num_candidato = str(numero_candidato).zfill(2)
    digitos = ''.join(secrets.choice(string.digits) for _ in range(5))
    return f"V{letras}{ano}{num_candidato}{digitos}"


def autenticar_mesario():
    titulo = input("Título do mesário: ").strip()
    cpf_parcial = solicitar_cpf_parcial()
    chave_digitada = input("Chave de acesso: ").strip().upper()

    eleitor = buscar_por_titulo(titulo)

    if not eleitor:
        registrar("ALERTA: Tentativa de acesso negado")
        print("Mesário não encontrado.")
        return None

    if eleitor["cpf"][:4] != cpf_parcial:
        registrar("ALERTA: Tentativa de acesso negado")
        print("CPF incorreto.")
        return None

    if eleitor["chave_acesso"] != chave_digitada:
        registrar("ALERTA: Tentativa de acesso negado")
        print("Chave de acesso incorreta.")
        return None

    if not eleitor["mesario"]:
        registrar("ALERTA: Tentativa de acesso negado")
        print("Apenas mesários podem realizar esta operação.")
        return None

    return eleitor


def iniciar_votacao():
    global votacao_aberta

    print("\n=== INICIAR VOTAÇÃO ===")

    mesario = autenticar_mesario()
    if not mesario:
        return

    confirm = input("Deseja iniciar uma nova votação? (s/n): ").lower()

    if confirm != 's':
        print("Operação cancelada.")
        return

    try:
        resetar_votacao()
        salvar()
        votacao_aberta = True

        registrar("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")

        candidatos = listar_candidatos()
        if not candidatos:
            print("Nenhum candidato cadastrado.")
        else:
            print("Votação iniciada com sucesso!")

    except Exception as erro:
        desfazer()
        print("Erro ao iniciar votação:", erro)


def encerrar_votacao():
    global votacao_aberta

    print("\n=== ENCERRAR VOTAÇÃO ===")

    if not votacao_aberta:
        print("A votação já está encerrada.")
        return

    mesario = autenticar_mesario()
    if not mesario:
        return

    confirm = input("Deseja realmente encerrar a votação? (Sim/Não): ").strip().lower()

    if confirm != "sim":
        print("Operação cancelada.")
        return


    chave_confirmacao = input("Digite sua chave de acesso novamente para confirmar: ").strip().upper()

    if chave_confirmacao != mesario["chave_acesso"]:
        registrar("ALERTA: Tentativa de acesso negado")
        print("Chave incorreta. Encerramento cancelado.")
        return

    votacao_aberta = False
    registrar("ENCERRAMENTO: Votação finalizada com sucesso.")
    print("Votação encerrada com sucesso!")


def registrar_voto():
    print("\n=== REGISTRO DE VOTO ===")

    if not votacao_aberta:
        print("A votação está encerrada!")
        return

    titulo = input("Título de eleitor: ").strip()
    cpf_parcial = solicitar_cpf_parcial()
    chave_digitada = input("Chave de acesso: ").strip().upper()

    if not titulo or not cpf_parcial:
        return

    try:
        eleitor = buscar_por_titulo(titulo)

        if not eleitor:
            registrar("ALERTA: Tentativa de acesso negado")
            print("Eleitor não encontrado.")
            return

        if eleitor["cpf"][:4] != cpf_parcial:
            registrar("ALERTA: Tentativa de acesso negado")
            print("CPF incorreto.")
            return

        if eleitor["chave_acesso"] != chave_digitada:
            registrar("ALERTA: Tentativa de acesso negado")
            print("Chave de acesso incorreta.")
            return

        if eleitor["status_voto"] == "JA_VOTOU":
            registrar("ALERTA: Tentativa de voto duplo")
            print("Esse eleitor já votou.")
            return

        # LOOP: só sai quando confirmar o voto
        while True:
            numero = input("Digite o número do candidato: ").strip()

            if not numero.isdigit():
                print("Número inválido. Tente novamente.")
                continue

            candidato = buscar_candidato(int(numero))

            if candidato:
                print(f"\nCandidato: {candidato['nome']}")
                print(f"Número: {numero}")
                print(f"Partido: {candidato['partido']}")
                confirm = input("Confirmar voto? (s/n): ").lower()
            else:
                print("\nCandidato não encontrado. O voto será registrado como NULO.")
                confirm = input("Confirmar voto nulo? (s/n): ").lower()

            if confirm == "s":
                break
            else:
                print("Voto não confirmado. Digite o número novamente.\n")
                continue

        agora = datetime.now()
        id_candidato = candidato["id"] if candidato else None
        numero_protocolo = int(numero) if candidato else 0
        protocolo = gerar_protocolo(numero_protocolo)

        inserir_voto(id_candidato, agora, protocolo)
        atualizar_status_eleitor(eleitor["id"])
        inserir_log(agora, "SUCESSO: Voto realizado com sucesso")
        registrar("SUCESSO: Voto realizado com sucesso")
        salvar()

        print(f"\nVoto registrado com sucesso!")
        print(f"Protocolo: {protocolo}")

    except Exception as erro:
        desfazer()
        print("Erro ao registrar voto:", erro)