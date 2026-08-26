from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, db

cliente = TestClient(app)


def test_listar_todos_os_imoveis_com_sucesso():
    mock_colecao = MagicMock()

    mock_doc1 = MagicMock()
    mock_doc1.id = "id_imovel_a"
    mock_doc1.to_dict.return_value = {
        "titulo": "Casa Confortável",
        "cidade": "Belo Horizonte",
        "estado": "MG",
        "valor": 850000.0,
        "imagens": ["url_externa.png"],
    }

    mock_doc2 = MagicMock()
    mock_doc2.id = "id_imovel_b"
    mock_doc2.to_dict.return_value = {
        "titulo": "Cobertura Luxuosa",
        "cidade": "Salvador",
        "estado": "BA",
        "valor": 2500000.0,
        "imagens": ["url_vista.jpeg", "url_piscina.jpeg"],
    }

    mock_colecao.stream.return_value = [mock_doc1, mock_doc2]
    db.collection = MagicMock(return_value=mock_colecao)

    resposta = cliente.get("/api/imoveis/")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 99  # FALHA INTENCIONAL para testar comentário de erro
    assert resposta.json()[0]["id"] == "id_imovel_a"
    assert resposta.json()[0]["titulo"] == "Casa Confortável"
    assert resposta.json()[1]["id"] == "id_imovel_b"
    assert resposta.json()[1]["titulo"] == "Cobertura Luxuosa"
    mock_colecao.stream.assert_called_once()


def test_obter_imovel_por_id_existente():
    mock_colecao = MagicMock()
    mock_snapshot = MagicMock()
    mock_snapshot.id = "imovel_encontrado_id"
    mock_snapshot.exists = True
    mock_snapshot.to_dict.return_value = {
        "titulo": "Terreno Amplo",
        "cidade": "Curitiba",
        "estado": "PR",
        "valor": 300000.0,
        "imagens": [],
    }
    mock_doc_ref = MagicMock()
    mock_doc_ref.get.return_value = mock_snapshot
    mock_colecao.document.return_value = mock_doc_ref
    db.collection = MagicMock(return_value=mock_colecao)

    resposta = cliente.get("/api/imoveis/imovel_encontrado_id")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == "imovel_encontrado_id"
    assert resposta.json()["titulo"] == "Terreno Amplo"
    assert resposta.json()["cidade"] == "Curitiba"
    mock_colecao.document.assert_called_once_with("imovel_encontrado_id")
