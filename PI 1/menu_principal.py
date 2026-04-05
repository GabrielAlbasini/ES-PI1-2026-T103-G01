from menu_gerenciamento import menu_gerenciamento
from menu_votacao import menu_votacao    
def menu_principal():
    while True:
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
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

        
