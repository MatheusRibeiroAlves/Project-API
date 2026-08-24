from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, db

cliente = TestClient(app)


def test_listar_imoveis_disponiveis_no_site():
    mock_colecao = MagicMock()

    mock_doc = MagicMock()
    mock_doc.id = "id_imovel_site"
    mock_doc.to_dict.return_value = {
        "titulo": "Apartamento Vista Mar",
        "cidade": "Florianópolis",
        "estado": "SC",
        "valor": 980000.0,
        "imagens": ["foto_frente.jpg"],
    }

    mock_colecao.stream.return_value = [mock_doc]
    db.collection = MagicMock(return_value=mock_colecao)

    resposta = cliente.get("/api/imoveis/")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["titulo"] == "Apartamento Vista Mar"
    assert resposta.json()[0]["cidade"] == "Florianópolis"


def test_obter_imovel_por_id_nao_existente():
    mock_colecao = MagicMock()
    mock_snapshot = MagicMock()
    mock_snapshot.exists = False
    mock_doc_ref = MagicMock()
    mock_doc_ref.get.return_value = mock_snapshot
    mock_colecao.document.return_value = mock_doc_ref
    db.collection = MagicMock(return_value=mock_colecao)

    resposta = cliente.get("/api/imoveis/id_que_nao_existe")

    assert resposta.status_code == 404
