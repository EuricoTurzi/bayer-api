from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Resultado(BaseModel):
    id: int
    qr_value: str
    max_padroes: int
    informacao: str
    data_hora: datetime
    imagem: Optional[str]  # base64 da imagem (pode ser None em alguns casos)
