def validar_cpf(cpf): #Valida se um CPF é matematicamente correto.
    
    cpf = cpf.replace(".", "").replace("-", "").strip() # Remove caracteres especiais caso existam

    if len(cpf) != 11 or not cpf.isdigit():  # Verifica se tem 11 dígitos e se todos são numéricos
        return False
    if cpf == cpf[0] * 11: # Rejeita CPFs com todos os dígitos iguais
        return False
    #Cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)

    resto = soma % 11

    if resto < 2:
        primeiro_dv = 0
    else:
        primeiro_dv = 11 - resto
    
    if primeiro_dv != int(cpf[9]): # Verifica se o primeiro dígito verificador calculado bate com o do CPF informado
        return False
    #Cálculo do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)

    resto = soma % 11

    if resto < 2:
        segundo_dv = 0
    else:
        segundo_dv = 11 - resto

    if segundo_dv != int(cpf[10]): # Verifica se o segundo dígito verificador calculado bate com o do CPF informado
        return False

    return True

#Valida se um Título de Eleitor é matematicamente correto.
def validar_titulo_eleitor(titulo):

    titulo = titulo.strip()

    if len(titulo) != 12 or not titulo.isdigit(): # Verifica se tem 12 dígitos e se são todos numéricos
        return False

    # Separação das partes do título de eleitor
    sequencial = titulo[:8]   # Pega os 8 primeiros dígitos
    uf = titulo[8:10]         # Pega os dígitos 9º e 10º(código da UF)
    dv1_informado = int(titulo[10])  # Pega o dígito 11º(primeiro DV)
    dv2_informado = int(titulo[11])  # Pega o dígito 12º(segundo DV)

    codigo_uf = int(uf)

    if codigo_uf < 1 or codigo_uf > 28: # Verifica se o código da UF é válido (01 a 28)
        return False

    # --- Cálculo do primeiro dígito verificador ---
    pesos_dv1 = [2, 3, 4, 5, 6, 7, 8, 9]
    soma = 0
    for i in range(8):
        soma += int(sequencial[i]) * pesos_dv1[i]

    resto = soma % 11

    if resto == 0 and codigo_uf in (1, 2): # SP (01) e MG (02): se resto for 0, DV1 = 1
        primeiro_dv = 1
    
    elif resto == 10: # Para todos: se resto for 10, DV1 = 0
        primeiro_dv = 0
    else:
        primeiro_dv = resto

    if primeiro_dv != dv1_informado:
        return False

    # --- Cálculo do segundo dígito verificador ---
    pesos_dv2 = [7, 8, 9]
    valores_dv2 = [int(uf[0]), int(uf[1]), primeiro_dv] # Usa os dois dígitos da UF e o primeiro DV calculado

    soma = 0
    
    for i in range(3):
        soma += valores_dv2[i] * pesos_dv2[i]

    resto = soma % 11

    if resto == 0 and codigo_uf in (1, 2): # SP (01) e MG (02): se resto for 0, DV2 = 1
        segundo_dv = 1
    elif resto == 10: # Para todos: se resto for 10, DV2 = 0
        segundo_dv = 0
    else:
        segundo_dv = resto

    if segundo_dv != dv2_informado:
        return False
    
    return True

# --- Solicitar cpf com loop de validação ---
def solicitar_cpf():
    #Solicita o CPF ao usuário em loop até que um CPF válido seja informado.
    while True:
        cpf = input("Digite o CPF: ").strip()
        if validar_cpf(cpf):
            return cpf
        print("CPF inválido! Digite novamente.")


# --- SOlicitar titulo com loop de validação ---
def solicitar_titulo():
    #Solicita o título de eleitor ao usuário em loop até que um título válido seja informado.
    while True:
        titulo = input("Digite o título de eleitor: ").strip()
        if validar_titulo_eleitor(titulo):
            return titulo
        print("Título de eleitor inválido! Digite novamente.")