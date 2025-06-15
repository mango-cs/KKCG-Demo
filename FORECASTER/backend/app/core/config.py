from pydantic_settings import BaseSettings
from pydantic import validator, Field
from typing import List, Optional, Any
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default="your-super-secret-key-change-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Database Configuration
    POSTGRES_SERVER: str = Field(default="localhost")  # Changed from "postgres" to "localhost"
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres123")
    POSTGRES_DB: str = Field(default="restaurant_forecasting")
    POSTGRES_PORT: str = Field(default="5432")
    DATABASE_URL: Optional[str] = None
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return (
            f"postgresql://{values.get('POSTGRES_USER')}:"
            f"{values.get('POSTGRES_PASSWORD')}@"
            f"{values.get('POSTGRES_SERVER')}:"
            f"{values.get('POSTGRES_PORT')}/"
            f"{values.get('POSTGRES_DB')}"
        )
    
    # Redis Configuration
    REDIS_HOST: str = Field(default="localhost")  # Changed from "redis" to "localhost"
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: Optional[str] = None
    REDIS_URL: Optional[str] = None
    
    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        password = values.get('REDIS_PASSWORD')
        if password:
            return f"redis://:{password}@{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}"
        return f"redis://{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0")  # Changed from redis to localhost
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0")  # Changed from redis to localhost
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    
    # MLflow Configuration
    MLFLOW_TRACKING_URI: str = Field(default="http://mlflow:5000")
    MLFLOW_EXPERIMENT_NAME: str = Field(default="restaurant_demand_forecasting")
    
    # Application Settings
    PROJECT_NAME: str = Field(default="Restaurant Demand Forecasting")
    VERSION: str = Field(default="1.0.0")
    DESCRIPTION: str = Field(default="AI-Powered Demand Forecasting System")
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")
    TIMEZONE: str = Field(default="Asia/Kolkata")
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = DATA_DIR / "models"
    FEATURES_DIR: Path = DATA_DIR / "features"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    
    # ML Configuration
    FEATURE_STORE_PATH: str = Field(default="/app/data/features")
    MODEL_REGISTRY_PATH: str = Field(default="/app/data/models")
    
    # Model Parameters
    PROPHET_SEASONALITY_MODE: str = Field(default="multiplicative")
    PROPHET_WEEKLY_SEASONALITY: bool = Field(default=True)
    PROPHET_YEARLY_SEASONALITY: bool = Field(default=True)
    PROPHET_DAILY_SEASONALITY: bool = Field(default=True)
    
    XGBOOST_N_ESTIMATORS: int = Field(default=100)
    XGBOOST_MAX_DEPTH: int = Field(default=6)
    XGBOOST_LEARNING_RATE: float = Field(default=0.1)
    
    LSTM_SEQUENCE_LENGTH: int = Field(default=24)  # 24 hours
    LSTM_EPOCHS: int = Field(default=50)
    LSTM_BATCH_SIZE: int = Field(default=32)
    
    # Data Simulation Parameters
    SIMULATION_START_DATE: str = Field(default="2024-01-01")
    SIMULATION_DAYS: int = Field(default=90)
    NUM_OUTLETS: int = Field(default=5)
    NUM_DISHES: int = Field(default=40)
    
    # Business Logic
    BUSINESS_HOURS_START: int = Field(default=6)  # 6 AM
    BUSINESS_HOURS_END: int = Field(default=23)   # 11 PM
    LUNCH_PEAK_START: int = Field(default=12)     # 12 PM
    LUNCH_PEAK_END: int = Field(default=14)       # 2 PM
    DINNER_PEAK_START: int = Field(default=19)    # 7 PM
    DINNER_PEAK_END: int = Field(default=21)      # 9 PM
    
    # Alert Thresholds
    LOW_INVENTORY_THRESHOLD: float = Field(default=0.2)  # 20% of average demand
    HIGH_DEMAND_THRESHOLD: float = Field(default=2.0)    # 200% of average demand
    MODEL_ACCURACY_THRESHOLD: float = Field(default=0.85) # 85% accuracy
    
    # External APIs (Mock)
    WEATHER_API_KEY: str = Field(default="mock_weather_api_key")
    EVENTS_API_KEY: str = Field(default="mock_events_api_key")
    
    # Security
    JWT_SECRET_KEY: str = Field(default="jwt-secret-key-change-in-production")
    ENCRYPTION_KEY: str = Field(default="encryption-key-32-chars-long!")
    
    # Monitoring
    PROMETHEUS_PORT: int = Field(default=9090)
    GRAFANA_PORT: int = Field(default=3001)
    
    # Rate Limiting
    API_RATE_LIMIT: str = Field(default="100/minute")
    ML_RATE_LIMIT: str = Field(default="10/minute")
    
    # Cache Settings
    CACHE_TTL: int = Field(default=300)  # 5 minutes
    FORECAST_CACHE_TTL: int = Field(default=3600)  # 1 hour
    
    # Model Training
    MODEL_RETRAIN_INTERVAL_HOURS: int = Field(default=24)  # Daily retraining
    MODEL_VALIDATION_SPLIT: float = Field(default=0.2)
    MODEL_TEST_SPLIT: float = Field(default=0.1)
    
    # Feature Engineering
    LAG_FEATURES: List[int] = Field(default=[1, 2, 3, 7, 14])  # Days
    ROLLING_WINDOW_SIZES: List[int] = Field(default=[3, 7, 14, 30])  # Days
    
    # Dish Categories (South Indian)
    DISH_CATEGORIES: dict = Field(default={
        "rice": ["Sambar Rice", "Rasam Rice", "Curd Rice", "Coconut Rice"],
        "dosa": ["Plain Dosa", "Masala Dosa", "Onion Dosa", "Ghee Dosa", "Paper Dosa"],
        "idli": ["Idli", "Button Idli", "Rava Idli"],
        "vada": ["Medu Vada", "Masala Vada", "Dahi Vada"],
        "sambar_rasam": ["Sambar", "Rasam", "Tomato Rasam", "Pepper Rasam"],
        "snacks": ["Bajji", "Bonda", "Murukku", "Mixture"],
        "sweets": ["Payasam", "Halwa", "Laddu", "Mysore Pak"],
        "beverages": ["Filter Coffee", "Tea", "Buttermilk", "Lassi"],
        "curries": ["Kootu", "Poriyal", "Aviyal", "Keerai"],
        "breads": ["Parotta", "Chapati", "Appam", "Uttapam"]
    })
    
    # Outlet Information
    OUTLETS: dict = Field(default={
        "outlet_1": {
            "name": "Chennai Central",
            "location": "Chennai, Tamil Nadu",
            "size": "large",
            "foot_traffic": "high"
        },
        "outlet_2": {
            "name": "Bangalore Koramangala",
            "location": "Bangalore, Karnataka", 
            "size": "medium",
            "foot_traffic": "medium"
        },
        "outlet_3": {
            "name": "Hyderabad Banjara Hills",
            "location": "Hyderabad, Telangana",
            "size": "large",
            "foot_traffic": "high"
        },
        "outlet_4": {
            "name": "Coimbatore RS Puram",
            "location": "Coimbatore, Tamil Nadu",
            "size": "small",
            "foot_traffic": "low"
        },
        "outlet_5": {
            "name": "Kochi Marine Drive",
            "location": "Kochi, Kerala",
            "size": "medium",
            "foot_traffic": "medium"
        }
    })
    
    # Festival and Event Calendar
    FESTIVALS_2024: dict = Field(default={
        "2024-01-15": "Pongal",
        "2024-01-26": "Republic Day",
        "2024-03-08": "Holi",
        "2024-04-14": "Tamil New Year",
        "2024-08-15": "Independence Day",
        "2024-09-07": "Ganesh Chaturthi",
        "2024-10-31": "Diwali",
        "2024-12-25": "Christmas"
    })
    
    # Weather Patterns (Simulated)
    WEATHER_PATTERNS: dict = Field(default={
        "monsoon_months": [6, 7, 8, 9],  # June to September
        "summer_months": [3, 4, 5],      # March to May
        "winter_months": [12, 1, 2],     # December to February
        "rainy_demand_impact": 0.7,      # 30% reduction
        "hot_weather_impact": 1.2,       # 20% increase
        "cool_weather_impact": 1.1       # 10% increase
    })
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories if they don't exist
        for path in [self.DATA_DIR, self.MODELS_DIR, self.FEATURES_DIR, 
                    self.RAW_DATA_DIR, self.PROCESSED_DATA_DIR]:
            path.mkdir(parents=True, exist_ok=True)

# Create global settings instance
settings = Settings() 