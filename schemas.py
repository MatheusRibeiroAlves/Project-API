from pydantic import BaseModel
from typing import Optional, List

class ImovelBase(BaseModel):
    titulo: str
    cidade: str
    estado: str
    valor: float
    imagens: Optional[List[str]] = None

class ImovelCreate(ImovelBase):
    pass

class ImovelResponse(ImovelBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True
