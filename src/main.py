import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.logging import logger
from src.core.config import settings
from src.core.db_healthcheck import check_database_connection
from src.auth.middleware import JWTValidationMiddleware
from src.auth.routes.user import router as user_router
from src.auth.routes.company import router as company_router
from src.auth.routes.microservice import router as microservice_router

app = FastAPI(
    title=settings.service_name,
    description="Service for managing authentication and authorization",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(JWTValidationMiddleware)

app.include_router(user_router, prefix="/auth/user")
app.include_router(company_router, prefix="/auth/company")
app.include_router(microservice_router, prefix="/auth/microservice")


@app.on_event("startup")
async def startup_event():
    """
    Event triggered on application startup.
    Logs startup activities and performs a database health check.
    """
    logger.info(f"Starting service: {settings.service_name}")
    if not check_database_connection():
        logger.error("Failed to connect to the database. Shutting down...")
        raise SystemExit("Database connection failed.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event triggered on application shutdown.
    Logs shutdown activities and cleans up resources.
    """
    logger.info(f"Shutting down the {settings.service_name} service...")


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify service and database status.
    """
    is_db_connected = check_database_connection()
    status = "connected" if is_db_connected else "not connected"
    logger.info(f"Health check: Database is {status}.")
    return {"status": "up", "database": status}


@app.get("/")
def root():
    """
    Root endpoint to confirm service is running.
    """
    logger.info("Root endpoint accessed.")
    return {"message": f"Welcome to {settings.service_name}!"}


if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
