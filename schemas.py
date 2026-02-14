from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Price
class PrecioBase(BaseModel):
    precio: float
    moneda: str
    fecha_registro: datetime


class PrecioOut(PrecioBase):
    id: int

    class Config:
        from_attributes = True  # Esto permite a Pydantic leer de SQLAlchemy


# Propieties
class PropiedadBase(BaseModel):
    titulo: str
    url_origen: str
    colonia: Optional[str] = None
    municipio: Optional[str] = "Zapopan"


# Output
class PropiedadOut(PropiedadBase):
    id: int
    fecha_descubrimiento: datetime

    precios: List[PrecioOut] = []

    class Config:
        from_attributes = True