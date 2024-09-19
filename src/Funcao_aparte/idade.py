
from datetime import datetime

def calcular_idade(data_nascimento):
    # Converte a string da data de nascimento para o formato de data
    data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
    # Pega a data hoje
    data_hoje = datetime.now()
    # Calcula a idade
    idade = data_hoje.year - data_nascimento.year
    
    # Verifica se a pessoa já fez aniversário este ano
    if (data_hoje.month, data_hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    
    return idade

# Exemplo de uso
data_nascimento = input("Digite a sua data de nascimento (dd/mm/aaaa): ")
idade = calcular_idade(data_nascimento)
print(f"Sua idade é: {idade} anos")
