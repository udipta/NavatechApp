from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import admin_router, organization_router
from services.database import create_tables


# Lifespan context manager to handle startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    create_tables()
    yield


# Add lifespan to FastAPI app
app = FastAPI(title="NavaTech FastAPI App", lifespan=lifespan)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(admin_router)
app.include_router(organization_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

