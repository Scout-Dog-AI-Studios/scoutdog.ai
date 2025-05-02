from fastapi import FastAPI
from app.api.v1.endpoints import greet as greet_router_v1
from app.api.v1.endpoints import upload as upload_router_v1
from contextlib import asynccontextmanager
from app.db.session import connect_to_astra, close_astra_connection

# --- CORS Middleware ---
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_astra()
    yield
    close_astra_connection()


# FastAPI app instance with lifespan event
app = FastAPI(title="Hello World Backend", lifespan=lifespan)


# Root endpoint for basic check
@app.get("/")
async def read_root():
    """Provides a simple health check message."""
    return {"message": "Backend is running!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] for dev, but restrict in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
# app.include_router(test_router_v1.router, prefix="/api/v1", tags=["v1_test"])
app.include_router(greet_router_v1.router, prefix="/api/v1", tags=["v1_greet"])
app.include_router(upload_router_v1.router, prefix="/api/v1", tags=["v1_upload"])
# We will add more routers and logic later
