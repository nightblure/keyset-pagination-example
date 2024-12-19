from fastapi import FastAPI

from src.api import router
from src.lifespan import lifespan

app = FastAPI(
    lifespan=lifespan
)
app.include_router(router)
