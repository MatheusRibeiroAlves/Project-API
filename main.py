from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from firebase_config import db
from schemas import ImovelCreate, ImovelResponse
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/imoveis/", response_model=ImovelResponse)
async def create_imovel(imovel: ImovelCreate):
    try:
        doc_ref = db.collection("imoveis").document()
        doc_ref.set(imovel.model_dump())
        return ImovelResponse(**imovel.model_dump(), id=doc_ref.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar imóvel: {str(e)}")


@app.get("/api/imoveis/", response_model=list[ImovelResponse])
async def get_imoveis():
    try:
        imoveis = []
        docs = db.collection("imoveis").stream()
        for doc in docs:
            imovel = ImovelResponse(**doc.to_dict(), id=doc.id)
            imoveis.append(imovel)
        return imoveis
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erro ao obter imóveis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter imóveis: {str(e)}")


@app.get("/api/imoveis/{imovel_id}", response_model=ImovelResponse)
async def get_imovel(imovel_id: str = Path(..., description="O ID do imóvel a ser retornado")):
    try:
        doc_ref = db.collection("imoveis").document(imovel_id)
        doc = doc_ref.get()
        if doc.exists:
            return ImovelResponse(**doc.to_dict(), id=doc.id)
        raise HTTPException(status_code=404, detail=f"Imóvel com ID {imovel_id} não encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter imóvel {imovel_id}: {str(e)}")


@app.delete("/api/imoveis/{imovel_id}", response_model=ImovelResponse)
async def delete_imovel(imovel_id: str = Path(..., description="O ID do imóvel a ser deletado")):
    try:
        doc_ref = db.collection("imoveis").document(imovel_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Imóvel com ID {imovel_id} não encontrado")
        doc_ref.delete()
        return ImovelResponse(**doc.to_dict(), id=doc.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar imóvel {imovel_id}: {str(e)}")


@app.put("/api/imoveis/{imovel_id}", response_model=ImovelResponse)
async def update_imovel(
    imovel_id: str = Path(..., description="O ID do imóvel a ser atualizado"),
    imovel_update: ImovelCreate = Body(..., description="Os dados atualizados do imóvel"),
):
    try:
        doc_ref = db.collection("imoveis").document(imovel_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Imóvel com ID {imovel_id} não encontrado")
        doc_ref.update(imovel_update.model_dump(exclude_unset=True))
        updated_doc = doc_ref.get()
        return ImovelResponse(**updated_doc.to_dict(), id=updated_doc.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar imóvel {imovel_id}: {str(e)}")
