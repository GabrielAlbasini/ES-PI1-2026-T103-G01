def menu_candidato():
    while True:
        print("\n--- CANDIDATO ---")
        print("1 - Cadastrar candidato")
        print("2 - Buscar candidato")
        print("3 - Listar candidatos")
        print("4 - Editar candidato")
        print("5 - Remover candidato")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            cadastrar_candidato()
        elif op == "2":
            buscar_candidato()
        elif op == "3":
            listar_candidatos()
        elif op == "4":
            editar_candidato()
        elif op == "5":
            remover_candidato()
        elif op == "0":
            break
        else:
            print("Opção inválida!")