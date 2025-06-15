from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ForecastRequest(BaseModel):
    dish: str
    outlet: str
    date_range: List[date]
    weather: Optional[str] = None
    event: Optional[str] = None

class ForecastItem(BaseModel):
    date: date
    predicted_demand: int
    lower_bound: int
    upper_bound: int

class ForecastExplanation(BaseModel):
    weather: float
    event: float
    day_of_week: float
    outlet_location: float = 0.0
    seasonal_trend: float = 0.0
    base_popularity: float = 0.0

class ForecastResponse(BaseModel):
    forecast: List[ForecastItem]
    explanations: ForecastExplanation 