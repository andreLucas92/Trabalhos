def calcular_digito_verificador(cpf_base):
    """
    Calcula os dois dígitos verificadores de um CPF dado os primeiros 9 dígitos.
    
    Parâmetros:
    cpf_base (str): String com os 9 primeiros dígitos do CPF.
    
    Retorna:
    str: Os dois dígitos verificadores.
    """
    if len(cpf_base) != 9 or not cpf_base.isdigit():
        raise ValueError("O CPF base deve ter exatamente 9 dígitos numéricos.")
    
    # Cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf_base[i]) * (10 - i)
    resto = soma % 11
    dig1 = 0 if resto < 2 else 11 - resto
    
    # Cálculo do segundo dígito verificador
    cpf_com_dig1 = cpf_base + str(dig1)
    soma = 0
    for i in range(10):
        soma += int(cpf_com_dig1[i]) * (11 - i)
    resto = soma % 11
    dig2 = 0 if resto < 2 else 11 - resto
    
    return str(dig1) + str(dig2)

# Exemplo de uso
if __name__ == "__main__":
    cpf_base = input("Digite os 9 primeiros dígitos do CPF: ")
    try:
        digitos = calcular_digito_verificador(cpf_base)
        cpf_completo = cpf_base + digitos
        print(f"CPF completo: {cpf_completo}")
    except ValueError as e:
        print(e)
