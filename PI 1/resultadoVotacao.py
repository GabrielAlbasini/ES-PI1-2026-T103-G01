from db import (
    buscar_resultados_boletim,
    contar_eleitores,
    contar_eleitores_votaram,
    buscar_votos_por_partido,
    contar_votos
)


# BOLETIM DE URNA

def boletim_urna():

    print("\n=== BOLETIM DE URNA ===")

    try:

        # Busca resultados e votos nulos
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

            # Define o candidato mais votado
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

        print(
            "Erro ao gerar boletim de urna:",
            erro
        )


# ESTATÍSTICAS

def estatisticas_comparecimento():

    print(
        "\n=== ESTATÍSTICAS DE COMPARECIMENTO ==="
    )

    try:

        total_eleitores = contar_eleitores()

        total_votaram = contar_eleitores_votaram()

        abstencoes = (
            total_eleitores -
            total_votaram
        )

        percentual = 0

        # Calcula percentual de comparecimento
        if total_eleitores > 0:

            percentual = (
                total_votaram /
                total_eleitores
            ) * 100

        print(
            f"Total de eleitores aptos: {total_eleitores}"
        )

        print(
            f"Total de comparecimento: {total_votaram}"
        )

        print(
            f"Total de abstenções: {abstencoes}"
        )

        print(
            f"Percentual de comparecimento: {percentual:.2f}%"
        )

    except Exception as erro:

        print(
            "Erro ao gerar estatísticas:",
            erro
        )


# VOTOS POR PARTIDO

def votos_por_partido():

    print(
        "\n=== VOTOS POR PARTIDO ==="
    )

    try:

        partidos = buscar_votos_por_partido()

        if not partidos:

            print("Nenhum partido encontrado.")
            return

        for partido in partidos:

            print(
                f"Partido: {partido['partido']}"
            )

            print(
                f"Total de votos: {partido['total_votos']}"
            )

            print("-" * 35)

    except Exception as erro:

        print(
            "Erro ao gerar votos por partido:",
            erro
        )


# VALIDAÇÃO DE INTEGRIDADE

def validacao_integridade():

    print(
        "\n=== VALIDAÇÃO DE INTEGRIDADE ==="
    )

    try:

        total_votos = contar_votos()

        total_eleitores_votaram = (
            contar_eleitores_votaram()
        )

        print(
            f"Total de votos registrados: {total_votos}"
        )

        print(
            f"Total de eleitores com status JA_VOTOU: "
            f"{total_eleitores_votaram}"
        )

        print(
            "\n=== RESULTADO DA VALIDAÇÃO ==="
        )

        # Compara votos e eleitores que votaram
        if total_votos == total_eleitores_votaram:

            print("INTEGRIDADE CONFIRMADA")

            print(
                "Nenhuma inconsistência encontrada."
            )

        else:

            print(
                "FALHA DE INTEGRIDADE DETECTADA"
            )

            print(
                "A quantidade de votos não corresponde "
                "aos eleitores que votaram."
            )

    except Exception as erro:

        print(
            "Erro na validação de integridade:",
            erro
        )