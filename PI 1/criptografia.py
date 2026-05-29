CHAVE = [[3, 3],
         [2, 5]]

MOD = 26


# TEXTO PARA NÚMEROS

def texto_para_numeros(texto):
    """
    Converte uma string de letras em uma lista de valores numéricos.

    Transforma cada caractere alfabético no seu índice correspondente
    no alfabeto (A=0, B=1, ..., Z=25). Espaços e caracteres não
    alfabéticos são ignorados.

    Args:
        texto (str): Texto a ser convertido, pode conter letras,
                     espaços e outros caracteres.

    Returns:
        list: Lista de inteiros representando cada letra do texto.
    """
    texto = texto.upper()
    texto = texto.replace(" ", "")
    numeros = []

    for caractere in texto:
        if caractere.isalpha():
            numeros.append(ord(caractere) - ord('A'))

    return numeros


# NÚMEROS PARA TEXTO

def numeros_para_texto(numeros):
    """
    Converte uma lista de valores numéricos de volta para uma string.

    Cada número é interpretado como índice do alfabeto e transformado
    na letra correspondente (0=A, 1=B, ..., 25=Z).

    Args:
        numeros (list): Lista de inteiros entre 0 e 25.

    Returns:
        str: String formada pelas letras correspondentes aos índices.
    """
    resultado = ""

    for numero in numeros:
        resultado += chr(numero + ord('A'))

    return resultado


# AJUSTAR TEXTO

def ajustar_texto(texto):
    """
    Prepara o texto para o processo de criptografia em blocos de 2.

    Remove espaços, converte para maiúsculas e, caso o número de
    caracteres seja ímpar, adiciona a letra 'X' ao final para
    completar o último bloco.

    Args:
        texto (str): Texto a ser ajustado antes da criptografia.

    Returns:
        str: Texto em maiúsculas, sem espaços e com comprimento par.
    """
    texto = texto.upper()
    texto = texto.replace(" ", "")

    # Completa bloco ímpar
    if len(texto) % 2 != 0:
        texto += "X"

    return texto


# CONVERTER NÚMEROS EM LETRAS

def numero_para_letra(texto):
    """
    Substitui dígitos numéricos por sequências de letras equivalentes.

    Utiliza um mapeamento fixo onde cada dígito (0-9) é substituído
    por um código de duas letras iniciado em 'Z' (ex: 0=ZA, 1=ZB).
    Letras presentes no texto são mantidas em maiúsculas.

    Args:
        texto (str): Texto contendo letras e/ou dígitos.

    Returns:
        str: Texto com todos os dígitos substituídos por seus
             respectivos códigos de letras.
    """
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
            resultado += mapa[caractere]
        elif caractere.isalpha():
            resultado += caractere.upper()

    return resultado


# CONVERTER LETRAS EM NÚMEROS

def letra_para_numero(texto):
    """
    Reverte os códigos de letras de volta para seus dígitos originais.

    Percorre o texto procurando sequências de duas letras que
    correspondam ao mapeamento inverso (ex: ZA=0, ZB=1). Caracteres
    que não formam código reconhecido são mantidos como estão.

    Args:
        texto (str): Texto com possíveis códigos de duas letras
                     gerados por numero_para_letra().

    Returns:
        str: Texto com os códigos substituídos pelos dígitos originais.
    """
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
            resultado += mapa[bloco]
            i += 2
        else:
            resultado += texto[i]
            i += 1

    return resultado


# MULTIPLICAÇÃO DE MATRIZ

def multiplicar_matriz(matriz, bloco):
    """
    Multiplica uma matriz 2x2 por um vetor de 2 elementos no módulo 26.

    Realiza a operação de multiplicação matricial entre a chave Hill
    e um bloco de dois números, aplicando módulo 26 ao resultado
    para manter os valores dentro do intervalo do alfabeto.

    Args:
        matriz (list): Matriz 2x2 representada como lista de listas
                       de inteiros.
        bloco (list): Lista com 2 inteiros representando o vetor
                      a ser multiplicado.

    Returns:
        list: Lista com 2 inteiros resultantes da multiplicação
              matricial com módulo 26 aplicado.
    """
    resultado = []

    for i in range(2):
        valor = (matriz[i][0] * bloco[0] + matriz[i][1] * bloco[1]) % MOD
        resultado.append(valor)

    return resultado


# INVERSA MODULAR

def inversa_modular(numero):
    """
    Calcula o inverso modular de um número inteiro no módulo 26.

    Busca um valor entre 1 e 25 tal que (numero * i) % 26 == 1.
    Caso nenhum valor satisfaça a condição, retorna None indicando
    que o inverso não existe.

    Args:
        numero (int): Número inteiro cujo inverso modular será
                      calculado.

    Returns:
        int: Inverso modular do número, ou None se não existir.
    """
    numero = numero % MOD

    for i in range(1, MOD):
        if (numero * i) % MOD == 1:
            return i

    return None


# INVERSA DA MATRIZ

def inversa_modular_matriz(matriz):
    """
    Calcula a matriz inversa modular de uma matriz 2x2 no módulo 26.

    Determina o determinante da matriz, calcula seu inverso modular
    e aplica a fórmula da adjunta para obter a inversa. Lança um
    erro caso a matriz não possua inversa modular válida.

    Args:
        matriz (list): Matriz 2x2 representada como lista de listas
                       de inteiros.

    Returns:
        list: Matriz 2x2 inversa no módulo 26, representada como
              lista de listas de inteiros.

    Raises:
        ValueError: Se o determinante da matriz não possuir inverso
                    modular no módulo 26.
    """
    a = matriz[0][0]
    b = matriz[0][1]
    c = matriz[1][0]
    d = matriz[1][1]

    det = (a * d - b * c) % MOD
    det_inv = inversa_modular(det)

    if det_inv is None:
        raise ValueError("Matriz sem inversa modular.")

    adjunta = [
        [d, -b],
        [-c, a]
    ]

    inversa = []

    for linha in adjunta:
        nova_linha = []
        for valor in linha:
            novo_valor = (det_inv * valor) % MOD
            nova_linha.append(novo_valor)
        inversa.append(nova_linha)

    return inversa


# CRIPTOGRAFAR TEXTO

def criptografar_hill(texto):
    """
    Criptografa um texto usando o algoritmo de cifra de Hill.

    Converte dígitos em letras, ajusta o tamanho do texto para
    blocos de 2, transforma os caracteres em números e aplica
    a multiplicação matricial com a chave definida em CHAVE.

    Args:
        texto (str): Texto original a ser criptografado, podendo
                     conter letras e dígitos.

    Returns:
        str: Texto criptografado em letras maiúsculas, ou string
             vazia se a entrada for vazia.
    """
    if not texto:
        return ""

    texto = numero_para_letra(texto)
    texto = ajustar_texto(texto)
    numeros = texto_para_numeros(texto)
    resultado = []

    for i in range(0, len(numeros), 2):
        bloco = [numeros[i], numeros[i + 1]]
        criptografado = multiplicar_matriz(CHAVE, bloco)
        resultado.extend(criptografado)

    return numeros_para_texto(resultado)


# DESCRIPTOGRAFAR TEXTO

def descriptografar_hill(texto):
    """
    Descriptografa um texto cifrado pelo algoritmo de Hill.

    Converte o texto cifrado em números, aplica a multiplicação
    pela matriz inversa da chave e reconverte o resultado em texto,
    revertendo também os códigos de letras para dígitos originais.

    Args:
        texto (str): Texto criptografado em letras maiúsculas,
                     gerado por criptografar_hill().

    Returns:
        str: Texto descriptografado original, ou string vazia
             se a entrada for vazia ou inválida.
    """
    if not texto:
        return ""

    numeros = texto_para_numeros(texto)

    if len(numeros) % 2 != 0:
        return ""

    chave_inversa = inversa_modular_matriz(CHAVE)
    resultado = []

    for i in range(0, len(numeros), 2):
        bloco = [numeros[i], numeros[i + 1]]
        descriptografado = multiplicar_matriz(chave_inversa, bloco)
        resultado.extend(descriptografado)

    texto_final = numeros_para_texto(resultado)
    texto_final = letra_para_numero(texto_final)

    # Remove caractere extra
    if texto_final.endswith("X"):
        texto_final = texto_final[:-1]

    return texto_final