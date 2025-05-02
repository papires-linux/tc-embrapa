import json
import ast
import logging
import requests
import pandas as pd
from datetime import date
from typing import Optional, Tuple, Union
from bs4 import BeautifulSoup

def ler_Variaveis(caminho_arquivo:str) -> dict:    
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return dados

CONFIG_DADOS_JSON = ler_Variaveis('config/db_site.json')
CONFIG_JSON = ler_Variaveis('config/config.json')

def echo(texto):
    logging.info(texto)
    print(texto)
    return texto

# --- Web scraping principal ---
def get_dados_web_scraping(
        url: str,
        funcao: str,
        tipo: str,
        ano: Optional[int] = None,
        tag_tb_base: Optional[str] = None
    ) -> Tuple[int, Union[str, list]]:
    try:
        status, dados = get_dados_web_scraping_web(url, ano, tag_tb_base)

        if status == 200:
            echo("Captura de dados via web")
            return status, dados

        echo("Captura de dados via CSV")
        return get_dados_csv(funcao, tipo, ano)

    except Exception as e:
        echo("Erro ao obter dados via scraping")
        return 500, str(e)

def incluir_ano(url: str, ano: int) -> str:
    base_url, query = url.split("?")
    return f"{base_url}?ano={ano}&{query}"

def get_schema(schema_raw: str, ano: int) -> list:
    return ast.literal_eval(schema_raw.replace('{ano}', str(ano)))

def dict_renomear_colunas(chave: list, valor: str) -> dict:
    valores = ast.literal_eval(valor)
    return dict(zip(chave, valores))

# --- Scraping Web ---

def get_dados_web_scraping_web(
        url: str,
        ano: Optional[int] = None,
        tag_tb_base: Optional[str] = ''
    ) -> Tuple[int, Union[str, list]]:
    try:
        if ano:
            url = incluir_ano(url, ano)
        echo(f"URL para consulta: {url}")
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return 404, f"Erro ao acessar o site: status {response.status_code}"
        soup = BeautifulSoup(response.content, 'html.parser')
        tabela = soup.find('table', class_=tag_tb_base) or soup.find('table')
        if not tabela:
            return 404, "Tabela não encontrada na página."
        linhas = tabela.find_all('tr')
        if not linhas:
            return 404, "Tabela sem conteúdo."
        cabecalho = [cell.get_text(strip=True) for cell in linhas[0].find_all(['th', 'td'])]
        dados = []

        for linha in linhas[1:]:
            colunas = linha.find_all(['td', 'th'])
            if colunas:
                linha_dados = {
                    cabecalho[i]: cell.get_text(strip=True).replace('.', '').replace('-', '0').replace(',', '.')
                    for i, cell in enumerate(colunas) if i < len(cabecalho)
                }
                dados.append(linha_dados)
        return 200, dados
    except Exception as e:
        echo("Erro durante scraping web")
        return 500, f"Erro no scraping web: {str(e)}"

# --- Leitura de CSV ---

def get_dados_csv(
        funcao: str,
        tipo: str,
        ano: Optional[int] = None
    ) -> Tuple[int, Union[str, list]]:
    try:
        config = CONFIG_DADOS_JSON[funcao]
        tipo_config = config.get(tipo, {})
        url_csv = tipo_config.get("CSV")
        delimitador = config.get("DELIMITADOR", ",")

        echo(f"URL CSV: {url_csv}")
        response = requests.get(url_csv)
        response.raise_for_status()

        df = pd.read_csv(url_csv, sep=delimitador)

        schema_raw = config.get("SCHEMA_RAW")
        schema_rename = config.get("SCHEMA_RENAME")

        ano_pesquisa = ano or date.today().year
        colunas_ano = get_schema(schema_raw, ano_pesquisa)

        df_filtrado = df[colunas_ano].rename(columns=dict_renomear_colunas(colunas_ano, schema_rename))

        json_data = df_filtrado.to_json(orient='records', force_ascii=False)
        dados = json.loads(json_data)

        echo(f"Total de registros carregados: {len(dados)}")
        return 200, dados

    except requests.exceptions.RequestException as e:
        echo("Erro ao acessar o CSV")
        return 500, f"Erro ao acessar o CSV: {str(e)}"

    except Exception as e:
        echo("Erro ao processar CSV")
        return 500, f"Erro ao processar CSV: {str(e)}"
