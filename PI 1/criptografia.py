import numpy as np

CHAVE = np.array([[3, 3],
                  [2, 5]])

MOD = 26


def texto_para_numeros(texto):
    """
    Converte texto em números (A=0, B=1, ..., Z=25).

    Args:
        texto (str): Texto a ser convertido.

    Returns:
        list[int]: Lista de números correspondentes.
    """
    texto = texto.upper().replace(" ", "")
    return [ord(c) - ord('A') for c in texto if c.isalpha()]


def numeros_para_texto(numeros):
    """
    Converte números em texto (0=A, 1=B, ..., 25=Z).

    Args:
        numeros (list[int]): Lista de números.

    Returns:
        str: Texto convertido.
    """
    return ''.join([chr(n + ord('A')) for n in numeros])


def ajustar_texto(texto):
    """
    Ajusta o texto para ter tamanho par.

    Args:
        texto (str): Texto original.

    Returns:
        str: Texto ajustado.
    """
    if len(texto) % 2 != 0:
        texto += 'X'
    return texto


def numero_para_letra(texto):
    """
    Converte números em letras (0=A, ..., 9=J).

    Args:
        texto (str): Texto numérico.

    Returns:
        str: Texto convertido.
    """
    return ''.join([chr(int(d) + 65) for d in texto if d.isdigit()])


def letra_para_numero(texto):
    """
    Converte letras em números (A=0, ..., J=9).

    Args:
        texto (str): Texto em letras.

    Returns:
        str: Texto numérico.
    """
    return ''.join([str(ord(c) - 65) for c in texto])


def criptografar_hill(texto):
    """
    Criptografa um texto usando a Cifra de Hill.

    Args:
        texto (str): Texto original.

    Returns:
        str: Texto criptografado.
    """
    texto = ajustar_texto(texto)
    numeros = texto_para_numeros(texto)
    resultado = []

    for i in range(0, len(numeros), 2):
        bloco = np.array([[numeros[i]],
                          [numeros[i + 1]]])

        criptografado = np.dot(CHAVE, bloco) % MOD
        resultado.extend(criptografado.flatten())

    return numeros_para_texto(resultado)


def inversa_modular_matriz(matriz):
    """
    Calcula a inversa modular da matriz 2x2 no módulo 26.

    Args:
        matriz (np.array): Matriz chave.

    Returns:
        np.array: Matriz inversa modular.
    """
    det = int(np.round(np.linalg.det(matriz)))
    det_mod = det % MOD

    for i in range(1, MOD):
        if (det_mod * i) % MOD == 1:
            det_inv = i
            break

    adj = np.array([[matriz[1][1], -matriz[0][1]],
                    [-matriz[1][0], matriz[0][0]]])

    return (det_inv * adj) % MOD


def descriptografar_hill(texto):
    """
    Descriptografa um texto usando a Cifra de Hill.

    Args:
        texto (str): Texto criptografado.

    Returns:
        str: Texto original.
    """
    numeros = texto_para_numeros(texto)
    chave_inv = inversa_modular_matriz(CHAVE)
    resultado = []

    for i in range(0, len(numeros), 2):
        bloco = np.array([[numeros[i]],
                          [numeros[i + 1]]])

        descriptografado = np.dot(chave_inv, bloco) % MOD
        resultado.extend(descriptografado.flatten())

    return numeros_para_texto(resultado)