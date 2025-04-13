from pydantic import BaseModel
from typing import Optional, List

class Imovel(BaseModel):

    titulo: str
    cidade: str
    estado: str
    valor: float
    imagens: Optional[List[str]] = None