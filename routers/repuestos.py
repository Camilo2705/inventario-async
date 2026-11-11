from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from typing import List
from core.database import obtener_bd
from models.repuesto import Repuesto
from schemas.mecanico_repuesto import RepuestoCreate, RepuestoResponse

router = APIRouter(prefix="/repuestos", tags=["Repuestos"])

@router.post("/", response_model=RepuestoResponse, status_code=201)
async def crear_repuesto(
    repuesto: RepuestoCreate,
    db: AsyncSession = Depends(obtener_bd)
):
    nuevo_repuesto = Repuesto(**repuesto.model_dump())

    db.add(nuevo_repuesto)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un repuesto con ese código SKU")

    await db.refresh(nuevo_repuesto)

    return nuevo_repuesto

@router.get("/", response_model=List[RepuestoResponse])
async def listar_repuestos(db: AsyncSession = Depends(obtener_bd)):
    sentencia = select(Repuesto)
    resultado = await db.execute(sentencia)
    repuestos = resultado.scalars().all()

    return repuestos