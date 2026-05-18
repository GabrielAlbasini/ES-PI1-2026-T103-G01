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

# =========================================
# ESTATÍSTICAS DE COMPARECIMENTO
# =========================================
def estatisticas_comparecimento():
 
    print("\n===== ESTATÍSTICAS DE COMPARECIMENTO =====")

    try:
        # Total de eleitores cadastrados
        cursor.execute("SELECT COUNT(*) AS total FROM eleitor")
        total_eleitores = cursor.fetchone()["total"]

        # Total de eleitores que votaram
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM eleitor
            WHERE status_voto = 'JA_VOTOU'
        """)

        total_votaram = cursor.fetchone()["total"]

        # Total de abstenções
        abstencoes = total_eleitores - total_votaram

        # Percentual
        percentual = 0

        if total_eleitores > 0:
            percentual = (total_votaram / total_eleitores) * 100

        print(f"Total de eleitores aptos: {total_eleitores}")
        print(f"Total de comparecimento: {total_votaram}")
        print(f"Total de abstenções: {abstencoes}")
        print(f"Percentual de comparecimento: {percentual:.2f}%")

    except Exception as erro:
        print("Erro ao gerar estatísticas:", erro)

# =========================================
# VOTOS POR PARTIDO
# =========================================
def votos_por_partido():

    print("\n===== VOTOS POR PARTIDO =====")

    try:
        cursor.execute("""
            SELECT
                c.partido,
                COUNT(v.id) AS total_votos
            FROM candidato c
            LEFT JOIN voto v
                ON c.id = v.id_candidato
            GROUP BY c.partido
            ORDER BY total_votos DESC
        """)

        partidos = cursor.fetchall()

        if not partidos:
            print("Nenhum partido encontrado.")
            return

        for partido in partidos:
            print(f"Partido: {partido['partido']}")
            print(f"Total de votos: {partido['total_votos']}")
            print("-" * 35)

    except Exception as erro:
        print("Erro ao gerar votos por partido:", erro)


# =========================================
# VALIDAÇÃO DE INTEGRIDADE
# =========================================
def validacao_integridade():
   

    print("\n===== VALIDAÇÃO DE INTEGRIDADE =====")

    try:
        # Total de votos registrados
        cursor.execute("SELECT COUNT(*) AS total FROM voto")
        total_votos = cursor.fetchone()["total"]

        # Total de eleitores que votaram
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM eleitor
            WHERE status_voto = 'JA_VOTOU'
        """)

        total_eleitores_votaram = cursor.fetchone()["total"]

        print(f"Total de votos registrados: {total_votos}")
        print(f"Total de eleitores com status JA_VOTOU: {total_eleitores_votaram}")

        print("\n===== RESULTADO DA VALIDAÇÃO =====")

        if total_votos == total_eleitores_votaram:
            print("INTEGRIDADE CONFIRMADA")
            print("Nenhuma inconsistência encontrada.")
        else:
            print("FALHA DE INTEGRIDADE DETECTADA")
            print("A quantidade de votos não corresponde aos eleitores que votaram.")

    except Exception as erro:
        print("Erro na validação de integridade:", erro)



