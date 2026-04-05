def menu_auditoria():
    while True:
        print("\n--- AUDITORIA ---")
        print("1 - Ver logs")
        print("2 - Ver protocolos")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            print("Exibindo logs...")
        elif op == "2":
            print("Exibindo protocolos...")
        elif op == "0":
            break
        else:
            print("Opção inválida!")