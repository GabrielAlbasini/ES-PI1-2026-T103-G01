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


# MENU ELEITOR

def menu_eleitor():

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


# MENU GERENCIAMENTO

def menu_gerenciamento():

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


# MENU AUDITORIA

def menu_auditoria():

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


# MENU RESULTADOS

def menu_resultados():

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


# SISTEMA DE VOTAÇÃO

def sistema_votacao():

    opcao = ""

    while opcao != "0":

        print("\n=== SISTEMA DE VOTAÇÃO ===")

        # Exibe opções conforme status da votação
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


# MENU VOTAÇÃO

def menu_votacao():

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


# MENU PRINCIPAL

def menu_principal():

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