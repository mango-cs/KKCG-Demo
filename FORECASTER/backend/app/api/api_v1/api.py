from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    auth,
    forecasts,
    sales,
    dishes,
    outlets,
    models,
    alerts,
    dashboard,
    simulation,
    users,
    analytics
)

# Create main API router
api_router = APIRouter()

# Include all endpoint routers with appropriate prefixes and tags
api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Authentication"]
)

api_router.include_router(
    forecasts.router, 
    prefix="/forecasts", 
    tags=["Forecasting"]
)

api_router.include_router(
    sales.router, 
    prefix="/sales", 
    tags=["Sales Data"]
)

api_router.include_router(
    dishes.router, 
    prefix="/dishes", 
    tags=["Dishes"]
)

api_router.include_router(
    outlets.router, 
    prefix="/outlets", 
    tags=["Outlets"]
)

api_router.include_router(
    models.router, 
    prefix="/models", 
    tags=["ML Models"]
)

api_router.include_router(
    alerts.router, 
    prefix="/alerts", 
    tags=["Alerts"]
)

api_router.include_router(
    dashboard.router, 
    prefix="/dashboard", 
    tags=["Dashboard"]
)

api_router.include_router(
    simulation.router, 
    prefix="/simulation", 
    tags=["Data Simulation"]
)

api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["User Management"]
)

api_router.include_router(
    analytics.router, 
    prefix="/analytics", 
    tags=["Analytics"]
) 