from auditoria import registrar
from validações import (
    validar_cpf,
    validar_titulo_eleitor,
    solicitar_cpf,
    solicitar_titulo
)
from db import (
    inserir_eleitor,
    buscar_por_titulo,
    buscar_por_cpf_ou_titulo,
    listar_todos,
    atualizar_eleitor,
    remover_por_titulo
)
import secrets
import string


def gerar_chave_acesso(nome):
    """Gera uma chave de acesso personalizada com base no nome do eleitor.

    Combina as duas primeiras letras do primeiro nome, a inicial do sobrenome
    e quatro dígitos aleatórios gerados de forma segura.

    Args:
        nome (str): Nome completo do eleitor, contendo ao menos nome e sobrenome.

    Returns:
        str: Chave de acesso no formato 'XX Y0000', onde XX são as iniciais do
             primeiro nome, Y é a inicial do sobrenome e 0000 são dígitos aleatórios.

    Raises:
        ValueError: Se o nome informado não contiver ao menos duas palavras.
    """
    partes = nome.strip().split()
    if len(partes) < 2:
        raise ValueError("Digite nome e sobrenome.")

    primeira_parte = partes[0][:2].upper()
    letra_sobrenome = partes[1][0].upper()
    # Usa secrets para garantir aleatoriedade criptograficamente segura
    numeros = ''.join(secrets.choice(string.digits) for _ in range(4))
    return primeira_parte + letra_sobrenome + numeros


def cadastrar_eleitor():
    """Coleta os dados e realiza o cadastro de um novo eleitor no sistema.

    Solicita nome, CPF, título de eleitor e flag de mesário, gera a chave
    de acesso automaticamente e persiste o registro no banco. Impede
    duplicidade verificando CPF e título antes de inserir.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== CADASTRO DE ELEITOR ===")

    nome = input("Digite o nome: ").strip()
    cpf = solicitar_cpf()
    titulo = solicitar_titulo()
    mesario = input("É mesário? (s/n): ").strip().lower()
    chave = gerar_chave_acesso(nome)

    if not nome:
        print("Erro: Todos os campos são obrigatórios!")
        return

    if mesario not in ["s", "n"]:
        print("Erro: Digite apenas 's' ou 'n'")
        return

    # Bloqueia cadastro duplicado por CPF ou título
    if buscar_por_cpf_ou_titulo(cpf, titulo):
        print("Erro: Eleitor já cadastrado!")
        return

    mesario_bool = mesario == "s"
    sucesso = inserir_eleitor(nome, cpf, titulo, mesario_bool, chave)

    if sucesso:
        print("Eleitor cadastrado com sucesso!")
        print(f"Sua chave de acesso é: {chave}")
        print("Guarde essa chave com segurança!")
    else:
        print("Erro ao cadastrar.")


def buscar_eleitor():
    """Busca e exibe os dados de um eleitor a partir do título de eleitor.

    Solicita o título ao usuário e exibe nome, título, CPF e status de
    voto caso o eleitor seja encontrado no banco.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== BUSCAR ELEITOR ===")

    titulo = input("Digite o título do eleitor: ").strip()
    eleitor = buscar_por_titulo(titulo)

    if eleitor:
        print("\nEleitor encontrado:")
        print(f"Nome: {eleitor['nome_completo']}")
        print(f"Título: {eleitor['titulo_eleitor']}")
        print(f"CPF: {eleitor['cpf']}")
        print(f"Status: {eleitor['status_voto']}")
    else:
        print("Eleitor não encontrado.")


def listar_eleitores():
    """Lista todos os eleitores cadastrados no sistema.

    Recupera e exibe nome, título, CPF, flag de mesário e status de voto
    de cada eleitor registrado. Informa caso não haja registros.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== LISTA DE ELEITORES ===")

    eleitores = listar_todos()

    if eleitores:
        for e in eleitores:
            print("\n----------")
            print(f"Nome: {e['nome_completo']}")
            print(f"Título: {e['titulo_eleitor']}")
            print(f"CPF: {e['cpf']}")
            print(f"Mesário: {'Sim' if e['mesario'] else 'Não'}")
            print(f"Status: {e['status_voto']}")
    else:
        print("Nenhum eleitor cadastrado.")


def editar_eleitor():
    """Edita os dados cadastrais de um eleitor existente.

    Localiza o eleitor pelo título, exibe os valores atuais e permite
    atualizar nome, CPF e flag de mesário. Campos deixados em branco
    mantêm o valor original. Valida o novo CPF antes de salvar.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== EDITAR ELEITOR ===")

    titulo = input("Digite o título: ").strip()
    eleitor = buscar_por_titulo(titulo)

    if not eleitor:
        print("Eleitor não encontrado.")
        return

    print("\nDeixe em branco para manter o valor atual.\n")

    novo_nome = input(f"Nome ({eleitor['nome_completo']}): ").strip()
    novo_cpf = input(f"CPF ({eleitor['cpf']}): ").strip()
    mesario_atual = 's' if eleitor['mesario'] else 'n'
    novo_mesario = input(f"É mesário? (s/n) [{mesario_atual}]: ").strip().lower()

    if novo_mesario and novo_mesario not in ["s", "n"]:
        print("Erro: use apenas 's' ou 'n'")
        return

    # Valida o CPF apenas se um novo valor foi informado
    if novo_cpf and not validar_cpf(novo_cpf):
        print("Erro: CPF inválido!")
        return

    # Preserva o valor anterior quando o campo for deixado em branco
    nome_final = novo_nome if novo_nome else eleitor['nome_completo']
    cpf_final = novo_cpf if novo_cpf else eleitor['cpf']
    mesario_final = (novo_mesario == "s") if novo_mesario else eleitor['mesario']

    sucesso = atualizar_eleitor(nome_final, cpf_final, mesario_final, titulo)

    if sucesso:
        print("Eleitor atualizado com sucesso!")
    else:
        print("Erro ao atualizar.")


def remover_eleitor():
    """Remove o cadastro de um eleitor após confirmação do usuário.

    Localiza o eleitor pelo título, exibe o nome para confirmação e
    realiza a exclusão somente após resposta afirmativa.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== REMOVER ELEITOR ===")

    titulo = input("Digite o título: ").strip()
    eleitor = buscar_por_titulo(titulo)

    if not eleitor:
        print("Eleitor não encontrado.")
        return

    confirm = input(f"Tem certeza que deseja remover {eleitor['nome_completo']}? (s/n): ").lower()

    if confirm != "s":
        print("Operação cancelada.")
        return

    sucesso = remover_por_titulo(titulo)

    if sucesso:
        print("Eleitor removido com sucesso!")
    else:
        print("Erro ao remover.")