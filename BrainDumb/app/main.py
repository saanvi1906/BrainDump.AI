from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .models import *  # ensures tables are registered
from .routers import health,dumps

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BrainDumb API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.APP_CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(dumps.router)
