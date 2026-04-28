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
