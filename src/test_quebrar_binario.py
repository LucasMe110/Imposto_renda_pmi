# src/test_quebrar_binario.py
import os
from quebrar_binario import quebrar_em_binario

# Caminho absoluto para a imagem original
caminho_imagem = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test.png'))
# Caminho para salvar a imagem reconstruída
caminho_saida = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagem_reconstruida.png'))

def reconstruir_imagem(caminho_saida, conteudo_binario):
    # Escreve o conteúdo binário em um novo arquivo de imagem
    with open(caminho_saida, 'wb') as arquivo:
        arquivo.write(conteudo_binario)

    print(f"Imagem reconstruída com sucesso em: {caminho_saida}")


try:
    # Converte a imagem original para binário
    conteudo_binario = quebrar_em_binario(caminho_imagem)
    print("Arquivo convertido para binário com sucesso!")
    print(f"Conteúdo binário (primeiros 100 bytes): {conteudo_binario[:100]}")

    # Reconstrói a imagem a partir do binário
    reconstruir_imagem(caminho_saida, conteudo_binario)
except ValueError as e:
    print(f"Erro: {e}")
except FileNotFoundError as e:
    print(f"Erro: Arquivo não encontrado. {e}")
