from db import conn, cursor
from validacoes import validar_cpf, validar_titulo_eleitor
import mysql.connector

def cadastrar_eleitor():
    # Função para cadastrar um novo eleitor no sistema
    print("\n--- CADASTRO DE ELEITOR ---")
    
    nome = input("Digite o nome: ").strip()
    titulo = input("Digite o título de eleitor: ").strip()
    cpf = input("Digite o CPF: ").strip()
    mesario = input("É mesário? (s/n): ").strip().lower()
    chave = input("Digite a chave de acesso: ").strip()
    # Validação dos campos obrigatórios
    if not nome or not titulo or not cpf or not chave: 
        print("Erro: Todos os campos são obrigatórios!")
        return
    # Validação do campo mesário
    if mesario not in ["s", "n"]:
        print("Erro: Digite apenas 's' ou 'n' para mesário!")
        return
    # Validação do CPF e do título de eleitor
    if not validar_cpf(cpf):
        print("Erro: CPF inválido!")
        return

    if not validar_titulo_eleitor(titulo):
        print("Erro: Título de eleitor inválido!")
        return
    # Verificação de duplicidade de CPF ou título de eleitor
    try:
        cursor.execute(
            "SELECT * FROM eleitor WHERE cpf = %s OR titulo_eleitor = %s",    
            (cpf, titulo)
        )
        if cursor.fetchone():
            print("Erro: Eleitor já cadastrado!")
            return
    # Conversão do campo mesário para booleano
        mesario_bool = mesario == "s"
    # Inserção do novo eleitor no banco de dados
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
    #Busca um eleitor pelo título de eleitor e exibe suas informações
    titulo = input("Digite o título do eleitor: ").strip()
    
    cursor.execute("SELECT * FROM eleitor WHERE titulo_eleitor = %s", (titulo,))
    eleitor = cursor.fetchone()
    # Exibe as informações do eleitor encontrado ou uma mensagem de erro caso não seja encontrado
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

        print("\nDeixe em branco para manter o valor atual.\n")

        novo_nome = input(f"Nome ({eleitor['nome_completo']}): ").strip()
        novo_cpf = input(f"CPF ({eleitor['cpf']}): ").strip()
        mesario_atual = 's' if eleitor['mesario'] else 'n'
        novo_mesario = input(f"É mesário? (s/n) [{mesario_atual}]: ").strip().lower()

        # VALIDAÇÃO MESÁRIO 
        if novo_mesario and novo_mesario not in ["s", "n"]:
            print("Erro: use apenas 's' ou 'n' para mesário!")
            return
      
        # CPF válido só se foi digitado e for diferente do valor atual 
        if novo_cpf:
            if not validar_cpf(novo_cpf):
                print("Erro: CPF inválido!")
                return

            cursor.execute(
                "SELECT * FROM eleitor WHERE cpf = %s AND titulo_eleitor != %s",
                (novo_cpf, titulo)
            )

            if cursor.fetchone():
                print("Erro: CPF já está sendo usado por outro eleitor!")
                return

        # valores finais 
        nome = novo_nome if novo_nome else eleitor['nome_completo']
        cpf_final = novo_cpf if novo_cpf else eleitor['cpf']
        if novo_mesario:
            mesario_final = novo_mesario == 's'
        else:
            mesario_final = eleitor['mesario']
        

        sql = """
        UPDATE eleitor
        SET nome_completo = %s,
            cpf = %s,
            mesario = %s
        WHERE titulo_eleitor = %s
        """

        cursor.execute(sql, (nome, cpf_final, mesario_final, titulo))
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
