from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
