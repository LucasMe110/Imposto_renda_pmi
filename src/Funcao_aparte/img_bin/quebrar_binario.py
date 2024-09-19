import mimetypes

def quebrar_em_binario(caminho_arquivo):
    # Verifica o tipo do arquivo
    tipo_mime, _ = mimetypes.guess_type(caminho_arquivo)

    # Verifica se o tipo do arquivo é suportado (img, xml, etc.)
    tipos_suportados = ['image/jpeg', 'image/png', 'application/xml', 'text/xml']

    if tipo_mime not in tipos_suportados:
        raise ValueError(f"Tipo de arquivo não suportado: {tipo_mime}")

    # Lê o arquivo em modo binário
    with open(caminho_arquivo, 'rb') as arquivo:
        conteudo_binario = arquivo.read()

    return conteudo_binario
