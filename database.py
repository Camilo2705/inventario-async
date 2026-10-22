import asyncio
import json
import os

ARCHIVO = "inventario.json"
tareas_segundo_plano = set()

DATOS_INICIALES = {
    "P001": {"nombre": "Mouse", "categoria": "Perifericos", "stock": 20},
    "P002": {"nombre": "Teclado", "categoria": "Perifericos", "stock": 5},
    "P003": {"nombre": "Monitor", "categoria": "Pantallas", "stock": 4},
}


def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def cargar():
    if not os.path.exists(ARCHIVO):
        guardar(DATOS_INICIALES)
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        return json.load(f)


async def alerta_stock_bajo(codigo, nombre, stock_actual):
    await asyncio.sleep(2)
    print(
        f"ALERTA CRITICA: El producto {nombre} ({codigo}) ha bajado a "
        f"{stock_actual} unidades. Solicitar restock inmediato."
    )


async def vender_producto(codigo, cantidad_vendida):
    datos = cargar()

    if codigo not in datos:
        raise KeyError("Producto no encontrado")

    producto = datos[codigo]

    if cantidad_vendida > producto["stock"]:
        raise ValueError("Stock insuficiente")

    producto["stock"] -= cantidad_vendida
    guardar(datos)

    if producto["stock"] < 3:
        tarea = asyncio.create_task(
            alerta_stock_bajo(codigo, producto["nombre"], producto["stock"])
        )
        tareas_segundo_plano.add(tarea)
        tarea.add_done_callback(tareas_segundo_plano.discard)

    return {
        "codigo": codigo,
        "producto": producto["nombre"],
        "vendidas": cantidad_vendida,
        "stock_restante": producto["stock"],
    }