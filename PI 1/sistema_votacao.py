def sistema_votacao():
    while True:
        print("\n--- SISTEMA DE VOTAÇÃO ---")
        print("1 - Votar")
        print("2 - Encerrar votação")
        print("0 - Voltar")

        op = input("Escolha: ")
        if op == "1":
            print("Votando...")
        elif op == "2":
            print("Encerrando votação...")
        elif op == "0":
            break
        else:
            print("Opção inválida!")