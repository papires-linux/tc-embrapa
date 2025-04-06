#import pandas as pd
import requests,json
from bs4                import BeautifulSoup

def getDadosWebScraping(url:str,tag_tb_base:str) -> list:
    # Faz a requisição para o site
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Cria o objeto BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontra a tabela no HTML
        # Como o site pode ter várias tabelas, podemos precisar ajustar o seletor
        tabela = soup.find('table', class_=tag_tb_base)
        
        # Se não encontrar com a classe 'tabela', tenta encontrar qualquer tabela
        if not tabela:
            tabela = soup.find('table')
        
        # Se encontrou a tabela
        if tabela:
            # Lista para armazenar os dados
            dados = []
            
            # Encontra todas as linhas da tabela
            linhas = tabela.find_all('tr')
            
            # Extrai os cabeçalhos
            cabecalhos = []
            for celula in linhas[0].find_all(['th', 'td']):
                cabecalhos.append(celula.get_text(strip=True))
            
            # Extrai os dados das linhas
            for linha in linhas[1:]:
                colunas = linha.find_all(['td', 'th'])
                if len(colunas) > 0:
                    linha_dados = {}
                    for i, celula in enumerate(colunas):
                        if i < len(cabecalhos):
                            linha_dados[cabecalhos[i]] = celula.get_text(strip=True)
                    dados.append(linha_dados)
            
            # # Cria um DataFrame com os dados
            # df = pd.DataFrame(dados)
            
            # # Exibe o DataFrame
            # print(df.head())
            return 200, dados
        else:
            texto = "Não foi possível encontrar a tabela no site."
            print(texto)
            return 404, texto
    else:
        texto = f"Falha ao acessar o site. Status code: {response.status_code}"
        print(texto)
        return 404, texto

# URL do site
#url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"
url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
#url = "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_03"

default_tag_tb_base = "tb_base tb_dados"
dados = getDadosWebScraping(url,default_tag_tb_base)
print(dados)