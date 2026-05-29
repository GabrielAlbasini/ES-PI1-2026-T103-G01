from db import (
    buscar_resultados_boletim,
    contar_eleitores,
    contar_eleitores_votaram,
    buscar_votos_por_partido,
    contar_votos
)


def boletim_urna():
    """Exibe o boletim de urna com os resultados da eleição.

    Recupera os dados de votação do banco, lista os votos de cada candidato,
    contabiliza votos nulos e identifica o candidato mais votado.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== BOLETIM DE URNA ===")
    try:
        resultados, total_nulos = buscar_resultados_boletim()
        if not resultados:
            print("Nenhum candidato cadastrado.")
            return

        maior_votacao = -1
        vencedor = None

        print("\n=== RESULTADO ===")
        for candidato in resultados:
            nome = candidato["nome"]
            numero = candidato["numero"]
            partido = candidato["partido"]
            votos = candidato["total_votos"]

            print(f"Candidato: {nome}")
            print(f"Número: {numero}")
            print(f"Partido: {partido}")
            print(f"Total de votos: {votos}")
            print("-" * 40)

            # Atualiza o vencedor sempre que encontrar uma votação maior
            if votos > maior_votacao:
                maior_votacao = votos
                vencedor = candidato

        print(f"Votos NULOS: {total_nulos}")
        print("-" * 40)

        if vencedor:
            print("\n=== VENCEDOR DA ELEIÇÃO ===")
            print(f"Nome: {vencedor['nome']}")
            print(f"Número: {vencedor['numero']}")
            print(f"Partido: {vencedor['partido']}")
            print(f"Total de votos: {vencedor['total_votos']}")

    except Exception as erro:
        print("Erro ao gerar boletim de urna:", erro)


def estatisticas_comparecimento():
    """Exibe as estatísticas de comparecimento eleitoral.

    Calcula e imprime o total de eleitores aptos, quantos compareceram,
    o número de abstenções e o percentual de participação.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== ESTATÍSTICAS DE COMPARECIMENTO ===")
    try:
        total_eleitores = contar_eleitores()
        total_votaram = contar_eleitores_votaram()
        abstencoes = total_eleitores - total_votaram

        # Evita divisão por zero caso não haja eleitores cadastrados
        percentual = 0
        if total_eleitores > 0:
            percentual = (total_votaram / total_eleitores) * 100

        print(f"Total de eleitores aptos: {total_eleitores}")
        print(f"Total de comparecimento: {total_votaram}")
        print(f"Total de abstenções: {abstencoes}")
        print(f"Percentual de comparecimento: {percentual:.2f}%")

    except Exception as erro:
        print("Erro ao gerar estatísticas:", erro)


def votos_por_partido():
    """Exibe o total de votos agrupados por partido político.

    Busca no banco os partidos e seus respectivos totais de votos,
    listando cada um com separador visual.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== VOTOS POR PARTIDO ===")
    try:
        partidos = buscar_votos_por_partido()
        if not partidos:
            print("Nenhum partido encontrado.")
            return

        for partido in partidos:
            print(f"Partido: {partido['partido']}")
            print(f"Total de votos: {partido['total_votos']}")
            print("-" * 35)

    except Exception as erro:
        print("Erro ao gerar votos por partido:", erro)


def validacao_integridade():
    """Verifica a integridade dos dados eleitorais registrados.

    Compara o total de votos gravados com o número de eleitores que
    possuem status JA_VOTOU. Se os valores forem iguais, a integridade
    é confirmada; caso contrário, uma falha é reportada.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== VALIDAÇÃO DE INTEGRIDADE ===")
    try:
        total_votos = contar_votos()
        total_eleitores_votaram = contar_eleitores_votaram()

        print(f"Total de votos registrados: {total_votos}")
        print(f"Total de eleitores com status JA_VOTOU: {total_eleitores_votaram}")
        print("\n=== RESULTADO DA VALIDAÇÃO ===")

        # Confronta os dois contadores para detectar inconsistências
        if total_votos == total_eleitores_votaram:
            print("INTEGRIDADE CONFIRMADA")
            print("Nenhuma inconsistência encontrada.")
        else:
            print("FALHA DE INTEGRIDADE DETECTADA")
            print("A quantidade de votos não corresponde aos eleitores que votaram.")

    except Exception as erro:
        print("Erro na validação de integridade:", erro)