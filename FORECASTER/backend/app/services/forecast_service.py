import random
from datetime import date, timedelta
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ForecastService:
    """Service for generating dummy forecasts with realistic predictions"""
    
    def __init__(self):
        # Base demand patterns for different dishes (South Indian restaurant)
        self.dish_base_demand = {
            "masala dosa": 180,
            "idli": 120,
            "sambar rice": 90,
            "filter coffee": 200,
            "vada": 80,
            "upma": 60,
            "curd rice": 70,
            "rasam rice": 85,
            "rava dosa": 140,
            "uttapam": 95
        }
        
        # Outlet location multipliers
        self.outlet_multipliers = {
            "chennai central": 1.3,
            "bangalore koramangala": 1.2,
            "hyderabad banjara hills": 1.1,
            "coimbatore": 0.9,
            "kochi": 0.8,
            "jubilee hills": 1.1
        }
        
        # Weather impact factors
        self.weather_factors = {
            "sunny": 1.0,
            "rainy": 0.8,
            "cloudy": 0.95,
            "stormy": 0.7
        }
        
        # Event impact factors
        self.event_factors = {
            "cricket finals": 1.4,
            "festival": 1.6,
            "holiday": 1.3,
            "normal": 1.0,
            "diwali": 1.8,
            "pongal": 1.7
        }
    
    def generate_forecast(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a dummy forecast with realistic patterns"""
        try:
            dish = request_data.get("dish", "").lower()
            outlet = request_data.get("outlet", "").lower()
            date_range = request_data.get("date_range", [])
            
            # Handle None values for optional parameters
            weather = request_data.get("weather")
            weather = weather.lower() if weather else "sunny"
            
            event = request_data.get("event")
            event = event.lower() if event else "normal"
            
            # Get base demand for the dish
            base_demand = self.dish_base_demand.get(dish, 100)
            
            # Apply outlet multiplier
            outlet_multiplier = self.outlet_multipliers.get(outlet, 1.0)
            
            # Apply weather factor
            weather_factor = self.weather_factors.get(weather, 1.0)
            
            # Apply event factor
            event_factor = self.event_factors.get(event, 1.0)
            
            forecasts = []
            
            for i, forecast_date in enumerate(date_range):
                if isinstance(forecast_date, str):
                    forecast_date = date.fromisoformat(forecast_date)
                
                # Day of week effect (weekends are busier)
                day_of_week_factor = 1.2 if forecast_date.weekday() >= 5 else 1.0
                
                # Add some daily variation
                daily_variation = random.uniform(0.85, 1.15)
                
                # Calculate predicted demand
                predicted_demand = int(
                    base_demand * 
                    outlet_multiplier * 
                    weather_factor * 
                    event_factor * 
                    day_of_week_factor * 
                    daily_variation
                )
                
                # Generate confidence bounds (±15%)
                confidence_range = int(predicted_demand * 0.15)
                lower_bound = max(0, predicted_demand - confidence_range)
                upper_bound = predicted_demand + confidence_range
                
                forecasts.append({
                    "date": forecast_date,
                    "predicted_demand": predicted_demand,
                    "lower_bound": lower_bound,
                    "upper_bound": upper_bound
                })
            
            # Generate dummy SHAP-style explanations
            explanations = {
                "weather": self._calculate_feature_impact(weather_factor),
                "event": self._calculate_feature_impact(event_factor),
                "day_of_week": self._calculate_feature_impact(
                    1.2 if any(date.fromisoformat(d) if isinstance(d, str) else d 
                             for d in date_range if (date.fromisoformat(d) if isinstance(d, str) else d).weekday() >= 5) 
                    else 1.0
                ),
                "outlet_location": self._calculate_feature_impact(outlet_multiplier),
                "seasonal_trend": random.uniform(-0.1, 0.2),
                "base_popularity": self._calculate_feature_impact(base_demand / 100)
            }
            
            logger.info(f"Generated forecast for {dish} at {outlet}: {len(forecasts)} predictions")
            
            return {
                "forecast": forecasts,
                "explanations": explanations,
                "metadata": {
                    "model_version": "dummy_v1.0",
                    "confidence_level": 0.85,
                    "features_used": list(explanations.keys())
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating forecast: {e}")
            raise
    
    def _calculate_feature_impact(self, factor: float) -> float:
        """Convert multiplier factor to SHAP-style contribution"""
        if factor > 1.0:
            return min(0.5, (factor - 1.0) * 0.8)
        elif factor < 1.0:
            return max(-0.5, (factor - 1.0) * 0.8)
        else:
            return 0.0 