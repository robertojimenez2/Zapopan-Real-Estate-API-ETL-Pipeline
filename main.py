from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# clean arquitecture
from database import SessionLocal
import crud
import models
import schemas

# Init app
app = FastAPI(
    title="Zapopan Real Estate API",
    description="API profesional estructurada en capas para consultar rentas.",
    version="2.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints

@app.get("/", tags=["Inicio"])
def home():
    return {"mensaje": "API de Inmuebles activa. Arquitectura MVC implementada."}


@app.get("/api/propiedades", response_model=List[schemas.PropiedadOut], tags=["Propiedades"])
def obtener_propiedades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    propiedades = crud.get_propiedades(db, limite=limit)
    return propiedades

# Endpoint nuevo: Buscar una sola casa por su ID
@app.get("/api/propiedades/{propiedad_id}", response_model=schemas.PropiedadOut, tags=["Propiedades"])
def obtener_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    db_propiedad = crud.get_propiedad_por_id(db, propiedad_id=propiedad_id)
    if db_propiedad is None:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada en la base de datos.")
    return db_propiedad

@app.get("/api/estadisticas", tags=["Análisis de Datos"])
def obtener_estadisticas(db: Session = Depends(get_db)):
    stats = crud.get_estadisticas_basicas(db)
    return {
        "zona": "Zapopan",
        "precio_promedio": stats["precio_promedio"],
        "moneda": "MXN"
    }