CHAVE = [[3, 3],
         [2, 5]]

MOD = 26


# TEXTO PARA NÚMEROS

def texto_para_numeros(texto):

    texto = texto.upper()
    texto = texto.replace(" ", "")

    numeros = []

    for caractere in texto:

        if caractere.isalpha():

            numeros.append(
                ord(caractere) - ord('A')
            )

    return numeros


# NÚMEROS PARA TEXTO

def numeros_para_texto(numeros):

    resultado = ""

    for numero in numeros:

        resultado += chr(
            numero + ord('A')
        )

    return resultado


# AJUSTAR TEXTO

def ajustar_texto(texto):

    texto = texto.upper()
    texto = texto.replace(" ", "")

    # Completa bloco ímpar
    if len(texto) % 2 != 0:

        texto += "X"

    return texto


# CONVERTER NÚMEROS EM LETRAS

def numero_para_letra(texto):

    mapa = {
        "0": "ZA",
        "1": "ZB",
        "2": "ZC",
        "3": "ZD",
        "4": "ZE",
        "5": "ZF",
        "6": "ZG",
        "7": "ZH",
        "8": "ZI",
        "9": "ZJ"
    }

    resultado = ""

    for caractere in texto:

        if caractere.isdigit():

            resultado += mapa[
                caractere
            ]

        elif caractere.isalpha():

            resultado += (
                caractere.upper()
            )

    return resultado


# CONVERTER LETRAS EM NÚMEROS

def letra_para_numero(texto):

    mapa = {
        "ZA": "0",
        "ZB": "1",
        "ZC": "2",
        "ZD": "3",
        "ZE": "4",
        "ZF": "5",
        "ZG": "6",
        "ZH": "7",
        "ZI": "8",
        "ZJ": "9"
    }

    resultado = ""

    i = 0

    while i < len(texto):

        bloco = texto[i:i + 2]

        if bloco in mapa:

            resultado += mapa[
                bloco
            ]

            i += 2

        else:

            resultado += texto[i]

            i += 1

    return resultado


# MULTIPLICAÇÃO DE MATRIZ

def multiplicar_matriz(
    matriz,
    bloco
):

    resultado = []

    for i in range(2):

        valor = (
            matriz[i][0] *
            bloco[0] +

            matriz[i][1] *
            bloco[1]
        ) % MOD

        resultado.append(
            valor
        )

    return resultado


# INVERSA MODULAR

def inversa_modular(numero):

    numero = numero % MOD

    for i in range(1, MOD):

        if (
            numero * i
        ) % MOD == 1:

            return i

    return None


# INVERSA DA MATRIZ

def inversa_modular_matriz(
    matriz
):

    a = matriz[0][0]
    b = matriz[0][1]
    c = matriz[1][0]
    d = matriz[1][1]

    det = (
        a * d -
        b * c
    ) % MOD

    det_inv = (
        inversa_modular(det)
    )

    if det_inv is None:

        raise ValueError(
            "Matriz sem "
            "inversa modular."
        )

    adjunta = [
        [d, -b],
        [-c, a]
    ]

    inversa = []

    for linha in adjunta:

        nova_linha = []

        for valor in linha:

            novo_valor = (
                det_inv * valor
            ) % MOD

            nova_linha.append(
                novo_valor
            )

        inversa.append(
            nova_linha
        )

    return inversa


# CRIPTOGRAFAR TEXTO

def criptografar_hill(texto):

    if not texto:
        return ""

    texto = numero_para_letra(
        texto
    )

    texto = ajustar_texto(
        texto
    )

    numeros = texto_para_numeros(
        texto
    )

    resultado = []

    for i in range(
        0,
        len(numeros),
        2
    ):

        bloco = [
            numeros[i],
            numeros[i + 1]
        ]

        criptografado = (
            multiplicar_matriz(
                CHAVE,
                bloco
            )
        )

        resultado.extend(
            criptografado
        )

    return numeros_para_texto(
        resultado
    )


# DESCRIPTOGRAFAR TEXTO

def descriptografar_hill(texto):

    if not texto:
        return ""

    numeros = (
        texto_para_numeros(
            texto
        )
    )

    if len(numeros) % 2 != 0:

        return ""

    chave_inversa = (
        inversa_modular_matriz(
            CHAVE
        )
    )

    resultado = []

    for i in range(
        0,
        len(numeros),
        2
    ):

        bloco = [
            numeros[i],
            numeros[i + 1]
        ]

        descriptografado = (
            multiplicar_matriz(
                chave_inversa,
                bloco
            )
        )

        resultado.extend(
            descriptografado
        )

    texto_final = (
        numeros_para_texto(
            resultado
        )
    )

    texto_final = (
        letra_para_numero(
            texto_final
        )
    )

    # Remove caractere extra
    if texto_final.endswith("X"):

        texto_final = (
            texto_final[:-1]
        )

    return texto_final