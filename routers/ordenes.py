from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from schemas import OrdenCreate, OrdenPatch, OrdenUpdate
from database import leer_base_datos, guardar_base_datos
from dependencias import verificar_api_key, parametros_paginacion

router = APIRouter(prefix="/ordenes", tags=["Gestionar ordenes"])

@router.get("/")
async def obtener_ordenes(
    estado: Optional[str] = Query(None, description="Filtrar por estado. Ej: Reparada"),
    modelo: Optional[str] = Query(None, description="Filtrar por modelo (coincidencia parcial). Ej: Bajaj"),
    costo_minimo: Optional[float] = Query(None, ge=0, description="Costo de reparación mínimo. Ej: 100000"),
    paginacion: dict = Depends(parametros_paginacion)
):
    datos = await leer_base_datos()

    # Filtros acumulativos: cada filtro recibido reduce la lista anterior (AND)
    resultado = datos

    if estado:
        resultado = [o for o in resultado if o["estado"].lower() == estado.lower()]

    if modelo:
        resultado = [o for o in resultado if modelo.lower() in o["modelo"].lower()]

    if costo_minimo is not None:
        resultado = [o for o in resultado if o["costo_reparacion"] >= costo_minimo]

    # La paginación se aplica DESPUÉS de filtrar
    skip = paginacion["skip"]
    limit = paginacion["limit"]
    pagina = resultado[skip : skip + limit]

    return {
        "total_ordenes": len(resultado),
        "mostrando": len(pagina),
        "skip": skip,
        "ordenes": pagina
    }

@router.post("/", status_code=201)
async def crear_orden(orden: OrdenCreate, api_key: str = Depends(verificar_api_key)):
    datos = await leer_base_datos()
    
    # Regla de Negocio: Validar que la placa no esté ya en el taller
    for item in datos:
        if item["placa"] == orden.placa and item["estado"] != "Entregada":
            raise HTTPException(
                status_code=400, 
                detail=f"La moto con placa {orden.placa} ya se encuentra en el taller ({item['estado']})."
            )
            
    nueva_orden = orden.model_dump()
    nueva_orden["estado"] = "En diagnóstico"
    nueva_orden["costo_reparacion"] = 0.0
    
    datos.append(nueva_orden)
    await guardar_base_datos(datos)
    
    return {"mensaje": "Orden creada exitosamente", "orden": nueva_orden, "Llave usada": api_key}

@router.put("/{placa}")
async def actualizar_orden(placa: str, orden_update: OrdenUpdate):
        
    datos = await leer_base_datos()
    
    for i, item in enumerate(datos):
        if item["placa"] == placa:
            
            datos[i]["estado"] = orden_update.nuevo_estado
            datos[i]["costo_reparacion"] = orden_update.costo_reparacion
            
            await guardar_base_datos(datos)
            return {"mensaje": "Orden actualizada correctamente", "orden": datos[i]}
            
    raise HTTPException(status_code=404, detail="Orden no encontrada")

@router.delete("/{placa}", status_code=204)
async def eliminar_orden(placa: str):
    datos = await leer_base_datos()

    # for orden in datos:
    #     if orden["placa"] != placa:
    #         datos_filtrados.append(orden)

    datos_filtrados = [orden for orden in datos if orden["placa"] != placa]

    if len(datos) == len(datos_filtrados):
        raise HTTPException(status_code=404, detail="La orden no existe.")

    await guardar_base_datos(datos_filtrados)

    return None

@router.patch("/{placa}")
async def actualizacion_parcial(placa: str, orden_patch: OrdenPatch):
    datos = await leer_base_datos()

    for i, orden in enumerate(datos):
        if orden["placa"] == placa:
            datos_a_actualizar = orden_patch.model_dump(exclude_unset=True)

            # Actualizamos solo con los datos que llegaron
            datos[i].update(datos_a_actualizar)

            await guardar_base_datos(datos)
            return {"mesaje": "La orden ha sido actualizada con los siguientes datos", "orden": datos[i]}

    raise HTTPException(status_code=404, detail="La orden no existe.")