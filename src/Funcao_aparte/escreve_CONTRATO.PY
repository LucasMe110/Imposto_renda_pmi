from docx import Document

# Abrir o documento
doc_path = 'CONTRATO DE ADESÃO DE USO DE APLICATIVO.docx'
document = Document(doc_path)

# Dados para substituir
dados_contratante = {
    '[Nome do Contratante]': 'Lucas Mello',
    '[Nacionalidade]': 'Brasileiro',
    '[Estado Civil]': 'Solteiro',
    '[Profissão]': 'Desenvolvedor de Software',
    '[Número do CPF]': '123.456.789-00',
    '[Endereço Completo]': 'Rua Exemplo, 123, Bairro Centro, Florianópolis, SC'
}

# Função para substituir textos no documento
def substituir_texto(doc, dados):
    for p in doc.paragraphs:
        for key, value in dados.items():
            if key in p.text:
                p.text = p.text.replace(key, value)

# Substituir os placeholders pelos dados reais
substituir_texto(document, dados_contratante)

# Salvar o novo documento com as alterações
document.save('C:/workspace/funcao_aparte/CONTRATO_ATUALIZADO.docx')

print("Documento atualizado e salvo com sucesso!")

