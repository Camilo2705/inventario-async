import json
from pathlib import Path

ARCHIVO = Path("taller.json")


def leer_ordenes() -> list:
    if not ARCHIVO.exists():
        return []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        contenido = f.read().strip()
        return json.loads(contenido) if contenido else []


def guardar_ordenes(ordenes: list) -> None:
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(ordenes, f, ensure_ascii=False, indent=4)