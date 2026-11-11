from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class Orden(Base):
    __tablename__ = "ordenes"

    #Definir las columnas
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    placa = Column(String(6), index=True, nullable=False)
    modelo = Column(String(20))
    falla_reportada = Column(String(255))
    estado = Column(String(20), default="En diagnóstico")
    costo_reparacion = Column(Float, default=0.0)