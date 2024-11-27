import random
import string

def gerar_string_com_id(usuario_id):
    """
    Gera uma string aleatória no formato solicitado:
    compartilhado/ + 5 caracteres + uma letra + ID do usuário + uma letra + 4 caracteres
    """
    # Gera 5 caracteres aleatórios
    cinco_caracteres = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    # Gera uma letra aleatória
    letra1 = random.choice(string.ascii_letters)
    # Converte o ID do usuário em string
    id_usuario = str(usuario_id)
    # Gera outra letra aleatória
    letra2 = random.choice(string.ascii_letters)
    # Gera 4 caracteres aleatórios
    quatro_caracteres = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    # Concatena tudo com o prefixo
    resultado = f"compartilhado/{cinco_caracteres}{letra1}{id_usuario}{letra2}{quatro_caracteres}"
    return resultado
