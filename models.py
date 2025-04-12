# models.py

from pydantic import BaseModel
from typing import Optional

class Imovel(BaseModel):
    titulo: str

