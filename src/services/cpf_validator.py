import re
import numpy as np

def cpf_validador(cpf: str):
    # Remover caracteres não numéricos
    cpf_numerico = re.sub("[^0-9]", "", cpf)
    
    # Verificar se o CPF tem 11 dígitos
    if len(cpf_numerico) != 11:
        return False  # CPF inválido se não tiver 11 dígitos
    
    # Converter CPF em array de números
    cpf_como_np = np.array([int(i) for i in cpf_numerico])
    
    # Pesos para os dígitos verificadores
    numeros_10_a_2 = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2])
    numeros_11_a_2 = np.array([11, 10, 9, 8, 7, 6, 5, 4, 3, 2])
    
    # Cálculo do primeiro dígito verificador
    primeiro_digito_valido = sum(cpf_como_np[0:9] * numeros_10_a_2) % 11
    if primeiro_digito_valido < 2:
        primeiro_digito_valido = 0
    else:
        primeiro_digito_valido = 11 - primeiro_digito_valido
    
    # Cálculo do segundo dígito verificador
    segundo_digito_valido = sum(cpf_como_np[0:10] * numeros_11_a_2) % 11
    if segundo_digito_valido < 2:
        segundo_digito_valido = 0
    else:
        segundo_digito_valido = 11 - segundo_digito_valido
    
    # Verificar se os dígitos conferem
    if cpf_como_np[9] == primeiro_digito_valido and cpf_como_np[10] == segundo_digito_valido:
        return True
    else:
        return False
