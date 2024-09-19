#pip install requests

import requests

def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        
        if "erro" not in dados:
            return {
                "logradouro": dados.get("logradouro"),
                "bairro": dados.get("bairro"),
                "cidade": dados.get("localidade"),
                "estado": dados.get("uf"),
                "cep": dados.get("cep")
            }
        else:
            return "CEP não encontrado."
    else:
        return f"Erro na consulta: {response.status_code}"

cep = "88056120"  # Insira o CEP desejado
info = buscar_cep(cep)

if isinstance(info, dict):
    print(f"Rua: {info['logradouro']}")
    print(f"Bairro: {info['bairro']}")
    print(f"Cidade: {info['cidade']}")
    print(f"Estado: {info['estado']}")
else:
    print(info)
