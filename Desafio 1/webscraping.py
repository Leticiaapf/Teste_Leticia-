import requests # #fazer a requesição ao endereço da internet e obter o conteudo da pagina (obter o código html da página)
import os  # acesso ao sistema operacional, vai ajudar a salvar a pasta
from bs4 import BeautifulSoup #pegar o código html e transformar em objeto python para ser manipulado

from urllib.parse import urljoin # manipulação de URLs em Python
import zipfile   #biblioteca para eu conseguir trablhar com arquivo zip

# Criar pasta para salvar PDFs
os.makedirs('meus_pdfs', exist_ok=True)

# URL base
url_base = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

# Fazer a requisição e obter a página
pagina = requests.get(url_base)
dados_pagina = BeautifulSoup(pagina.text, 'html.parser')

# Função para fazer o download do PDF e salvar na pasta meus_pdfs
def download_pdf(url):
    try:
        # Construir a URL completa (caso seja um link relativo)
        url_completa = urljoin(url_base, url)

        # Nome do arquivo (extraído do final da URL)
        nome_arquivo = os.path.join('meus_pdfs', url_completa.split("/")[-1])

        # Fazer o download do arquivo PDF
        resposta = requests.get(url_completa, stream=True)

        if resposta.status_code == 200:
            
            # Salvar o arquivo
            with open(nome_arquivo, 'wb') as pdf:
                for chunk in resposta.iter_content(chunk_size=1024):
                    pdf.write(chunk)
            print(f'Download concluído: {nome_arquivo}')
            return nome_arquivo  # Retorna o nome do arquivo baixado para poder adicionar ao ZIP
        else:
            print(f'Erro ao baixar {url_completa}: Status code {resposta.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'Erro ao fazer requisição para {url_completa}: {e}')


# usei find_all para percorrer todos os <li> e fazer o download dos PDFs
todos_anexos = dados_pagina.find_all('li')
arquivos_pdf = []  # Lista para armazenar os caminhos dos arquivos PDF baixados

for li in todos_anexos:
    link = li.find('a', class_="internal-link")
    if link:  # Verifica se o link foi encontrado
        url = link['href']

        # Verificar se a URL termina com '.pdf'
        if url.endswith('.pdf'): #logo, vai exibir apenas os que terminas com .pdf
            print(f"Baixando: {url}")
            nome_arquivo_baixado = download_pdf(url)
            if nome_arquivo_baixado:
                arquivos_pdf.append(nome_arquivo_baixado)

# Compactação dos arquivos PDF em um único arquivo ZIP
if arquivos_pdf:
    with zipfile.ZipFile('meus_pdfs/arquivos_compactados.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arquivo_pdf in arquivos_pdf:
            zipf.write(arquivo_pdf, os.path.basename(arquivo_pdf))  # Adiciona o arquivo ao ZIP
        print('Arquivos compactados com sucesso em "meus_pdfs/arquivos_compactados.zip"')
else:
    print('Nenhum arquivo PDF foi baixado para compactação.')