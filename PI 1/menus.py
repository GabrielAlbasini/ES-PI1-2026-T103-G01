from eleitor import (
    cadastrar_eleitor,
    buscar_eleitor,
    listar_eleitores,
    editar_eleitor,
    remover_eleitor
)
from voto import (
    iniciar_votacao,
    registrar_voto,
    encerrar_votacao
)
import voto
from auditoria import (
    exibir_logs,
    exibir_protocolos
)
from resultadoVotacao import (
    boletim_urna,
    estatisticas_comparecimento,
    votos_por_partido,
    validacao_integridade
)


def menu_eleitor():
    """Exibe e gerencia o submenu de operações relacionadas a eleitores.

    Permite cadastrar, buscar, listar, editar e remover eleitores.
    O loop permanece ativo até o usuário escolher a opção de voltar.

    Args:
        Nenhum.

    Returns:
        None
    """
    opcao = ""
    while opcao != "0":
        print("\n=== ELEITOR ===")
        print("1 - Cadastrar eleitor")
        print("2 - Buscar eleitor")
        print("3 - Listar eleitores")
        print("4 - Editar eleitor")
        print("5 - Remover eleitor")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_eleitor()
        elif opcao == '2':
            buscar_eleitor()
        elif opcao == '3':
            listar_eleitores()
        elif opcao == '4':
            editar_eleitor()
        elif opcao == '5':
            remover_eleitor()
        elif opcao == '0':
            print("Voltando...")


def menu_gerenciamento():
    """Exibe e gerencia o submenu de gerenciamento do sistema.

    Agrupa as opções administrativas do sistema, atualmente dando acesso
    ao submenu de eleitores. O loop permanece ativo até o usuário voltar.

    Args:
        Nenhum.

    Returns:
        None
    """
    opcao = ""
    while opcao != "0":
        print("\n=== GERENCIAMENTO ===")
        print("1 - Eleitor")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_eleitor()
        elif opcao == '0':
            print("Voltando...")
        else:
            print("Opção inválida.")


def menu_auditoria():
    """Exibe e gerencia o submenu de auditoria do sistema.

    Permite visualizar os logs de eventos e os protocolos de votação
    registrados. O loop permanece ativo até o usuário escolher voltar.

    Args:
        Nenhum.

    Returns:
        None
    """
    opcao = ""
    while opcao != "0":
        print("\n=== AUDITORIA ===")
        print("1 - Ver logs")
        print("2 - Ver protocolos")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            exibir_logs()
        elif opcao == "2":
            exibir_protocolos()
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def menu_resultados():
    """Exibe e gerencia o submenu de resultados da eleição.

    Dá acesso ao boletim de urna, estatísticas de comparecimento,
    votos por partido e validação de integridade dos dados.

    Args:
        Nenhum.

    Returns:
        None
    """
    opcao = ""
    while opcao != "0":
        print("\n=== RESULTADOS ===")
        print("1 - Boletim de urna")
        print("2 - Estatísticas")
        print("3 - Votos por partido")
        print("4 - Validação de integridade")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            boletim_urna()
        elif opcao == "2":
            estatisticas_comparecimento()
        elif opcao == "3":
            votos_por_partido()
        elif opcao == "4":
            validacao_integridade()
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def sistema_votacao():
    """Gerencia o fluxo da sessão de votação conforme o estado atual.

    Exibe opções dinâmicas de acordo com o estado global da votação:
    quando fechada, permite apenas iniciar; quando aberta, permite votar
    ou encerrar. Impede ações incompatíveis com o estado vigente.

    Args:
        Nenhum.

    Returns:
        None
    """
    opcao = ""
    while opcao != "0":
        print("\n=== SISTEMA DE VOTAÇÃO ===")

        # Opções mudam conforme a votação está aberta ou fechada
        if not voto.votacao_aberta:
            print("1 - Iniciar votação")
            print("0 - Voltar")
        else:
            print("2 - Votar")
            print("3 - Encerrar votação")
            print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            if not voto.votacao_aberta:
                iniciar_votacao()
            else:
                print("A votação já está em andamento.")
        elif opcao == "2":
            if voto.votacao_aberta:
                registrar_voto()
            else:
                print("Opção inválida!")
        elif opcao == "3":
            if voto.votacao_aberta:
                encerrar_votacao()
            else:
                print("Opção inválida!")
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def menu_votacao():
    """Exibe e gerencia o submenu principal de votação.

    Centraliza o acesso ao sistema de votação, à auditoria e aos
    resultados. O loop permanece ativo até o usuário escolher voltar.

    Args:
        Nenhum.

    Returns:
        None
    """
    opcao = ""
    while opcao != "0":
        print("\n=== MENU DE VOTAÇÃO ===")
        print("1 - Abrir sistema de votação")
        print("2 - Auditoria")
        print("3 - Resultados")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            sistema_votacao()
        elif opcao == "2":
            menu_auditoria()
        elif opcao == "3":
            menu_resultados()
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def menu_principal():
    """Exibe e gerencia o menu principal do sistema de votação.

    Ponto de entrada da interface do usuário. Direciona para o módulo
    de gerenciamento ou de votação conforme a escolha, encerrando o
    sistema quando o usuário seleciona a opção de sair.

    Args:
        Nenhum.

    Returns:
        None
    """
    opcao = ""
    while opcao != "0":
        print("\n=== SISTEMA DE VOTAÇÃO ===")
        print("1 - Gerenciamento")
        print("2 - Votação")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_gerenciamento()
        elif opcao == '2':
            menu_votacao()
        elif opcao == '0':
            print("Saindo do sistema. Até logo!")
        else:
            print("Opção inválida.")