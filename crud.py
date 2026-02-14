from sqlalchemy.orm import Session
import models

def get_propiedades(db: Session, limite: int = 100):

    return db.query(models.Propiedad).limit(limite).all()

def get_propiedad_por_id(db: Session, propiedad_id: int):

    return db.query(models.Propiedad).filter(models.Propiedad.id == propiedad_id).first()

def get_estadisticas_basicas(db: Session):

    from sqlalchemy import func
    promedio = db.query(func.avg(models.Precio.precio)).scalar()
    return {"precio_promedio": round(promedio, 2) if promedio else 0.0}