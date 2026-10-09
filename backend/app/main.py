import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, WebSocketDisconnect

from app.database.connection import Base, engine
from app.database import models

from app.routes.servers import router as server_router
from app.routes.metrics import router as metrics_router
from app.services.websocket import manager
from app.routes.api_monitor import router as api_monitor_router


from app.services.monitor_scheduler import monitoring_loop
from app.routes.alerts import router as alerts_router
from app.routes.logs import router as logs_router
from app.routes.auth import router as auth_router

from app.routes.deployments import router as deployments_router


Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):

    monitoring_task = asyncio.create_task(
        monitoring_loop()
    )

    yield

    monitoring_task.cancel()

    
app = FastAPI(
    title="ServerWatch API",
    description="Mini DevOps monitoring platform",
    version="1.0.0",
    lifespan=lifespan
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(server_router)
app.include_router(metrics_router)
app.include_router(api_monitor_router)
app.include_router(alerts_router)
app.include_router(logs_router)
app.include_router(auth_router)
app.include_router(deployments_router)


@app.get("/")
def home():
    return {
        "message": "ServerWatch API is running"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:

        while True:

            data = await websocket.receive_text()

            await manager.broadcast(data)

    except WebSocketDisconnect:

        manager.disconnect(websocket)