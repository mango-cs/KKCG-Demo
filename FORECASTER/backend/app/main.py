from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import logging
import time
import uvicorn
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.core.redis_client import redis_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Restaurant Demand Forecasting API")
    
    # Create database tables (optional for demo)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created")
    except Exception as e:
        logger.warning(f"⚠️ Database not available, running in demo mode: {e}")
    
    # Initialize Redis connection (optional for demo)
    try:
        await redis_client.ping()
        logger.info("✅ Redis connection established")
    except Exception as e:
        logger.warning(f"⚠️ Redis not available, running in demo mode: {e}")
    
    logger.info("🎯 API is ready! Running in demo mode with sample data")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Restaurant Demand Forecasting API")
    try:
        await redis_client.close()
        logger.info("✅ Cleanup completed")
    except Exception as e:
        logger.warning(f"⚠️ Cleanup failed (expected in demo mode): {e}")

# Create FastAPI application
app = FastAPI(
    title="🍛 Restaurant Demand Forecasting API",
    description="""
    ## AI-Powered Demand Forecasting System for South Indian Restaurant Chain
    
    This API provides comprehensive demand forecasting capabilities using advanced ML models:
    
    * **Prophet Model**: Time series forecasting with seasonality
    * **XGBoost Model**: Gradient boosting with feature importance
    * **LSTM Model**: Deep learning for sequential patterns
    
    ### Features:
    - 📊 Real-time demand forecasting
    - 🔍 Model explanations with SHAP values
    - 🎯 What-if scenario simulations
    - 📈 Historical data analysis
    - 🚨 Alert system for inventory management
    - 📋 Model performance monitoring
    
    ### Use Cases:
    - Daily operations planning
    - Inventory optimization
    - Staff scheduling
    - Menu performance analysis
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware for request timing and logging
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log request
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    
    return response

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection (optional for demo)
        from app.core.database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "healthy"
    except Exception as e:
        logger.warning(f"Database not available (demo mode): {e}")
        db_status = "unavailable (demo mode)"
    
    try:
        # Check Redis connection (optional for demo)
        await redis_client.ping()
        redis_status = "healthy"
    except Exception as e:
        logger.warning(f"Redis not available (demo mode): {e}")
        redis_status = "unavailable (demo mode)"
    
    # API is considered healthy even if external services are unavailable (demo mode)
    health_status = {
        "status": "healthy",  # Always healthy for demo
        "mode": "demo" if (db_status == "unavailable (demo mode)" or redis_status == "unavailable (demo mode)") else "production",
        "timestamp": time.time(),
        "services": {
            "database": db_status,
            "redis": redis_status
        },
        "version": "1.0.0",
        "message": "API is running in demo mode with sample data" if db_status == "unavailable (demo mode)" else "All services operational"
    }
    
    return health_status

# Metrics endpoint for Prometheus
@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🍛 Welcome to Restaurant Demand Forecasting API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "status": "running"
    }

# Import forecast service and schemas
from app.services.forecast_service import ForecastService
from app.api.schemas.forecast import ForecastRequest, ForecastResponse

# Initialize forecast service
forecast_service = ForecastService()

# Forecasting endpoints
@app.get("/api/v1/forecasts/test", tags=["Forecasts"])
async def test_forecast():
    """Test forecast endpoint"""
    return {
        "message": "Forecast API is working!",
        "timestamp": time.time(),
        "sample_forecast": {
            "dish": "Masala Dosa",
            "outlet": "Chennai Central",
            "predicted_demand": 150,
            "confidence_interval": [140, 160],
            "forecast_date": "2025-06-13"
        }
    }

@app.post("/api/v1/forecasts", response_model=ForecastResponse, tags=["Forecasts"])
async def create_forecast(request: ForecastRequest):
    """
    Generate demand forecast for a specific dish and outlet
    
    **Parameters:**
    - **dish**: Name of the dish (e.g., "Masala Dosa", "Idli")
    - **outlet**: Outlet location (e.g., "Chennai Central", "Jubilee Hills")
    - **date_range**: List of dates for forecast
    - **weather**: Optional weather condition (sunny, rainy, cloudy, stormy)
    - **event**: Optional event type (cricket finals, festival, holiday, diwali, pongal)
    
    **Returns:**
    - Forecast predictions with confidence intervals
    - SHAP-style explanations for feature contributions
    """
    try:
        # Convert request to dict for service
        request_data = {
            "dish": request.dish,
            "outlet": request.outlet,
            "date_range": request.date_range,
            "weather": request.weather,
            "event": request.event
        }
        
        # Generate forecast using service
        forecast_result = forecast_service.generate_forecast(request_data)
        
        # Create response
        response = ForecastResponse(
            forecast=forecast_result["forecast"],
            explanations=forecast_result["explanations"]
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error in forecast endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate forecast: {str(e)}")

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested resource was not found.",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "message": f"HTTP {exc.status_code} error occurred.",
            "path": str(request.url.path)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 