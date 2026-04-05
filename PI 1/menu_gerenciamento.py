from menu_eleitor import menu_eleitor
from menu_candidato import menu_candidato
def menu_gerenciamento():
    while True:
        print("\n===== GERENCIAMENTO DE CANDIDATOS =====")
        print("1 - Eleitor")
        print("2 - Candidato")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            menu_eleitor()
           
        elif opcao == '2':
            menu_candidato()
           
        elif opcao == '0':
            print("Voltando ao menu principal.")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")