import re

def validar_senha(senha):
    #pelo menos 8 caracteres
    if len(senha) < 8:
        return False
    #menos uma letra maiúscula
    if not re.search(r'[A-Z]', senha):
        return False
    
    #pelo menos um numero
    if not re.search(r'\d', senha):
        return False
    
    #pelo menos um caractere especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False
    
    return True