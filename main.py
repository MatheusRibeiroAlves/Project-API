from fastapi import FastAPI, HTTPException, Path, Body
from firebase_config import db
from schemas import ImovelCreate, ImovelResponse
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/imoveis/", response_model=ImovelResponse)
async def create_imovel(imovel: ImovelCreate):
    try:
        doc_ref = db.collection("imoveis").document()
        doc_ref.set(imovel.dict())
        return ImovelResponse(**imovel.dict(), id=doc_ref.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar imóvel: {str(e)}")


@app.get("/api/imoveis/", response_model=list[ImovelResponse])
async def get_imoveis():
    try:
        imoveis = []
        docs = db.collection("imoveis").stream()
        for doc in docs:
            doc_dict = doc.to_dict()
            imovel = ImovelResponse(**doc_dict, id=doc.id)
            imoveis.append(imovel)
        return imoveis
    except Exception as e:
        logging.error(f"Erro ao obter imóveis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter imóveis: {str(e)}")


@app.get("/api/imoveis/{imovel_id}", response_model=ImovelResponse)
async def get_imovel(imovel_id: str = Path(..., description="O ID do imóvel a ser retornado")):
    try:
        doc_ref = db.collection("imoveis").document(imovel_id)
        doc = doc_ref.get()
        if doc.exists:
            imovel_data = doc.to_dict()
            return ImovelResponse(**imovel_data, id=doc.id)
        else:
            raise HTTPException(status_code=404, detail=f"Imóvel com ID {imovel_id} não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter imóvel com ID {imovel_id}: {str(e)}")


@app.delete("/api/imoveis/{imovel_id}", response_model=ImovelResponse)
async def delete_imovel(imovel_id: str = Path(..., description="O ID do imóvel a ser deletado")):
    try:
        doc_ref = db.collection("imoveis").document(imovel_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Imóvel com ID {imovel_id} não encontrado")

        doc_ref.delete()
        return ImovelResponse(**doc.to_dict(), id=doc.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar imóvel com ID {imovel_id}: {str(e)}")


@app.put("/api/imoveis/{imovel_id}", response_model=ImovelResponse)
async def update_imovel(
    imovel_id: str = Path(..., description="O ID do imóvel a ser atualizado"),
    imovel_update: ImovelCreate = Body(..., description="Os dados atualizados do imóvel")
):
    try:
        doc_ref = db.collection("imoveis").document(imovel_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Imóvel com ID {imovel_id} não encontrado")

        doc_ref.update(imovel_update.dict(exclude_unset=True))
        updated_doc = doc_ref.get()
        return ImovelResponse(**updated_doc.to_dict(), id=updated_doc.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar imóvel com ID {imovel_id}: {str(e)}")
