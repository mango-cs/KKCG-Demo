from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import enum

class ModelType(str, enum.Enum):
    PROPHET = "prophet"
    XGBOOST = "xgboost"
    LSTM = "lstm"
    ENSEMBLE = "ensemble"

class ForecastRequest(BaseModel):
    dish_name: str = Field(..., description="Name of the dish to forecast")
    outlet_id: str = Field(..., description="Outlet identifier")
    model_name: ModelType = Field(default=ModelType.PROPHET, description="ML model to use")
    forecast_horizon: int = Field(default=7, ge=1, le=30, description="Number of days to forecast")
    include_confidence: bool = Field(default=True, description="Include confidence intervals")
    external_factors: Optional[Dict[str, Any]] = Field(default=None, description="Additional factors")
    force_refresh: bool = Field(default=False, description="Force refresh cache")

class ForecastResponse(BaseModel):
    dish_name: str
    outlet_id: str
    model_name: str
    forecast_date: datetime
    predictions: List[float]
    confidence_intervals: List[Tuple[Optional[float], Optional[float]]]
    model_metrics: Dict[str, Any]
    feature_importance: Dict[str, float]
    shap_values: Optional[Dict[str, Any]] = None
    warnings: List[str] = []
    metadata: Dict[str, Any] = {}

class BatchItem(BaseModel):
    dish_name: str
    outlet_id: str

class ForecastBatch(BaseModel):
    items: List[BatchItem]
    model_name: ModelType = ModelType.PROPHET
    forecast_horizon: int = Field(default=7, ge=1, le=30)
    include_confidence: bool = True
    external_factors: Optional[Dict[str, Any]] = None

class ModelComparison(BaseModel):
    dish_name: str
    outlet_id: str
    comparison_date: datetime
    models: Dict[str, Dict[str, Any]]
    ensemble_prediction: List[float]
    best_model: Optional[str]
    metadata: Dict[str, Any]

class WhatIfScenario(BaseModel):
    scenario_name: str = Field(..., description="Name of the scenario")
    dish_name: str
    outlet_id: str
    model_name: ModelType = ModelType.PROPHET
    forecast_horizon: int = Field(default=7, ge=1, le=30)
    
    # Scenario multipliers
    weather_multiplier: float = Field(default=1.0, ge=0.1, le=3.0, description="Weather impact multiplier")
    event_multiplier: float = Field(default=1.0, ge=0.1, le=5.0, description="Event impact multiplier")
    promotion_multiplier: float = Field(default=1.0, ge=0.1, le=3.0, description="Promotion impact multiplier")
    price_change_percent: float = Field(default=0.0, ge=-50.0, le=100.0, description="Price change percentage")

class ForecastMetrics(BaseModel):
    dish_name: str
    outlet_id: str
    model_name: str
    evaluation_period_days: int
    total_forecasts: int
    
    # Accuracy metrics
    mae: float = Field(..., description="Mean Absolute Error")
    mape: float = Field(..., description="Mean Absolute Percentage Error")
    rmse: float = Field(..., description="Root Mean Square Error")
    bias: float = Field(..., description="Forecast bias")
    accuracy_percentage: float = Field(..., description="Overall accuracy percentage")
    
    metadata: Dict[str, Any] = {} 