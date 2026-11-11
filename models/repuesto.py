from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class Repuesto(Base):
    __tablename__ = "repuestos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_sku = Column(String(20), unique=True, index=True)
    nombre = Column(String(100))
    precio_compra = Column(Float)
    precio_venta = Column(Float)
    stock_actual = Column(Integer, default=0)