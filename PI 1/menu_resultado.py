def menu_resultados():
    while True:
        print("\n--- RESULTADOS ---")
        print("1 - Boletim de urna")
        print("2 - Estatísticas")
        print("3 - Votos por partido")
        print("4 - Validação de integridade")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            print("Boletim de urna...")
        elif op == "2":
            print("Estatísticas...")
        elif op == "3":
            print("Votos por partido...")
        elif op == "4":
            print("Validação de integridade...")
        elif op == "0":
            break
        else:
            print("Opção inválida!")