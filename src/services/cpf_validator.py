import re
import numpy as np

def cpf_validador(cpf: str):
    cpf_numerico = re.sub("[^0-9]", "", cpf)
    cpf_como_np = np.array([int(i)for i in cpf_numerico])
    numeros_10_a_2 = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2])
    numeros_11_a_2 = np.array([11, 10, 9, 8, 7, 6, 5, 4, 3, 2])
    primeiro_digito_valido = sum(cpf_como_np[0:9] * 10* numeros_10_a_2) % 11
    segundo_digito_valido = sum(cpf_como_np[0:10] * 10* numeros_11_a_2) % 11
    if cpf_como_np[9] ==primeiro_digito_valido and cpf_como_np[10] == segundo_digito_valido:
        cpfvali=True
    else:
        cpfvali=False
    return cpfvali