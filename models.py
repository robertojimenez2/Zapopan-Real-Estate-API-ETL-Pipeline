from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Propiedad(Base):
    __tablename__ = 'propiedades'

    id = Column(Integer, primary_key=True, index=True)

    url_origen = Column(String, unique=True, index=True, nullable=False)
    titulo = Column(String, nullable=False)

    colonia = Column(String, index=True)
    municipio = Column(String, default="Zapopan")

    m2_terreno = Column(Float, nullable=True)
    m2_construccion = Column(Float, nullable=True)
    habitaciones = Column(Integer, nullable=True)
    banios = Column(Float, nullable=True)

    # metadata
    fecha_descubrimiento = Column(DateTime, default=datetime.utcnow)

    precios = relationship("Precio", back_populates="propiedad")


class Precio(Base):
    __tablename__ = 'historial_precios'

    id = Column(Integer, primary_key=True, index=True)
    propiedad_id = Column(Integer, ForeignKey('propiedades.id'))

    precio = Column(Float, nullable=False)
    moneda = Column(String, default="MXN")  # Importante si hay rentas en USD
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    propiedad = relationship("Propiedad", back_populates="precios")