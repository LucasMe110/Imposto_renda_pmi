import re

# Função para validar critérios de segurança da senha
def validar_senha(senha):
    if len(senha) < 8:
        return False
    if not re.search(r'[A-Z]', senha):
        return False
    if not re.search(r'\d', senha):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False
    return True

# Solicita a senha inicial
senha = input("Digite a senha: ")

# Verifica se a senha atende aos critérios de segurança
if validar_senha(senha):
    # Se atender, solicita a repetição da senha
    senha2 = input("Repita a senha: ")

    # Verifica se as senhas são iguais
    if senha == senha2:
        print("Senha válida e cadastrada com sucesso!")
    else:
        print("Senhas não coincidem.")
else:
    print("A senha não atende aos requisitos de segurança.")
