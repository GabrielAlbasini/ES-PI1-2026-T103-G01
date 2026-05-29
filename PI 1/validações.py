def validar_cpf(cpf):
    """Valida um número de CPF verificando formato e dígitos verificadores.

    Remove formatação, confere tamanho, rejeita sequências repetidas e
    recalcula os dois dígitos verificadores pelo algoritmo oficial da Receita Federal.

    Args:
        cpf (str): CPF a ser validado, com ou sem pontuação.

    Returns:
        bool: True se o CPF for válido, False caso contrário.
    """
    # Remove pontos, traços e espaços antes de qualquer validação
    cpf = cpf.replace(".", "").replace("-", "").strip()

    # CPF deve ter exatamente 11 dígitos numéricos
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    # Sequências como 111.111.111-11 são inválidas mesmo passando no cálculo
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador (peso 10 a 2)
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    primeiro_dv = 0 if resto < 2 else 11 - resto

    if primeiro_dv != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador (peso 11 a 2)
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    segundo_dv = 0 if resto < 2 else 11 - resto

    if segundo_dv != int(cpf[10]):
        return False

    return True


def validar_titulo_eleitor(titulo):
    """Valida um título de eleitor verificando formato e dígitos verificadores.

    Confere se o título possui 12 dígitos, valida o código de UF e recalcula
    os dois dígitos verificadores seguindo as regras do TSE.

    Args:
        titulo (str): Título de eleitor a ser validado (apenas dígitos).

    Returns:
        bool: True se o título for válido, False caso contrário.
    """
    titulo = titulo.strip()

    # Título deve ter exatamente 12 dígitos numéricos
    if len(titulo) != 12 or not titulo.isdigit():
        return False

    # Estrutura do título: 8 dígitos sequenciais + 2 de UF + 2 verificadores
    sequencial = titulo[:8]
    uf = titulo[8:10]
    dv1_informado = int(titulo[10])
    dv2_informado = int(titulo[11])
    codigo_uf = int(uf)

    # Código de UF válido vai de 01 (SP) a 28 (exterior)
    if codigo_uf < 1 or codigo_uf > 28:
        return False

    # Calcula o primeiro dígito verificador com pesos de 2 a 9
    pesos_dv1 = [2, 3, 4, 5, 6, 7, 8, 9]
    soma = 0
    for i in range(8):
        soma += int(sequencial[i]) * pesos_dv1[i]
    resto = soma % 11

    # UFs 01 e 02 (SP e MG) usam regra especial para resto 0
    if resto == 0 and codigo_uf in (1, 2):
        primeiro_dv = 1
    elif resto == 10:
        primeiro_dv = 0
    else:
        primeiro_dv = resto

    if primeiro_dv != dv1_informado:
        return False

    # Calcula o segundo dígito verificador usando os dígitos da UF e o primeiro DV
    pesos_dv2 = [7, 8, 9]
    valores_dv2 = [int(uf[0]), int(uf[1]), primeiro_dv]
    soma = 0
    for i in range(3):
        soma += valores_dv2[i] * pesos_dv2[i]
    resto = soma % 11

    # Mesma regra especial para UFs 01 e 02
    if resto == 0 and codigo_uf in (1, 2):
        segundo_dv = 1
    elif resto == 10:
        segundo_dv = 0
    else:
        segundo_dv = resto

    if segundo_dv != dv2_informado:
        return False

    return True


def solicitar_cpf():
    """Solicita um CPF ao usuário em loop até que um valor válido seja informado.

    Args:
        Nenhum.

    Returns:
        str: CPF válido digitado pelo usuário, sem formatação.
    """
    while True:
        cpf = input("Digite o CPF: ").strip()
        if validar_cpf(cpf):
            return cpf
        print("CPF inválido! Digite novamente.")


def solicitar_cpf_parcial():
    """Solicita os 4 primeiros dígitos do CPF para busca parcial.

    Args:
        Nenhum.

    Returns:
        str: String com exatamente 4 dígitos numéricos.
    """
    while True:
        cpf = input("Digite os 4 primeiros dígitos do CPF: ").strip()
        if cpf.isdigit() and len(cpf) == 4:
            return cpf
        print("Digite exatamente 4 números.")


def solicitar_titulo():
    """Solicita um título de eleitor ao usuário em loop até que um valor válido seja informado.

    Args:
        Nenhum.

    Returns:
        str: Título de eleitor válido digitado pelo usuário.
    """
    while True:
        titulo = input("Digite o título de eleitor: ").strip()
        if validar_titulo_eleitor(titulo):
            return titulo
        print("Título de eleitor inválido! Digite novamente.")