from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import class to SQLAlchemy
from models import Base, Propiedad, Precio
# Name of DB
DATABASE_URL = "sqlite:///./zapopan_propiedades.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Force the creation of the tables
Base.metadata.create_all(bind=engine)
print("Success conection")