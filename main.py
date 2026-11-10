from fastapi import FastAPI
from routers.ordenes import router as router_ordenes

app = FastAPI(
    title="API Recepción Taller Mecánico",
    description="Sistema de triaje y facturación",
    version="1.0"
)

app.include_router(router_ordenes)
