from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class Mecanico(Base):
    __tablename__ = "mecanicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento = Column(String(15), unique=True, nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    especialidad = Column(String(50))  # Ej: "Electricidad", "Motor", "Frenos"
    activo = Column(Boolean, default=True)  # Para soft delete