# Importação das funções do banco de dados
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

# Importação da função de solicitação parcial do CPF
from validações import solicitar_cpf_parcial

# Importação do sistema de auditoria
from auditoria import registrar

# Importação de data/hora
from datetime import datetime

# Bibliotecas para geração segura de códigos aleatórios
import secrets
import string


# Controle global do estado da votação
votacao_aberta = False


# Gera um protocolo único de votação
def gerar_protocolo(numero_candidato):

    # Gera 2 letras aleatórias
    letras = ''.join(
        secrets.choice(string.ascii_uppercase)
        for _ in range(2)
    )

    # Obtém os 2 últimos dígitos do ano atual
    ano = datetime.now().strftime("%y")

    # Completa o número do candidato com zeros à esquerda
    num_candidato = str(numero_candidato).zfill(2)

    # Gera 5 números aleatórios
    digitos = ''.join(
        secrets.choice(string.digits)
        for _ in range(5)
    )

    # Monta o protocolo final
    return f"V{letras}{ano}{num_candidato}{digitos}"


# Realiza autenticação do mesário
def autenticar_mesario():

    titulo = input("Título do mesário: ").strip()

    cpf_parcial = solicitar_cpf_parcial()

    chave_digitada = input(
        "Chave de acesso: "
    ).strip().upper()

    # Busca eleitor pelo título
    eleitor = buscar_por_titulo(titulo)

    # Verifica existência do mesário
    if not eleitor:

        registrar(
            "ALERTA: Tentativa de acesso negado"
        )

        print("Mesário não encontrado.")

        return None

    # Validação dos 4 primeiros dígitos do CPF
    if eleitor["cpf"][:4] != cpf_parcial:

        registrar(
            "ALERTA: Tentativa de acesso negado"
        )

        print("CPF incorreto.")

        return None

    # Verifica chave de acesso
    if eleitor["chave_acesso"] != chave_digitada:

        registrar(
            "ALERTA: Tentativa de acesso negado"
        )

        print("Chave de acesso incorreta.")

        return None

    # Verifica permissão de mesário
    if not eleitor["mesario"]:

        registrar(
            "ALERTA: Tentativa de acesso negado"
        )

        print(
            "Apenas mesários podem realizar esta operação."
        )

        return None

    return eleitor


# Inicia uma nova votação
def iniciar_votacao():

    global votacao_aberta

    print("\n=== INICIAR VOTAÇÃO ===")

    # Autenticação obrigatória do mesário
    mesario = autenticar_mesario()

    if not mesario:
        return

    confirm = input(
        "Deseja iniciar uma nova votação? (s/n): "
    ).lower()

    # Confirmação do usuário
    if confirm != 's':

        print("Operação cancelada.")

        return

    try:

        # Limpa votos anteriores
        resetar_votacao()

        salvar()

        # Marca votação como aberta
        votacao_aberta = True

        registrar(
            "ABERTURA: Votação iniciada com sucesso. Total de votos zerado."
        )

        # Lista candidatos cadastrados
        candidatos = listar_candidatos()

        if not candidatos:

            print(
                "Nenhum candidato cadastrado."
            )

        else:

            print(
                "Votação iniciada com sucesso!"
            )

    except Exception as erro:

        desfazer()

        print(
            "Erro ao iniciar votação:",
            erro
        )


# Encerra a votação
def encerrar_votacao():

    global votacao_aberta

    print("\n=== ENCERRAR VOTAÇÃO ===")

    # Verifica se já está encerrada
    if not votacao_aberta:

        print(
            "A votação já está encerrada."
        )

        return

    # Autenticação do mesário
    mesario = autenticar_mesario()

    if not mesario:
        return

    confirm = input(
        "Deseja realmente encerrar a votação? (Sim/Não): "
    ).strip().lower()

    # Confirma encerramento
    if confirm != "sim":

        print("Operação cancelada.")

        return

    # Confirmação extra com chave
    chave_confirmacao = input(
        "Digite sua chave de acesso novamente para confirmar: "
    ).strip().upper()

    # Verifica chave
    if chave_confirmacao != mesario["chave_acesso"]:

        registrar(
            "ALERTA: Tentativa de acesso negado"
        )

        print(
            "Chave incorreta. Encerramento cancelado."
        )

        return

    # Fecha votação
    votacao_aberta = False

    registrar(
        "ENCERRAMENTO: Votação finalizada com sucesso."
    )

    print(
        "Votação encerrada com sucesso!"
    )


# Registra o voto do eleitor
def registrar_voto():

    print("\n=== REGISTRO DE VOTO ===")

    # Verifica se a votação está aberta
    if not votacao_aberta:

        print(
            "A votação está encerrada!"
        )

        return

    titulo = input(
        "Título de eleitor: "
    ).strip()

    cpf_parcial = solicitar_cpf_parcial()

    chave_digitada = input(
        "Chave de acesso: "
    ).strip().upper()

    # Verifica campos obrigatórios
    if not titulo or not cpf_parcial:
        return

    try:

        # Busca eleitor
        eleitor = buscar_por_titulo(titulo)

        if not eleitor:

            registrar(
                "ALERTA: Tentativa de acesso negado"
            )

            print(
                "Eleitor não encontrado."
            )

            return

        # Validação parcial do CPF
        if eleitor["cpf"][:4] != cpf_parcial:

            registrar(
                "ALERTA: Tentativa de acesso negado"
            )

            print("CPF incorreto.")

            return

        # Verificação da chave
        if eleitor["chave_acesso"] != chave_digitada:

            registrar(
                "ALERTA: Tentativa de acesso negado"
            )

            print(
                "Chave de acesso incorreta."
            )

            return

        # Impede voto duplicado
        if eleitor["status_voto"] == "JA_VOTOU":

            registrar(
                "ALERTA: Tentativa de voto duplo"
            )

            print(
                "Esse eleitor já votou."
            )

            return

        # Loop de votação
        while True:

            numero = input(
                "Digite o número do candidato: "
            ).strip()

            # Validação numérica
            if not numero.isdigit():

                print(
                    "Número inválido. Tente novamente."
                )

                continue

            # Busca candidato
            candidato = buscar_candidato(
                int(numero)
            )

            if candidato:

                print(
                    f"\nCandidato: {candidato['nome']}"
                )

                print(
                    f"Número: {numero}"
                )

                print(
                    f"Partido: {candidato['partido']}"
                )

                confirm = input(
                    "Confirmar voto? (s/n): "
                ).lower()

            else:

                print(
                    "\nCandidato não encontrado. O voto será registrado como NULO."
                )

                confirm = input(
                    "Confirmar voto nulo? (s/n): "
                ).lower()

            # Sai do loop se confirmado
            if confirm == "s":
                break

            else:

                print(
                    "Voto não confirmado. Digite o número novamente.\n"
                )

                continue

        # Dados do registro do voto
        agora = datetime.now()

        id_candidato = (
            candidato["id"]
            if candidato
            else None
        )

        numero_protocolo = (
            int(numero)
            if candidato
            else 0
        )

        # Geração do protocolo
        protocolo = gerar_protocolo(
            numero_protocolo
        )

        # Salva voto
        inserir_voto(
            id_candidato,
            agora,
            protocolo
        )

        # Atualiza status do eleitor
        atualizar_status_eleitor(
            eleitor["id"]
        )

        # Registra logs
        inserir_log(
            agora,
            "SUCESSO: Voto realizado com sucesso"
        )

        registrar(
            "SUCESSO: Voto realizado com sucesso"
        )

        salvar()

        print(
            "\nVoto registrado com sucesso!"
        )

        print(
            f"Protocolo: {protocolo}"
        )

    except Exception as erro:

        desfazer()

        print(
            "Erro ao registrar voto:",
            erro
        )