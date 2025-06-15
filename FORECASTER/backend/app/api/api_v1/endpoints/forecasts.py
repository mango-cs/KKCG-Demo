from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.core.redis_client import redis_client
from app.core.celery_app import celery_app
from app.db import models
from app.api.schemas.forecasts import (
    ForecastRequest,
    ForecastResponse,
    ForecastBatch,
    ModelComparison,
    WhatIfScenario,
    ForecastMetrics
)
from app.ml.model_manager import ModelManager
from app.api.deps import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=ForecastResponse)
async def generate_forecast(
    request: ForecastRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Generate demand forecast for a specific dish and outlet
    
    **Parameters:**
    - **dish_name**: Name of the dish
    - **outlet_id**: Outlet identifier
    - **model_name**: ML model to use (prophet, xgboost, lstm, or ensemble)
    - **forecast_horizon**: Number of days to forecast
    - **include_confidence**: Whether to include confidence intervals
    - **external_factors**: Additional factors to consider
    
    **Returns:**
    - Forecast predictions with confidence intervals
    - Model metadata and feature importance
    - SHAP explanations (if available)
    """
    try:
        # Check cache first
        cache_key = f"forecast:{request.dish_name}:{request.outlet_id}:{request.model_name}:{request.forecast_horizon}"
        cached_forecast = await redis_client.get_json(cache_key)
        
        if cached_forecast and not request.force_refresh:
            logger.info(f"Returning cached forecast for {cache_key}")
            return ForecastResponse(**cached_forecast)
        
        # Initialize model manager
        model_manager = ModelManager()
        
        # Validate inputs
        dish = db.query(models.Dish).filter(models.Dish.name == request.dish_name).first()
        if not dish:
            raise HTTPException(status_code=404, detail=f"Dish '{request.dish_name}' not found")
        
        outlet = db.query(models.Outlet).filter(models.Outlet.outlet_id == request.outlet_id).first()
        if not outlet:
            raise HTTPException(status_code=404, detail=f"Outlet '{request.outlet_id}' not found")
        
        # Check if we have sufficient historical data
        min_data_points = 30  # Minimum 30 days of data
        data_count = db.query(models.SalesData).filter(
            models.SalesData.dish_name == request.dish_name,
            models.SalesData.outlet_id == request.outlet_id
        ).count()
        
        if data_count < min_data_points:
            # Queue background task to generate more data if needed
            background_tasks.add_task(
                generate_sample_data_if_needed,
                request.dish_name,
                request.outlet_id,
                min_data_points
            )
            
            # Return basic forecast with warning
            return ForecastResponse(
                dish_name=request.dish_name,
                outlet_id=request.outlet_id,
                model_name=request.model_name,
                forecast_date=datetime.now(),
                predictions=[],
                confidence_intervals=[],
                model_metrics={},
                feature_importance={},
                warnings=[f"Insufficient historical data ({data_count} days). Generating sample data..."],
                metadata={
                    "data_points": data_count,
                    "required_minimum": min_data_points
                }
            )
        
        # Generate forecast using selected model
        if request.model_name == "ensemble":
            forecast_result = await model_manager.generate_ensemble_forecast(
                dish_name=request.dish_name,
                outlet_id=request.outlet_id,
                horizon=request.forecast_horizon,
                include_confidence=request.include_confidence,
                external_factors=request.external_factors
            )
        else:
            forecast_result = await model_manager.generate_forecast(
                model_name=request.model_name,
                dish_name=request.dish_name,
                outlet_id=request.outlet_id,
                horizon=request.forecast_horizon,
                include_confidence=request.include_confidence,
                external_factors=request.external_factors
            )
        
        # Save forecast to database
        for i, prediction in enumerate(forecast_result["predictions"]):
            forecast_date = datetime.now() + timedelta(days=i+1)
            
            forecast_record = models.Forecast(
                forecast_date=forecast_date,
                dish_name=request.dish_name,
                outlet_id=request.outlet_id,
                model_name=request.model_name,
                predicted_quantity=prediction,
                confidence_lower=forecast_result.get("confidence_lower", [None] * len(forecast_result["predictions"]))[i],
                confidence_upper=forecast_result.get("confidence_upper", [None] * len(forecast_result["predictions"]))[i],
                model_version=forecast_result.get("model_version"),
                model_parameters=forecast_result.get("model_parameters"),
                feature_importance=forecast_result.get("feature_importance")
            )
            db.add(forecast_record)
        
        db.commit()
        
        # Create response
        response = ForecastResponse(
            dish_name=request.dish_name,
            outlet_id=request.outlet_id,
            model_name=request.model_name,
            forecast_date=datetime.now(),
            predictions=forecast_result["predictions"],
            confidence_intervals=list(zip(
                forecast_result.get("confidence_lower", []),
                forecast_result.get("confidence_upper", [])
            )) if request.include_confidence else [],
            model_metrics=forecast_result.get("metrics", {}),
            feature_importance=forecast_result.get("feature_importance", {}),
            shap_values=forecast_result.get("shap_values", {}),
            warnings=forecast_result.get("warnings", []),
            metadata={
                "model_version": forecast_result.get("model_version"),
                "training_samples": forecast_result.get("training_samples"),
                "forecast_generated_at": datetime.now().isoformat()
            }
        )
        
        # Cache the forecast
        await redis_client.cache_forecast(
            request.dish_name,
            request.outlet_id,
            response.dict(),
            ttl=3600  # 1 hour cache
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating forecast: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate forecast: {str(e)}")

@router.post("/batch", response_model=List[ForecastResponse])
async def generate_batch_forecasts(
    batch_request: ForecastBatch,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generate forecasts for multiple dish-outlet combinations"""
    try:
        forecasts = []
        
        for item in batch_request.items:
            try:
                forecast_request = ForecastRequest(
                    dish_name=item.dish_name,
                    outlet_id=item.outlet_id,
                    model_name=batch_request.model_name,
                    forecast_horizon=batch_request.forecast_horizon,
                    include_confidence=batch_request.include_confidence,
                    external_factors=batch_request.external_factors
                )
                
                forecast = await generate_forecast(
                    forecast_request, background_tasks, db, current_user
                )
                forecasts.append(forecast)
                
            except Exception as e:
                logger.error(f"Error in batch forecast for {item.dish_name}-{item.outlet_id}: {e}")
                # Add error forecast
                forecasts.append(ForecastResponse(
                    dish_name=item.dish_name,
                    outlet_id=item.outlet_id,
                    model_name=batch_request.model_name,
                    forecast_date=datetime.now(),
                    predictions=[],
                    confidence_intervals=[],
                    model_metrics={},
                    feature_importance={},
                    warnings=[f"Failed to generate forecast: {str(e)}"],
                    metadata={"error": True}
                ))
        
        return forecasts
        
    except Exception as e:
        logger.error(f"Error in batch forecast generation: {e}")
        raise HTTPException(status_code=500, detail=f"Batch forecast failed: {str(e)}")

@router.get("/history", response_model=List[ForecastResponse])
async def get_forecast_history(
    dish_name: str = Query(..., description="Dish name"),
    outlet_id: str = Query(..., description="Outlet ID"),
    model_name: Optional[str] = Query(None, description="Model name filter"),
    days: int = Query(30, description="Number of days to look back"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve historical forecasts for analysis"""
    try:
        query = db.query(models.Forecast).filter(
            models.Forecast.dish_name == dish_name,
            models.Forecast.outlet_id == outlet_id,
            models.Forecast.created_at >= datetime.now() - timedelta(days=days)
        )
        
        if model_name:
            query = query.filter(models.Forecast.model_name == model_name)
        
        forecasts = query.order_by(models.Forecast.created_at.desc()).all()
        
        return [
            ForecastResponse(
                dish_name=f.dish_name,
                outlet_id=f.outlet_id,
                model_name=f.model_name,
                forecast_date=f.created_at,
                predictions=[f.predicted_quantity],
                confidence_intervals=[(f.confidence_lower, f.confidence_upper)] if f.confidence_lower else [],
                model_metrics=f.model_parameters or {},
                feature_importance=f.feature_importance or {},
                metadata={
                    "forecast_id": f.id,
                    "model_version": f.model_version,
                    "actual_quantity": f.actual_quantity,
                    "absolute_error": f.absolute_error,
                    "percentage_error": f.percentage_error
                }
            )
            for f in forecasts
        ]
        
    except Exception as e:
        logger.error(f"Error retrieving forecast history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare-models", response_model=ModelComparison)
async def compare_models(
    dish_name: str,
    outlet_id: str,
    models_to_compare: List[str] = ["prophet", "xgboost", "lstm"],
    forecast_horizon: int = 7,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Compare performance of different ML models"""
    try:
        model_manager = ModelManager()
        comparison_results = {}
        
        for model_name in models_to_compare:
            try:
                forecast_result = await model_manager.generate_forecast(
                    model_name=model_name,
                    dish_name=dish_name,
                    outlet_id=outlet_id,
                    horizon=forecast_horizon,
                    include_confidence=True
                )
                
                comparison_results[model_name] = {
                    "predictions": forecast_result["predictions"],
                    "metrics": forecast_result.get("metrics", {}),
                    "feature_importance": forecast_result.get("feature_importance", {}),
                    "training_time": forecast_result.get("training_time", 0),
                    "inference_time": forecast_result.get("inference_time", 0)
                }
                
            except Exception as e:
                logger.error(f"Error with model {model_name}: {e}")
                comparison_results[model_name] = {"error": str(e)}
        
        # Calculate ensemble prediction
        valid_predictions = [
            result["predictions"] for result in comparison_results.values()
            if "predictions" in result and result["predictions"]
        ]
        
        ensemble_prediction = []
        if valid_predictions:
            for i in range(len(valid_predictions[0])):
                avg_pred = sum(pred[i] for pred in valid_predictions) / len(valid_predictions)
                ensemble_prediction.append(avg_pred)
        
        return ModelComparison(
            dish_name=dish_name,
            outlet_id=outlet_id,
            comparison_date=datetime.now(),
            models=comparison_results,
            ensemble_prediction=ensemble_prediction,
            best_model=min(
                comparison_results.keys(),
                key=lambda x: comparison_results[x].get("metrics", {}).get("mape", float('inf'))
            ) if comparison_results else None,
            metadata={
                "models_compared": len(comparison_results),
                "forecast_horizon": forecast_horizon
            }
        )
        
    except Exception as e:
        logger.error(f"Error in model comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/what-if", response_model=ForecastResponse)
async def what_if_analysis(
    scenario: WhatIfScenario,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Perform what-if analysis for different scenarios"""
    try:
        model_manager = ModelManager()
        
        # Apply scenario modifications
        external_factors = {
            "weather_impact": scenario.weather_multiplier,
            "event_impact": scenario.event_multiplier,
            "promotion_impact": scenario.promotion_multiplier,
            "price_change": scenario.price_change_percent,
            "scenario_name": scenario.scenario_name
        }
        
        # Generate forecast with modified factors
        forecast_result = await model_manager.generate_forecast(
            model_name=scenario.model_name,
            dish_name=scenario.dish_name,
            outlet_id=scenario.outlet_id,
            horizon=scenario.forecast_horizon,
            include_confidence=True,
            external_factors=external_factors
        )
        
        # Apply scenario multipliers to predictions
        modified_predictions = [
            pred * scenario.weather_multiplier * scenario.event_multiplier * scenario.promotion_multiplier
            for pred in forecast_result["predictions"]
        ]
        
        response = ForecastResponse(
            dish_name=scenario.dish_name,
            outlet_id=scenario.outlet_id,
            model_name=f"{scenario.model_name}_whatif",
            forecast_date=datetime.now(),
            predictions=modified_predictions,
            confidence_intervals=[],
            model_metrics=forecast_result.get("metrics", {}),
            feature_importance=forecast_result.get("feature_importance", {}),
            warnings=[f"What-if scenario: {scenario.scenario_name}"],
            metadata={
                "scenario": scenario.dict(),
                "base_predictions": forecast_result["predictions"],
                "applied_multipliers": {
                    "weather": scenario.weather_multiplier,
                    "event": scenario.event_multiplier,
                    "promotion": scenario.promotion_multiplier
                }
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error in what-if analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics", response_model=ForecastMetrics)
async def get_forecast_metrics(
    dish_name: str = Query(..., description="Dish name"),
    outlet_id: str = Query(..., description="Outlet ID"),
    model_name: str = Query(..., description="Model name"),
    days: int = Query(30, description="Evaluation period in days"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get forecast accuracy metrics for a specific model"""
    try:
        # Get forecasts with actual values
        forecasts = db.query(models.Forecast).filter(
            models.Forecast.dish_name == dish_name,
            models.Forecast.outlet_id == outlet_id,
            models.Forecast.model_name == model_name,
            models.Forecast.actual_quantity.isnot(None),
            models.Forecast.created_at >= datetime.now() - timedelta(days=days)
        ).all()
        
        if not forecasts:
            raise HTTPException(
                status_code=404,
                detail="No forecasts with actual values found for the specified criteria"
            )
        
        # Calculate metrics
        predictions = [f.predicted_quantity for f in forecasts]
        actuals = [f.actual_quantity for f in forecasts]
        
        mae = sum(abs(p - a) for p, a in zip(predictions, actuals)) / len(predictions)
        mape = sum(abs((a - p) / a) for p, a in zip(predictions, actuals) if a != 0) / len(predictions) * 100
        rmse = (sum((p - a) ** 2 for p, a in zip(predictions, actuals)) / len(predictions)) ** 0.5
        
        # Calculate bias and trend
        bias = sum(p - a for p, a in zip(predictions, actuals)) / len(predictions)
        
        return ForecastMetrics(
            dish_name=dish_name,
            outlet_id=outlet_id,
            model_name=model_name,
            evaluation_period_days=days,
            total_forecasts=len(forecasts),
            mae=mae,
            mape=mape,
            rmse=rmse,
            bias=bias,
            accuracy_percentage=max(0, 100 - mape),
            metadata={
                "evaluation_date": datetime.now().isoformat(),
                "forecast_dates": [f.forecast_date.isoformat() for f in forecasts[:5]]  # First 5 dates
            }
        )
        
    except Exception as e:
        logger.error(f"Error calculating forecast metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background task functions
async def generate_sample_data_if_needed(dish_name: str, outlet_id: str, min_points: int):
    """Background task to generate sample data if insufficient historical data"""
    try:
        # Queue Celery task for data generation
        celery_app.send_task(
            "app.ml.tasks.generate_sample_data",
            args=[dish_name, outlet_id, min_points]
        )
        logger.info(f"Queued sample data generation for {dish_name} at {outlet_id}")
    except Exception as e:
        logger.error(f"Error queuing sample data generation: {e}") 