from auditoria import registrar
from validações import validar_cpf, validar_titulo_eleitor
from db import (
    inserir_eleitor,
    buscar_por_titulo,
    buscar_por_cpf_ou_titulo,
    listar_todos,
    atualizar_eleitor,
    remover_por_titulo
)

import secrets
import string


# GERAR CHAVE DE ACESSO

def gerar_chave_acesso(nome):
    partes = nome.strip().split()

    if len(partes) < 2:
        raise ValueError("Digite nome e sobrenome.")

    primeira_parte = partes[0][:2].upper()   # 2 letras do nome
    letra_sobrenome = partes[1][0].upper()   # 1 letra do sobrenome
    numeros = ''.join(secrets.choice(string.digits) for _ in range(4))  # 4 números

    return primeira_parte + letra_sobrenome + numeros


# CADASTRAR

def cadastrar_eleitor():
    print("\n--- CADASTRO DE ELEITOR ---")
    
    nome = input("Digite o nome: ").strip()
    titulo = input("Digite o título de eleitor: ").strip()
    cpf = input("Digite o CPF: ").strip()
    mesario = input("É mesário? (s/n): ").strip().lower()

    if not nome or not titulo or not cpf:
        registrar("Erro cadastro: campos obrigatórios não preenchidos")
        print("Erro: Todos os campos são obrigatórios!")
        return

    if mesario not in ["s", "n"]:
        print("Erro: Digite apenas 's' ou 'n'")
        return

    if not validar_cpf(cpf):
        registrar(f"Erro cadastro: CPF inválido ({cpf})")
        print("Erro: CPF inválido!")
        return

    if not validar_titulo_eleitor(titulo):
        registrar(f"Erro cadastro: Título inválido ({titulo})")
        print("Erro: Título inválido!")
        return

    if buscar_por_cpf_ou_titulo(cpf, titulo):
        registrar(f"Tentativa de cadastro duplicado - título {titulo}")
        print("Erro: Eleitor já cadastrado!")
        return

    try:
        chave = gerar_chave_acesso(nome)
    except ValueError as e:
        print(e)
        return

    mesario_bool = mesario == "s"

    sucesso = inserir_eleitor(nome, cpf, titulo, mesario_bool, chave)

    if sucesso:
        registrar(f"Eleitor cadastrado: {nome} - título {titulo}")
        print("\nEleitor cadastrado com sucesso!")
        print(f"Sua chave de acesso é: {chave}")
        print("Guarde essa chave com segurança!")
    else:
        registrar(f"Erro ao cadastrar eleitor: {nome}")
        print("Erro ao cadastrar.")


# BUSCAR

def buscar_eleitor():
    print("\n--- BUSCAR ELEITOR ---")

    titulo = input("Digite o título do eleitor: ").strip()

    eleitor = buscar_por_titulo(titulo)

    if eleitor:
        registrar(f"Consulta de eleitor: {titulo}")
        print("\nEleitor encontrado:")
        print(f"Nome: {eleitor['nome_completo']}")
        print(f"Título: {eleitor['titulo_eleitor']}")
        print(f"CPF: {eleitor['cpf']}")
        print(f"Status: {eleitor['status_voto']}")
    else:
        registrar(f"Consulta falha: {titulo}")
        print("Eleitor não encontrado.")


# LISTAR
def listar_eleitores():
    print("\n--- LISTA DE ELEITORES ---")

    eleitores = listar_todos()

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


# EDITAR

def editar_eleitor():
    print("\n- EDITAR ELEITOR -")

    titulo = input("Digite o título: ").strip()

    eleitor = buscar_por_titulo(titulo)

    if not eleitor:
        registrar(f"Tentativa de edição em eleitor inexistente: {titulo}")
        print("Eleitor não encontrado.")
        return

    print("\nDeixe em branco para manter o valor atual.\n")

    novo_nome = input(f"Nome ({eleitor['nome_completo']}): ").strip()
    novo_cpf = input(f"CPF ({eleitor['cpf']}): ").strip()
    mesario_atual = 's' if eleitor['mesario'] else 'n'
    novo_mesario = input(f"É mesário? (s/n) [{mesario_atual}]: ").strip().lower()

    if novo_mesario and novo_mesario not in ["s", "n"]:
        print("Erro: use apenas 's' ou 'n'")
        return

    if novo_cpf and not validar_cpf(novo_cpf):
        print("Erro: CPF inválido!")
        return

    nome_final = novo_nome if novo_nome else eleitor['nome_completo']
    cpf_final = novo_cpf if novo_cpf else eleitor['cpf']
    mesario_final = (novo_mesario == "s") if novo_mesario else eleitor['mesario']

    sucesso = atualizar_eleitor(nome_final, cpf_final, mesario_final, titulo)

    if sucesso:
        registrar(f"Eleitor atualizado: {titulo}")
        print("Eleitor atualizado com sucesso!")
    else:
        registrar(f"Erro ao atualizar eleitor: {titulo}")
        print("Erro ao atualizar.")


# REMOVER

def remover_eleitor():
    print("\n--- REMOVER ELEITOR ---")

    titulo = input("Digite o título: ").strip()

    eleitor = buscar_por_titulo(titulo)

    if not eleitor:
        registrar(f"Tentativa de remoção de eleitor inexistente: {titulo}")
        print("Eleitor não encontrado.")
        return

    confirm = input(f"Tem certeza que deseja remover {eleitor['nome_completo']}? (s/n): ").lower()

    if confirm != "s":
        registrar(f"Remoção cancelada: {titulo}")
        print("Operação cancelada.")
        return

    sucesso = remover_por_titulo(titulo)

    if sucesso:
        registrar(f"Eleitor removido: {titulo}")
        print("Eleitor removido com sucesso!")
    else:
        registrar(f"Erro ao remover eleitor: {titulo}")
        print("Erro ao remover.")