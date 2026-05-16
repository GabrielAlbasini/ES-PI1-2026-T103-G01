CHAVE = [[3, 3],
         [2, 5]]

MOD = 26


def texto_para_numeros(texto):

    texto = texto.upper().replace(" ", "")

    return [ord(c) - ord('A') for c in texto if c.isalpha()]


def numeros_para_texto(numeros):

    return ''.join([chr(n + ord('A')) for n in numeros])


def ajustar_texto(texto):

    if len(texto) % 2 != 0:
        texto += 'X'

    return texto


def numero_para_letra(texto):

    resultado = ""

    for caractere in texto:

        if caractere.isdigit():
            resultado += chr(int(caractere) + 65)

        else:
            resultado += caractere.upper()

    return resultado


def letra_para_numero(texto):

    resultado = ""

    for caractere in texto:

        valor = ord(caractere.upper()) - 65

        if 0 <= valor <= 9:
            resultado += str(valor)

        else:
            resultado += caractere

    return resultado


def multiplicar_matriz(matriz, bloco):

    resultado = []

    for i in range(2):

        valor = (
            matriz[i][0] * bloco[0] +
            matriz[i][1] * bloco[1]
        ) % MOD

        resultado.append(valor)

    return resultado


def inversa_modular(numero):

    numero = numero % MOD

    for i in range(1, MOD):

        if (numero * i) % MOD == 1:
            return i

    return None


def inversa_modular_matriz(matriz):

    a = matriz[0][0]
    b = matriz[0][1]
    c = matriz[1][0]
    d = matriz[1][1]

    det = (a * d - b * c) % MOD

    det_inv = inversa_modular(det)

    adjunta = [[d, -b],
               [-c, a]]

    inversa = []

    for linha in adjunta:

        nova_linha = []

        for valor in linha:

            novo_valor = (det_inv * valor) % MOD

            nova_linha.append(novo_valor)

        inversa.append(nova_linha)

    return inversa


def criptografar_hill(texto):

    texto = numero_para_letra(texto)

    texto = ajustar_texto(texto)

    numeros = texto_para_numeros(texto)

    resultado = []

    for i in range(0, len(numeros), 2):

        bloco = [numeros[i],
                 numeros[i + 1]]

        criptografado = multiplicar_matriz(CHAVE, bloco)

        resultado.extend(criptografado)

    return numeros_para_texto(resultado)


def descriptografar_hill(texto):

    numeros = texto_para_numeros(texto)

    chave_inversa = inversa_modular_matriz(CHAVE)

    resultado = []

    for i in range(0, len(numeros), 2):

        bloco = [numeros[i],
                 numeros[i + 1]]

        descriptografado = multiplicar_matriz(chave_inversa, bloco)

        resultado.extend(descriptografado)

    texto_final = numeros_para_texto(resultado)

    texto_final = letra_para_numero(texto_final)

    return texto_final


cpf = "12345678901"

cpf_criptografado = criptografar_hill(cpf)

print("CPF Original:", cpf)
print("CPF Criptografado:", cpf_criptografado)

cpf_descriptografado = descriptografar_hill(cpf_criptografado)

print("CPF Descriptografado:", cpf_descriptografado)