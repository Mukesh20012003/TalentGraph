import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from neo4j.exceptions import ServiceUnavailable, Neo4jError, AuthError

from app.config import settings
from app.db import db
from app.routes import health, talent, graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("talent_graph")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting up: Connecting to CognoDB...")
    db.connect()
    yield
    logger.info("🛑 Shutting down: Closing connection pool...")
    db.close()

app = FastAPI(
    title="Talent & Skills Knowledge Graph API",
    description="Cognitive talent exploration API powered by CognoDB and openCypher.",
    version="1.0.0",
    lifespan=lifespan
)

# -------------------------------------------------------------
# Global Exception Handlers (Requirement 5.3: Graceful Error Handling)
# -------------------------------------------------------------

@app.exception_handler(ServiceUnavailable)
async def service_unavailable_handler(request: Request, exc: ServiceUnavailable):
    logger.error(f"Database unavailable during request to {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Database Service Unavailable",
            "message": "Unable to communicate with the CognoDB instance. Please check credentials or instance status.",
            "path": request.url.path
        }
    )

@app.exception_handler(AuthError)
async def auth_error_handler(request: Request, exc: AuthError):
    logger.error(f"Database authentication error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Database Authentication Failed",
            "message": "Invalid CognoDB credentials provided in environment configuration."
        }
    )

@app.exception_handler(Neo4jError)
async def neo4j_error_handler(request: Request, exc: Neo4jError):
    logger.error(f"Cypher execution error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Cypher Execution Error",
            "message": exc.message,
            "code": exc.code
        }
    )

# -------------------------------------------------------------
# Middleware & Routers
# -------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(talent.router)
app.include_router(graph.router)

@app.get("/")
def root():
    return {
        "name": "Talent & Skills Knowledge Graph API",
        "status": "online",
        "docs": "/docs",
        "health": "/api/health"
    }