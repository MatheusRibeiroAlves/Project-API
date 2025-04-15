from fastapi import FastAPI, HTTPException
from firebase_config import db
from models import Imovel
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/api/imoveis/")
async def create_imovel(imovel: Imovel):
    try:
        doc_ref = db.collection("imoveis").document()
        doc_ref.set(imovel.dict())
        return {"message": "Imóvel cadastrado com sucesso.", "id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar imóvel: {str(e)}")


@app.get("/api/imoveis/", response_model=list[Imovel])
async def get_imoveis():
    try:
        imoveis = []
        docs = db.collection("imoveis").stream()
        for doc in docs:
            doc_dict = doc.to_dict()
            logging.info(f"Dados do documento do Firestore: {doc_dict}")
            imovel = Imovel(**doc_dict)
            imoveis.append(imovel)
        return imoveis
    except Exception as e:
        logging.error(f"Erro ao obter imóveis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter imóveis: {str(e)}")