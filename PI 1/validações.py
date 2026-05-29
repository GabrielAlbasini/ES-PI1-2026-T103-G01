# VALIDAÇÃO CPF

def validar_cpf(cpf):

    # Remove caracteres especiais
    cpf = cpf.replace(
        ".",
        ""
    ).replace(
        "-",
        ""
    ).strip()

    # Verifica tamanho e formato
    if len(cpf) != 11 or not cpf.isdigit():

        return False

    # Rejeita dígitos repetidos
    if cpf == cpf[0] * 11:

        return False

    # Primeiro dígito verificador
    soma = 0

    for i in range(9):

        soma += (
            int(cpf[i]) *
            (10 - i)
        )

    resto = soma % 11

    if resto < 2:

        primeiro_dv = 0

    else:

        primeiro_dv = 11 - resto

    if primeiro_dv != int(cpf[9]):

        return False

    # Segundo dígito verificador
    soma = 0

    for i in range(10):

        soma += (
            int(cpf[i]) *
            (11 - i)
        )

    resto = soma % 11

    if resto < 2:

        segundo_dv = 0

    else:

        segundo_dv = 11 - resto

    if segundo_dv != int(cpf[10]):

        return False

    return True


# VALIDAÇÃO TÍTULO

def validar_titulo_eleitor(titulo):

    titulo = titulo.strip()

    # Verifica tamanho e formato
    if len(titulo) != 12 or not titulo.isdigit():

        return False

    # Divide partes do título
    sequencial = titulo[:8]

    uf = titulo[8:10]

    dv1_informado = int(titulo[10])

    dv2_informado = int(titulo[11])

    codigo_uf = int(uf)

    # Verifica código da UF
    if codigo_uf < 1 or codigo_uf > 28:

        return False

    # Primeiro dígito verificador
    pesos_dv1 = [
        2, 3, 4, 5,
        6, 7, 8, 9
    ]

    soma = 0

    for i in range(8):

        soma += (
            int(sequencial[i]) *
            pesos_dv1[i]
        )

    resto = soma % 11

    if resto == 0 and codigo_uf in (1, 2):

        primeiro_dv = 1

    elif resto == 10:

        primeiro_dv = 0

    else:

        primeiro_dv = resto

    if primeiro_dv != dv1_informado:

        return False

    # Segundo dígito verificador
    pesos_dv2 = [7, 8, 9]

    valores_dv2 = [
        int(uf[0]),
        int(uf[1]),
        primeiro_dv
    ]

    soma = 0

    for i in range(3):

        soma += (
            valores_dv2[i] *
            pesos_dv2[i]
        )

    resto = soma % 11

    if resto == 0 and codigo_uf in (1, 2):

        segundo_dv = 1

    elif resto == 10:

        segundo_dv = 0

    else:

        segundo_dv = resto

    if segundo_dv != dv2_informado:

        return False

    return True


# SOLICITAR CPF

def solicitar_cpf():

    while True:

        cpf = input(
            "Digite o CPF: "
        ).strip()

        if validar_cpf(cpf):

            return cpf

        print(
            "CPF inválido! "
            "Digite novamente."
        )


# SOLICITAR CPF PARCIAL

def solicitar_cpf_parcial():

    while True:

        cpf = input(
            "Digite os 4 primeiros dígitos do CPF: "
        ).strip()

        if cpf.isdigit() and len(cpf) == 4:

            return cpf

        print(
            "Digite exatamente 4 números."
        )


# SOLICITAR TÍTULO

def solicitar_titulo():

    while True:

        titulo = input(
            "Digite o título de eleitor: "
        ).strip()

        if validar_titulo_eleitor(titulo):

            return titulo

        print(
            "Título de eleitor inválido! "
            "Digite novamente."
        )