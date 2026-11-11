from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from typing import List
from core.database import obtener_bd
from models.mecanico import Mecanico
from schemas.mecanico_repuesto import MecanicoCreate, MecanicoResponse

router = APIRouter(prefix="/mecanicos", tags=["Mecánicos"])

@router.post("/", response_model=MecanicoResponse, status_code=201)
async def crear_mecanico(
    mecanico: MecanicoCreate,
    db: AsyncSession = Depends(obtener_bd)
):
    nuevo_mecanico = Mecanico(**mecanico.model_dump())

    db.add(nuevo_mecanico)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un mecánico con ese documento")

    await db.refresh(nuevo_mecanico)

    return nuevo_mecanico

@router.get("/", response_model=List[MecanicoResponse])
async def listar_mecanicos(db: AsyncSession = Depends(obtener_bd)):
    sentencia = select(Mecanico)
    resultado = await db.execute(sentencia)
    mecanicos = resultado.scalars().all()

    return mecanicos