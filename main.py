from fastapi import FastAPI, HTTPException
from firebase_config import db
from models import Imovel

app = FastAPI()

@app.post("/imoveis/")
async def create_imovel(imovel: Imovel):
    try:
        doc_ref = db.collection("imoveis").document()
        doc_ref.set(imovel.dict())
        return {"message": "Imóvel cadastrado com sucesso.", "id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar imóvel: {str(e)}")