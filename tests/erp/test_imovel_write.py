from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, db

cliente = TestClient(app)


def test_criar_novo_imovel_com_sucesso():
    mock_colecao = MagicMock()
    mock_documento = MagicMock()
    mock_documento.id = "id_gerado_pelo_banco"
    mock_colecao.document.return_value = mock_documento
    db.collection = MagicMock(return_value=mock_colecao)

    dados = {
        "titulo": "Apartamento Espaçoso",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "valor": 1200000.0,
        "imagens": ["url_fachada.jpg", "url_sala.jpg"],
    }
    resposta = cliente.post("/api/imoveis/", json=dados)

    assert resposta.status_code == 200
    assert resposta.json()["id"] == "id_gerado_pelo_banco"
    assert resposta.json()["titulo"] == "Apartamento Espaçoso"
    assert resposta.json()["cidade"] == "Rio de Janeiro"
    mock_colecao.document.assert_called_once()
    mock_documento.set.assert_called_once_with(dados)


def test_deletar_imovel_existente():
    mock_colecao = MagicMock()
    mock_snapshot = MagicMock()
    mock_snapshot.id = "imovel_para_deletar_id"
    mock_snapshot.exists = True
    mock_snapshot.to_dict.return_value = {
        "titulo": "Loja Comercial",
        "cidade": "São Paulo",
        "estado": "SP",
        "valor": 1500000.0,
        "imagens": [],
    }
    mock_doc_ref = MagicMock()
    mock_doc_ref.get.return_value = mock_snapshot
    mock_doc_ref.delete.return_value = None
    mock_colecao.document.return_value = mock_doc_ref
    db.collection = MagicMock(return_value=mock_colecao)

    resposta = cliente.delete("/api/imoveis/imovel_para_deletar_id")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == "imovel_para_deletar_id"
    assert resposta.json()["titulo"] == "Loja Comercial"
    mock_doc_ref.delete.assert_called_once()


def test_deletar_imovel_nao_existente():
    mock_colecao = MagicMock()
    mock_snapshot = MagicMock()
    mock_snapshot.exists = False
    mock_doc_ref = MagicMock()
    mock_doc_ref.get.return_value = mock_snapshot
    mock_colecao.document.return_value = mock_doc_ref
    db.collection = MagicMock(return_value=mock_colecao)

    resposta = cliente.delete("/api/imoveis/id_inexistente")

    assert resposta.status_code == 404


def test_atualizar_imovel_existente():
    mock_colecao = MagicMock()
    mock_snapshot_original = MagicMock()
    mock_snapshot_original.exists = True
    mock_snapshot_original.to_dict.return_value = {
        "titulo": "Imovel Antigo",
        "cidade": "Cidade Velha",
        "estado": "CV",
        "valor": 700000.0,
        "imagens": [],
    }
    mock_snapshot_atualizado = MagicMock()
    mock_snapshot_atualizado.id = "imovel_para_atualizar_id"
    mock_snapshot_atualizado.exists = True
    mock_snapshot_atualizado.to_dict.return_value = {
        "titulo": "Imovel Moderno",
        "cidade": "Cidade Nova",
        "estado": "CN",
        "valor": 950000.0,
        "imagens": ["nova_url.png"],
    }
    mock_doc_ref = MagicMock()
    mock_doc_ref.get.side_effect = [mock_snapshot_original, mock_snapshot_atualizado]
    mock_doc_ref.update.return_value = None
    mock_colecao.document.return_value = mock_doc_ref
    db.collection = MagicMock(return_value=mock_colecao)

    dados_atualizados = {
        "titulo": "Imovel Moderno",
        "cidade": "Cidade Nova",
        "estado": "CN",
        "valor": 950000.0,
        "imagens": ["nova_url.png"],
    }
    resposta = cliente.put("/api/imoveis/imovel_para_atualizar_id", json=dados_atualizados)

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Imovel Moderno"
    assert resposta.json()["valor"] == 950000.0


def test_atualizar_imovel_nao_existente():
    mock_colecao = MagicMock()
    mock_snapshot = MagicMock()
    mock_snapshot.exists = False
    mock_doc_ref = MagicMock()
    mock_doc_ref.get.return_value = mock_snapshot
    mock_colecao.document.return_value = mock_doc_ref
    db.collection = MagicMock(return_value=mock_colecao)

    dados = {
        "titulo": "Qualquer",
        "cidade": "Qualquer",
        "estado": "QQ",
        "valor": 100.0,
    }
    resposta = cliente.put("/api/imoveis/id_inexistente", json=dados)

    assert resposta.status_code == 404
