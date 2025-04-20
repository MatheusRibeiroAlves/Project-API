from unittest.mock import patch
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app, db
from schemas import ImovelCreate, ImovelResponse

def test_criar_novo_imovel_com_sucesso():
    cliente_api_teste = TestClient(app)
    mock_colecao_imoveis = MagicMock()
    mock_documento_imovel = MagicMock()
    mock_documento_imovel.id = "id_gerado_pelo_banco"
    mock_colecao_imoveis.document.return_value = mock_documento_imovel
    db.collection = MagicMock(return_value=mock_colecao_imoveis)
    dados_novo_imovel = {"titulo": "Apartamento Espaçoso", "cidade": "Rio de Janeiro", "estado": "RJ", "valor": 1200000.0, "imagens": ["url_fachada.jpg", "url_sala.jpg"]}
    resposta = cliente_api_teste.post("/api/imoveis/", json=dados_novo_imovel)
    assert resposta.status_code == 200
    assert resposta.json()["id"] == "id_gerado_pelo_banco"
    assert resposta.json()["titulo"] == "Apartamento Espaçoso"
    assert resposta.json()["cidade"] == "Rio de Janeiro"
    assert resposta.json()["estado"] == "RJ"
    assert resposta.json()["valor"] == 1200000.0
    assert resposta.json()["imagens"] == ["url_fachada.jpg", "url_sala.jpg"]
    mock_colecao_imoveis.document.assert_called_once()
    mock_documento_imovel.set.assert_called_once_with(dados_novo_imovel)

def test_listar_todos_os_imoveis_com_sucesso():
    cliente_api_teste = TestClient(app)
    mock_colecao_imoveis = MagicMock()

    mock_doc1 = MagicMock()
    mock_doc1.id = "id_imovel_a"
    mock_doc1.to_dict.return_value = {"titulo": "Casa Confortável", "cidade": "Belo Horizonte", "estado": "MG", "valor": 850000.0, "imagens": ["url_externa.png"]}

    mock_doc2 = MagicMock()
    mock_doc2.id = "id_imovel_b"
    mock_doc2.to_dict.return_value = {"titulo": "Cobertura Luxuosa", "cidade": "Salvador", "estado": "BA", "valor": 2500000.0, "imagens": ["url_vista.jpeg", "url_piscina.jpeg"]}

    mock_colecao_imoveis.stream.return_value = [mock_doc1, mock_doc2]
    db.collection = MagicMock(return_value=mock_colecao_imoveis)

    resposta = cliente_api_teste.get("/api/imoveis/")
    print(resposta.json())
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2
    assert resposta.json()[0]["id"] == "id_imovel_a"
    assert resposta.json()[0]["titulo"] == "Casa Confortável"
    assert resposta.json()[0]["cidade"] == "Belo Horizonte"
    assert resposta.json()[0]["estado"] == "MG"
    assert resposta.json()[0]["valor"] == 850000.0
    assert resposta.json()[0]["imagens"] == ["url_externa.png"]
    assert resposta.json()[1]["id"] == "id_imovel_b"
    assert resposta.json()[1]["titulo"] == "Cobertura Luxuosa"
    assert resposta.json()[1]["cidade"] == "Salvador"
    assert resposta.json()[1]["estado"] == "BA"
    assert resposta.json()[1]["valor"] == 2500000.0
    assert resposta.json()[1]["imagens"] == ["url_vista.jpeg", "url_piscina.jpeg"]

    mock_colecao_imoveis.stream.assert_called_once()

def test_obter_imovel_por_id_existente():
    cliente_api_teste = TestClient(app)
    mock_colecao_imoveis = MagicMock()
    mock_documento_snapshot = MagicMock()
    mock_documento_snapshot.id = "imovel_encontrado_id"
    mock_documento_snapshot.exists = True
    mock_documento_snapshot.to_dict.return_value = {"titulo": "Terreno Amplo", "cidade": "Curitiba", "estado": "PR", "valor": 300000.0, "imagens": []}

    mock_documento_referencia = MagicMock()
    mock_documento_referencia.get.return_value = mock_documento_snapshot

    mock_colecao_imoveis.document.return_value = mock_documento_referencia
    db.collection = MagicMock(return_value=mock_colecao_imoveis)
    resposta = cliente_api_teste.get("/api/imoveis/imovel_encontrado_id")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == "imovel_encontrado_id"
    assert resposta.json()["titulo"] == "Terreno Amplo"
    assert resposta.json()["cidade"] == "Curitiba"
    assert resposta.json()["estado"] == "PR"
    assert resposta.json()["valor"] == 300000.0
    assert resposta.json()["imagens"] == []
    mock_colecao_imoveis.document.assert_called_once_with("imovel_encontrado_id")
    mock_documento_referencia.get.assert_called_once()

def test_deletar_imovel_existente():
    cliente_api_teste = TestClient(app)
    mock_colecao_imoveis = MagicMock()
    mock_documento_snapshot = MagicMock()
    mock_documento_snapshot.id = "imovel_para_deletar_id"
    mock_documento_snapshot.exists = True
    mock_documento_snapshot.to_dict.return_value = {"titulo": "Loja Comercial", "cidade": "São Paulo", "estado": "SP", "valor": 1500000.0, "imagens": []}

    mock_documento_referencia = MagicMock()
    mock_documento_referencia.get.return_value = mock_documento_snapshot
    mock_documento_referencia.delete.return_value = None

    mock_colecao_imoveis.document.return_value = mock_documento_referencia
    db.collection = MagicMock(return_value=mock_colecao_imoveis)
    resposta = cliente_api_teste.delete("/api/imoveis/imovel_para_deletar_id")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == "imovel_para_deletar_id"
    assert resposta.json()["titulo"] == "Loja Comercial"
    assert resposta.json()["cidade"] == "São Paulo"
    assert resposta.json()["estado"] == "SP"
    assert resposta.json()["valor"] == 1500000.0
    assert resposta.json()["imagens"] == []
    mock_colecao_imoveis.document.assert_called_once_with("imovel_para_deletar_id")
    mock_documento_referencia.get.assert_called_once()
    mock_documento_referencia.delete.assert_called_once()

def test_atualizar_imovel_existente():
    cliente_api_teste = TestClient(app)
    mock_colecao_imoveis = MagicMock()

    mock_documento_snapshot_get = MagicMock()
    mock_documento_snapshot_get.id = "imovel_para_atualizar_id"
    mock_documento_snapshot_get.exists = True
    mock_documento_snapshot_get.to_dict.return_value = {"titulo": "Imovel Antigo", "cidade": "Cidade Velha", "estado": "CV", "valor": 700000.0, "imagens": []}

    mock_documento_snapshot_update = MagicMock()
    mock_documento_snapshot_update.id = "imovel_para_atualizar_id"
    mock_documento_snapshot_update.exists = True
    mock_documento_snapshot_update.to_dict.return_value = {"titulo": "Imovel Moderno", "cidade": "Cidade Nova", "estado": "CN", "valor": 950000.0, "imagens": ["nova_url.png"]}

    mock_documento_referencia = MagicMock()
    mock_documento_referencia.get.side_effect = [mock_documento_snapshot_get, mock_documento_snapshot_update]
    mock_documento_referencia.update.return_value = None

    mock_colecao_imoveis.document.return_value = mock_documento_referencia
    db.collection = MagicMock(return_value=mock_colecao_imoveis)

