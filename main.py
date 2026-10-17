import asyncio
from database import vender_producto, tareas_segundo_plano

async def intentar_venta(codigo, cantidad):
    try:
        resultado = await vender_producto(codigo, cantidad)
        print(f"Venta exitosa: {resultado}")
    except KeyError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
        
async def main():
    await asyncio.gather(
        intentar_venta("P001", 2),
        intentar_venta("P002", 3),
        intentar_venta("P003", 10),
        intentar_venta("P999", 1),
    )
    if tareas_segundo_plano:
        await asyncio.gather(*tareas_segundo_plano)
        
asyncio.run(main())