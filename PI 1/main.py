import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lobo2404$",
    database="sistema_votacao"
)

cursor = conn.cursor(dictionary=True)
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


def main():
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

def cadastrar_eleitor():
    print("\n--- CADASTRO DE ELEITOR ---")
    
    nome = input("Digite o nome: ").strip()
    titulo = input("Digite o título de eleitor: ").strip()
    cpf = input("Digite o CPF: ").strip()
    mesario = input("É mesário? (s/n): ").strip().lower()
    chave = input("Digite a chave de acesso: ").strip()

    if not nome or not titulo or not cpf or not chave:
        print("Erro: Todos os campos são obrigatórios!")
        return

    mesario_bool = True if mesario == "s" else False

    try:
        sql = """
        INSERT INTO eleitor 
        (nome_completo, cpf, titulo_eleitor, mesario, chave_acesso)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (nome, cpf, titulo, mesario_bool, chave)

        cursor.execute(sql, valores)
        conn.commit()

        print("Eleitor cadastrado com sucesso!")

    except mysql.connector.Error as err:
        print("Erro ao cadastrar:", err)

def buscar_eleitor():
    print("\n--- BUSCAR ELEITOR ---")

    titulo = input("Digite o título do eleitor: ").strip()

    cursor.execute("SELECT * FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
    eleitor = cursor.fetchone()

    if eleitor:
        print("\nEleitor encontrado:")
        print(f"Nome: {eleitor['nome_completo']}")
        print(f"Título: {eleitor['titulo_eleitor']}")
        print(f"CPF: {eleitor['cpf']}")
        print(f"Status: {eleitor['status_voto']}")
    else:
        print("Eleitor não encontrado.")

def listar_eleitores():
    print("\n--- LISTA DE ELEITORES ---")

    try:
        cursor.execute("SELECT * FROM eleitor")
        eleitores = cursor.fetchall()

        if eleitores:
            for e in eleitores:
                print("\n----------")
                print(f"Nome: {e['nome_completo']}")
                print(f"Título: {e['titulo_eleitor']}")
                print(f"CPF: {e['cpf']}")
                print(f"Mesário: {'Sim' if e['mesario'] else 'Não'}")
                print(f"Status: {e['status_voto']}")
        else:
            print("Nenhum eleitor cadastrado.")

    except mysql.connector.Error as err:
        print("Erro ao listar:", err)


def editar_eleitor():
    print("\n- EDITAR ELEITOR -")

    titulo = input("Digite o título do eleitor que deseja editar: ").strip()

    try:
        cursor.execute("SELECT * FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
        eleitor = cursor.fetchone()

        if not eleitor:
            print("Eleitor não encontrado.")
            return

        print("\n")

        novo_nome = input(f"Nome ({eleitor['nome_completo']}): ").strip()
        novo_cpf = input(f"CPF ({eleitor['cpf']}): ").strip()
        novo_mesario = input("É mesário? (s/n): ").strip().lower()

        nome = novo_nome if novo_nome else eleitor['nome_completo']
        cpf = novo_cpf if novo_cpf else eleitor['cpf']
        mesario = eleitor['mesario'] if novo_mesario == "" else (novo_mesario == 's')

        sql = """
        UPDATE eleitor
        SET nome_completo = %s, cpf = %s, mesario = %s
        WHERE titulo_eleitor = %s
        """

        cursor.execute(sql, (nome, cpf, mesario, titulo))
        conn.commit()

        print("Eleitor atualizado com sucesso!")

    except mysql.connector.Error as err:
        print("Erro ao editar:", err)


def remover_eleitor():
    print("\n--- REMOVER ELEITOR ---")

    titulo = input("Digite o título do eleitor: ").strip()

    try:
        cursor.execute("SELECT * FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
        eleitor = cursor.fetchone()

        if not eleitor:
            print("Eleitor não encontrado.")
            return

        confirm = input(f"Tem certeza que deseja remover {eleitor['nome_completo']}? (s/n): ").lower()

        if confirm == 's':
            cursor.execute("DELETE FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
            conn.commit()
            print("Eleitor removido com sucesso!")
        else:
            print("Operação cancelada.")

    except mysql.connector.Error as err:
        print("Erro ao remover:", err)
if __name__ == "__main__":
    main() 
