from eleitor import (
    cadastrar_eleitor,
    buscar_eleitor,
    listar_eleitores,
    editar_eleitor,
    remover_eleitor
)

def menu_eleitor():
    opcao = ""
    while opcao != "0":
        print("\n--- ELEITOR ---")
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


def menu_candidato():
    opcao = ""
    while opcao != "0":
        print("\n--- CANDIDATO ---")
        print("1 - Cadastrar candidato")
        print("2 - Buscar candidato")
        print("3 - Listar candidatos")
        print("4 - Editar candidato")
        print("5 - Remover candidato")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_candidato()
        elif opcao == "2":
            buscar_candidato()
        elif opcao == "3":
            listar_candidatos()
        elif opcao == "4":
            editar_candidato()
        elif opcao == "5":
            remover_candidato()
        elif opcao == "0":
            print("Voltando...")


def menu_gerenciamento():
    opcao = ""
    while opcao != "0":
        print("\n===== GERENCIAMENTO =====")
        print("1 - Eleitor")
        print("2 - Candidato")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_eleitor()
        elif opcao == '2':
            menu_candidato()
        elif opcao == '0':
            print("Voltando...")
        else:
            print("Opção inválida.")


def menu_auditoria():
    opcao = ""
    while opcao != "0":
        print("\n--- AUDITORIA ---")
        print("1 - Ver logs")
        print("2 - Ver protocolos")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            print("Exibindo logs...")
        elif opcao == "2":
            print("Exibindo protocolos...")
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def menu_resultados():
    opcao = ""
    while opcao != "0":
        print("\n--- RESULTADOS ---")
        print("1 - Boletim de urna")
        print("2 - Estatísticas")
        print("3 - Votos por partido")
        print("4 - Validação de integridade")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            print("Boletim de urna...")
        elif opcao == "2":
            print("Estatísticas...")
        elif opcao == "3":
            print("Votos por partido...")
        elif opcao == "4":
            print("Validação de integridade...")
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")

def sistema_votacao():
    opcao = ""
    while opcao != "0":
        print("\n--- SISTEMA DE VOTAÇÃO ---")
        print("1 - Votar")
        print("2 - Encerrar votação")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            print("Votando...")
        elif opcao == "2":
            print("Encerrando votação...")
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def menu_votacao():
    opcao = ""
    while opcao != "0":
        print("\n--- MENU DE VOTAÇÃO ---")
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
    opcao = ""
    while opcao != "0":
        print("\n===== SISTEMA DE VOTAÇÃO =====")
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