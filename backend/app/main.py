from fastapi import FastAPI

try:
    from app.presentation.routers import api_router
except ImportError:
    api_router = None

def create_app() -> FastAPI:
    app = FastAPI(
        title="Gaia Template API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Mount routers if they exist
    if api_router:
        app.include_router(api_router, prefix="/api/v1")
        
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}
        
    return app

app = create_app()
