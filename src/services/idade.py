from datetime import datetime

def calcular_idade(data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    data_hoje = datetime.now()
    idade = data_hoje.year - data_nascimento.year
    
    # Verifica se a pessoa já fez aniversário este ano
    if (data_hoje.month, data_hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    
    # Retorna True se a idade for igual ou maior a 18, False caso contrário
    return idade >= 18
