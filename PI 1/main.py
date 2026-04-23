import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lobo2404$",
    database="sistema_votacao"
)

cursor = conn.cursor(dictionary=True)

def validar_cpf(cpf): #Valida se um CPF é matematicamente correto.
    
    cpf = cpf.replace(".", "").replace("-", "").strip() # Remove caracteres especiais caso existam

    if len(cpf) != 11 or not cpf.isdigit():  # Verifica se tem 11 dígitos e se todos são numéricos
        return False
    if cpf == cpf[0] * 11: # Rejeita CPFs com todos os dígitos iguais
        return False
    #Cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)

    resto = soma % 11

    if resto < 2:
        primeiro_dv = 0
    else:
        primeiro_dv = 11 - resto
    
    if primeiro_dv != int(cpf[9]): # Verifica se o primeiro dígito verificador calculado bate com o do CPF informado
        return False
    #Cálculo do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)

    resto = soma % 11

    if resto < 2:
        segundo_dv = 0
    else:
        segundo_dv = 11 - resto

    if segundo_dv != int(cpf[10]): # Verifica se o segundo dígito verificador calculado bate com o do CPF informado
        return False

    return True
#Valida se um Título de Eleitor é matematicamente correto.
def validar_titulo_eleitor(titulo):

    titulo = titulo.strip()

    if len(titulo) != 12 or not titulo.isdigit(): # Verifica se tem 12 dígitos e se são todos numéricos
        return False

    # Separação das partes do título de eleitor
    sequencial = titulo[:8]   # Pega os 8 primeiros dígitos
    uf = titulo[8:10]         # Pega os dígitos 9º e 10º(código da UF)
    dv1_informado = int(titulo[10])  # Pega o dígito 11º(primeiro DV)
    dv2_informado = int(titulo[11])  # Pega o dígito 12º(segundo DV)

    codigo_uf = int(uf)

    if codigo_uf < 1 or codigo_uf > 28: # Verifica se o código da UF é válido (01 a 28)
        return False

    # --- Cálculo do primeiro dígito verificador ---
    pesos_dv1 = [2, 3, 4, 5, 6, 7, 8, 9]
    soma = 0
    for i in range(8):
        soma += int(sequencial[i]) * pesos_dv1[i]

    resto = soma % 11

    if resto == 0 and codigo_uf in (1, 2): # SP (01) e MG (02): se resto for 0, DV1 = 1
        primeiro_dv = 1
    
    elif resto == 10: # Para todos: se resto for 10, DV1 = 0
        primeiro_dv = 0
    else:
        primeiro_dv = resto

    if primeiro_dv != dv1_informado:
        return False

    # --- Cálculo do segundo dígito verificador ---
    pesos_dv2 = [7, 8, 9]
    valores_dv2 = [int(uf[0]), int(uf[1]), primeiro_dv] # Usa os dois dígitos da UF e o primeiro DV calculado

    soma = 0
    
    for i in range(3):
        soma += valores_dv2[i] * pesos_dv2[i]

    resto = soma % 11

    if resto == 0 and codigo_uf in (1, 2): # SP (01) e MG (02): se resto for 0, DV2 = 1
        segundo_dv = 1
    elif resto == 10: # Para todos: se resto for 10, DV2 = 0
        segundo_dv = 0
    else:
        segundo_dv = resto

    if segundo_dv != dv2_informado:
        return False
    
    return True

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
if __name__ == "__main__":
    main() 
