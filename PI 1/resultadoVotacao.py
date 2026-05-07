from db import cursor


# =========================================
# BOLETIM DE URNA
# =========================================
def boletim_urna():

    print("\n===== BOLETIM DE URNA =====")

    try:
        cursor.execute("""
            SELECT
                c.nome,
                c.numero,
                c.partido,
                COUNT(v.id) AS total_votos
            FROM candidato c
            LEFT JOIN voto v
                ON c.id = v.id_candidato
            GROUP BY c.id
            ORDER BY c.nome ASC
        """)

        resultados = cursor.fetchall()

        if not resultados:
            print("Nenhum candidato cadastrado.")
            return

        maior_votacao = -1
        vencedor = None

        print("\n=========== RESULTADO ===========")

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

            if votos > maior_votacao:
                maior_votacao = votos
                vencedor = candidato

        if vencedor:
            print("\n===== VENCEDOR DA ELEIÇÃO =====")
            print(f"Nome: {vencedor['nome']}")
            print(f"Número: {vencedor['numero']}")
            print(f"Partido: {vencedor['partido']}")
            print(f"Total de votos: {vencedor['total_votos']}")

    except Exception as erro:
        print("Erro ao gerar boletim de urna:", erro)


