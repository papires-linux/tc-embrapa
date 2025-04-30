# Como rodar os testes: pytest tests/

import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock

from src.operator import operator_enum
from src.routes.dados import obter_dados  # ajuste o caminho se necessário

#❌ Teste de URL não encontrada (None)
@patch("src.routes.dados.CONFIG_DADOS_JSON", {
    "FUNCX": {
        "WEB": "https://example.com/data"
    }
})
@patch("src.api.dados.scraping.getDadosWebScraping")
def test_obter_dados_sucesso(mock_scraping):
    mock_scraping.return_value = (200, {"data": [1, 2, 3]})
    
    resultado = obter_dados(operator_enum.FuncaoEnum("FUNCX"))
    
    assert resultado == {"data": [1, 2, 3]}
    mock_scraping.assert_called_once()

#❌ Teste de URL não encontrada (None)
@patch("src.routes.dados.CONFIG_DADOS_JSON", {
    "FUNCX": {}
})
def test_obter_dados_url_nao_encontrada():
    with pytest.raises(HTTPException) as exc:
        obter_dados(operator_enum.FuncaoEnum("FUNCX"))
    
    assert exc.value.status_code == 404
    assert "Path not found" in str(exc.value.detail)

#❌ Teste de erro retornado pelo scraping (ex: 500)
@patch("src.routes.dados.CONFIG_DADOS_JSON", {
    "FUNCX": {
        "WEB": "https://example.com/data"
    }
})
@patch("src.routes.dados.scraping.getDadosWebScraping")
def test_obter_dados_scraping_retorna_erro(mock_scraping):
    mock_scraping.return_value = (500, "Erro interno")

    with pytest.raises(HTTPException) as exc:
        obter_dados(operator_enum.FuncaoEnum("FUNCX"))
    
    assert exc.value.status_code == 500
    assert "Erro interno" in str(exc.value.detail)

# ❌ Teste de erro por chave inválida (KeyError)
@patch("src.routes.dados.CONFIG_DADOS_JSON", {})
def test_obter_dados_chave_invalida():
    with pytest.raises(HTTPException) as exc:
        obter_dados(operator_enum.FuncaoEnum("FUNCX"))
    
    assert exc.value.status_code == 400
    assert "Erro de configuração" in str(exc.value.detail)
