
def menu_eleitor():
     while True:
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
            print("Voltando ao menu de gerenciamento.")
            break