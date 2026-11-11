from pydantic import BaseModel, Field
from typing import Optional

# ---------- Mecánico ----------
class MecanicoCreate(BaseModel):
    documento: str = Field(..., max_length=15, description="Documento de identidad")
    nombre_completo: str = Field(..., max_length=100)
    especialidad: Optional[str] = Field(None, max_length=50, description="Ej: Electricidad, Motor, Frenos")

class MecanicoResponse(BaseModel):
    id: int
    documento: str
    nombre_completo: str
    especialidad: Optional[str] = None
    activo: bool

    model_config = {"from_attributes": True}

# ---------- Repuesto ----------
class RepuestoCreate(BaseModel):
    codigo_sku: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    precio_compra: float = Field(..., ge=0)
    precio_venta: float = Field(..., ge=0)
    stock_actual: int = Field(0, ge=0)

class RepuestoResponse(BaseModel):
    id: int
    codigo_sku: str
    nombre: str
    precio_compra: float
    precio_venta: float
    stock_actual: int

    model_config = {"from_attributes": True}