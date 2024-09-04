import re
import numpy as np

def calcular_digito(cpf, pesos):
    soma = sum(cpf[i] * pesos[i] for i in range(len(pesos)))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto

def cpf_validador(cpf: str):
    cpf_numerico = re.sub("[^0-9]", "", cpf)
    if len(cpf_numerico) != 11:
        return False

    cpf_como_np = np.array([int(i) for i in cpf_numerico])

    primeiro_digito_valido = calcular_digito(cpf_como_np[:9], range(10, 1, -1))
    segundo_digito_valido = calcular_digito(cpf_como_np[:10], range(11, 2, -1))

    return cpf_como_np[9] == primeiro_digito_valido and cpf_como_np[10] == segundo_digito_valido
