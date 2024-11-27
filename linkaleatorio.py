import random
import string

def gerar_string_aleatoria():
    # Gera 5 caracteres aleatórios
    cinco_caracteres = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    # Gera uma letra aleatória
    letra1 = random.choice(string.ascii_letters)
    # Número 3
    numero = '3'
    # Gera outra letra aleatória
    letra2 = random.choice(string.ascii_letters)
    # Gera 4 caracteres aleatórios
    quatro_caracteres = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    # Concatena tudo
    resultado = cinco_caracteres + letra1 + numero + letra2 + quatro_caracteres
    return resultado

# Exemplo de uso
string_gerada = gerar_string_aleatoria()
print(string_gerada)
