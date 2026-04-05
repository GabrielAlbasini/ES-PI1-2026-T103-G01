from menu_auditoria import menu_auditoria
from menu_resultado import menu_resultados
from sistema_votacao import sistema_votacao 
def menu_votacao():
    while True:
        print("\n--- MENU DE VOTAÇÃO ---")
        print("1 - Abrir sistema de votação")
        print("2 - Auditoria")
        print("3 - Resultados")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            sistema_votacao()
        elif op == "2":
            menu_auditoria()
        elif op == "3":
            menu_resultados()
        elif op == "0":
            break
        else:
            print("Opção inválida!")