from fastapi import FastAPI, HTTPException
from database import cargar, vender_producto

app = FastAPI()


@app.get("/categorias")
def obtener_categorias():
    productos = cargar()
    categorias = set()

    for producto in productos.values():
        categorias.add(producto["categoria"])

    return list(categorias)


@app.get("/alertas/stock")
def alertas_stock():
    productos = cargar()
    criticos = []

    for codigo, producto in productos.items():
        if producto["stock"] <= 3:
            producto["codigo"] = codigo
            criticos.append(producto)

    return criticos


@app.get("/productos/buscar/{palabra_clave}")
def buscar_productos(palabra_clave: str):
    productos = cargar()
    encontrados = []

    for codigo, producto in productos.items():
        if palabra_clave.lower() in producto["nombre"].lower():
            producto["codigo"] = codigo
            encontrados.append(producto)

    return encontrados


@app.post("/vender/{codigo}/{cantidad}")
async def vender(codigo: str, cantidad: int):
    try:
        return await vender_producto(codigo, cantidad)
    except KeyError:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    except ValueError:
        raise HTTPException(status_code=400, detail="Stock insuficiente")