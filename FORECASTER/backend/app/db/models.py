from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.core.database import Base

# Sales Data Model
class SalesData(Base):
    __tablename__ = "sales_data"
    
    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    dish_name = Column(String(100), nullable=False, index=True)
    outlet_id = Column(String(50), nullable=False, index=True)
    quantity_sold = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    weather = Column(String(50))
    event = Column(String(100))
    promotion_flag = Column(Boolean, default=False)
    
    # Calculated fields
    revenue = Column(Float)  # price * quantity_sold
    profit = Column(Float)   # revenue - (cost * quantity_sold)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Add indexes for better performance
    __table_args__ = (
        Index('idx_sales_datetime_dish_outlet', 'datetime', 'dish_name', 'outlet_id'),
        Index('idx_sales_datetime', 'datetime'),
        Index('idx_sales_dish_outlet', 'dish_name', 'outlet_id'),
    )

# Dish Master Data
class Dish(Base):
    __tablename__ = "dishes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    base_price = Column(Float, nullable=False)
    base_cost = Column(Float, nullable=False)
    description = Column(Text)
    ingredients = Column(JSON)  # List of ingredients
    preparation_time = Column(Integer)  # Minutes
    is_active = Column(Boolean, default=True)
    
    # Nutritional information
    calories = Column(Integer)
    is_vegetarian = Column(Boolean, default=True)
    is_vegan = Column(Boolean, default=False)
    spice_level = Column(String(20))  # Mild, Medium, Hot
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Outlet Master Data
class Outlet(Base):
    __tablename__ = "outlets"
    
    id = Column(Integer, primary_key=True, index=True)
    outlet_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    city = Column(String(50), nullable=False, index=True)
    state = Column(String(50), nullable=False)
    size = Column(String(20))  # small, medium, large
    foot_traffic = Column(String(20))  # low, medium, high
    
    # Operational details
    opening_hours = JSON  # {"monday": {"open": "06:00", "close": "23:00"}, ...}
    seating_capacity = Column(Integer)
    staff_count = Column(Integer)
    
    # Location coordinates
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Forecast Data
class Forecast(Base):
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    forecast_date = Column(DateTime, nullable=False, index=True)
    dish_name = Column(String(100), nullable=False, index=True)
    outlet_id = Column(String(50), nullable=False, index=True)
    model_name = Column(String(50), nullable=False, index=True)
    
    # Forecast values
    predicted_quantity = Column(Float, nullable=False)
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    confidence_level = Column(Float, default=0.95)
    
    # Actual values (filled when available)
    actual_quantity = Column(Float)
    absolute_error = Column(Float)
    percentage_error = Column(Float)
    
    # Model version and metadata
    model_version = Column(String(50))
    model_parameters = Column(JSON)
    feature_importance = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_forecast_date_dish_outlet', 'forecast_date', 'dish_name', 'outlet_id'),
        Index('idx_forecast_model', 'model_name', 'forecast_date'),
    )

# Model Registry
class ModelRegistry(Base):
    __tablename__ = "model_registry"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(50), nullable=False, index=True)
    model_type = Column(String(50), nullable=False)  # prophet, xgboost, lstm
    version = Column(String(50), nullable=False)
    
    # Model metadata
    parameters = Column(JSON)
    training_data_start = Column(DateTime)
    training_data_end = Column(DateTime)
    training_samples = Column(Integer)
    
    # Performance metrics
    mae = Column(Float)  # Mean Absolute Error
    mape = Column(Float)  # Mean Absolute Percentage Error
    rmse = Column(Float)  # Root Mean Square Error
    r2_score = Column(Float)  # R-squared
    
    # Model files
    model_path = Column(String(500))  # Path to saved model file
    model_size = Column(Integer)  # File size in bytes
    
    # Status
    is_active = Column(Boolean, default=True)
    is_production = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Alerts
class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50), nullable=False, index=True)  # inventory_low, demand_spike, etc.
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    
    # Alert details
    dish_name = Column(String(100), index=True)
    outlet_id = Column(String(50), index=True)
    message = Column(Text, nullable=False)
    description = Column(Text)
    
    # Alert data
    current_value = Column(Float)
    threshold_value = Column(Float)
    recommended_action = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String(100))
    acknowledged_at = Column(DateTime)
    
    # Resolution
    is_resolved = Column(Boolean, default=False)
    resolved_by = Column(String(100))
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# User Management
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile information
    full_name = Column(String(100))
    role = Column(String(50), default="user")  # admin, manager, analyst, user
    outlet_id = Column(String(50))  # Associated outlet
    
    # Permissions
    permissions = Column(JSON)  # List of permissions
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Login tracking
    last_login = Column(DateTime)
    login_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Feature Store
class FeatureStore(Base):
    __tablename__ = "feature_store"
    
    id = Column(Integer, primary_key=True, index=True)
    feature_name = Column(String(100), nullable=False, index=True)
    feature_type = Column(String(50), nullable=False)  # categorical, numerical, datetime
    
    # Feature metadata
    description = Column(Text)
    data_type = Column(String(50))
    source_table = Column(String(100))
    source_column = Column(String(100))
    transformation = Column(Text)  # SQL or Python code for feature generation
    
    # Feature statistics
    min_value = Column(Float)
    max_value = Column(Float)
    mean_value = Column(Float)
    std_value = Column(Float)
    null_count = Column(Integer)
    unique_count = Column(Integer)
    
    # Importance scores
    importance_prophet = Column(Float)
    importance_xgboost = Column(Float)
    importance_lstm = Column(Float)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Experiments (MLflow integration)
class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Experiment configuration
    model_type = Column(String(50), nullable=False)
    parameters = Column(JSON)
    tags = Column(JSON)
    
    # Results
    metrics = Column(JSON)
    status = Column(String(50), default="running")  # running, completed, failed
    
    # Artifacts
    artifacts_path = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Model Performance Tracking
class ModelPerformance(Base):
    __tablename__ = "model_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(50), nullable=False, index=True)
    evaluation_date = Column(DateTime, nullable=False, index=True)
    
    # Performance metrics
    mae = Column(Float)
    mape = Column(Float)
    rmse = Column(Float)
    r2_score = Column(Float)
    
    # Additional metrics
    accuracy_trend = Column(Float)  # Trend over time
    prediction_bias = Column(Float)
    seasonal_accuracy = Column(JSON)  # Accuracy by season/month
    
    # Data drift metrics
    feature_drift_score = Column(Float)
    target_drift_score = Column(Float)
    data_quality_score = Column(Float)
    
    # Evaluation details
    test_samples = Column(Integer)
    evaluation_period_start = Column(DateTime)
    evaluation_period_end = Column(DateTime)
    
    # Notes
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())

# Events and Holidays
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(100), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)  # festival, holiday, sports, promotion
    
    # Event details
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=False)
    description = Column(Text)
    
    # Impact
    expected_impact = Column(Float)  # Multiplier effect on demand
    actual_impact = Column(Float)
    
    # Scope
    is_national = Column(Boolean, default=False)
    is_regional = Column(Boolean, default=False)
    affected_outlets = Column(JSON)  # List of outlet IDs
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Inventory Tracking (for alert system)
class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    outlet_id = Column(String(50), nullable=False, index=True)
    ingredient_name = Column(String(100), nullable=False, index=True)
    
    # Inventory levels
    current_stock = Column(Float, nullable=False)
    minimum_stock = Column(Float, nullable=False)
    maximum_stock = Column(Float, nullable=False)
    reorder_point = Column(Float, nullable=False)
    
    # Units
    unit = Column(String(20))  # kg, liters, pieces, etc.
    
    # Cost information
    unit_cost = Column(Float)
    total_value = Column(Float)
    
    # Supplier information
    supplier_name = Column(String(100))
    lead_time = Column(Integer)  # Days
    
    # Last updated
    last_updated = Column(DateTime, default=func.now())
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_inventory_outlet_ingredient', 'outlet_id', 'ingredient_name'),
    ) 