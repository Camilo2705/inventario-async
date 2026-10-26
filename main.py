from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import leer_ordenes, guardar_ordenes

app = FastAPI(title="Sistema de Órdenes de Servicio")


class OrdenCreate(BaseModel):
    placa: str = Field(..., min_length=1, max_length=6)
    modelo: str = Field(..., min_length=1)
    falla_reportada: str = Field(..., min_length=1)


class OrdenUpdate(BaseModel):
    nuevo_estado: str
    costo_reparacion: float


@app.post("/ordenes", status_code=201)
def crear_orden(orden: OrdenCreate):
    ordenes = leer_ordenes()

    # Si la moto ya está en el taller (estado distinto de "Entregada") -> 400
    for o in ordenes:
        if o["placa"] == orden.placa and o["estado"] != "Entregada":
            raise HTTPException(
                status_code=400, detail="La moto ya se encuentra en el taller"
            )

    nueva = orden.dict()
    nueva["estado"] = "En diagnóstico"
    nueva["costo_reparacion"] = 0

    ordenes.append(nueva)
    guardar_ordenes(ordenes)
    return nueva


@app.get("/ordenes")
def consultar_ordenes():
    return leer_ordenes()


@app.put("/ordenes/{placa}")
def actualizar_orden(placa: str, datos: OrdenUpdate):
    ordenes = leer_ordenes()

    orden = None
    for o in reversed(ordenes):
        if o["placa"] == placa:
            orden = o
            break

    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    if datos.nuevo_estado == "Reparada" and datos.costo_reparacion <= 0:
        raise HTTPException(
            status_code=400,
            detail="No se puede marcar como reparada sin asignar un costo de reparación",
        )

    orden["estado"] = datos.nuevo_estado
    orden["costo_reparacion"] = datos.costo_reparacion
    guardar_ordenes(ordenes)
    return orden