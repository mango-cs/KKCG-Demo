# 🔮 FORECASTER Backend System - Context

## Purpose
This folder contains the **FastAPI backend system** that powers the AI-driven demand forecasting capabilities of the KKCG Analytics System. It provides ML-powered predictions with explainable AI features and robust API endpoints.

## 🏗️ System Architecture

### Backend Application (`backend/`)
- **FastAPI Service**: High-performance async API server
- **ML Pipeline**: Demand forecasting models and data processing
- **Database Integration**: PostgreSQL for data persistence (optional)
- **Caching Layer**: Redis for performance optimization (optional)
- **Demo Mode**: Fully functional without external dependencies

### ML Pipeline (`ml_pipeline/`)
- **Data Processing**: Feature engineering and data transformation
- **Model Training**: Scikit-learn based ML algorithms
- **Prediction Engine**: Real-time demand forecasting
- **Explanation System**: SHAP-style feature importance analysis

## 🤖 ML Capabilities

### Demand Forecasting
- **Algorithm**: Ensemble methods with scikit-learn
- **Forecast Horizon**: 7-day predictions with confidence intervals
- **Input Features**:
  - Historical demand patterns
  - Weather conditions (Sunny, Rainy, Cloudy, Stormy)
  - Special events (Cricket Finals, Festivals, Holidays)
  - Day of week patterns
  - Outlet location factors
  - Seasonal trends

### Model Interpretability
- **SHAP Analysis**: Feature importance explanations
- **Confidence Intervals**: Prediction uncertainty quantification
- **Factor Impact**: Positive/negative contribution analysis
- **Business Insights**: Actionable recommendations

## 🔧 API Endpoints

### Core Functionality
- **`GET /health`**: System health check and status
- **`POST /api/v1/forecasts`**: Generate demand predictions
- **`GET /docs`**: Interactive API documentation (Swagger UI)
- **`GET /redoc`**: Alternative API documentation

### Forecast Request Format
```json
{
  "dish": "Masala Dosa",
  "outlet": "Chennai Central", 
  "date_range": ["2025-06-13", "2025-06-14", "2025-06-15"],
  "weather": "rainy",
  "event": "cricket_finals"
}
```

### Response Format
```json
{
  "forecast": [
    {
      "date": "2025-06-13",
      "predicted_demand": 180,
      "lower_bound": 153,
      "upper_bound": 207
    }
  ],
  "explanations": {
    "weather": -0.15,
    "event": 0.25,
    "day_of_week": 0.10,
    "outlet_location": 0.08,
    "seasonal_trend": 0.12,
    "base_popularity": 0.45
  }
}
```

## 🗃️ Data Model

### South Indian Dishes (10 items)
- Masala Dosa, Idli, Filter Coffee
- Sambar Rice, Vada, Upma
- Curd Rice, Rasam Rice, Rava Dosa, Uttapam

### Restaurant Outlets (6 locations)
- Chennai Central, Bangalore Koramangala
- Hyderabad Banjara Hills, Coimbatore
- Kochi, Jubilee Hills

### Contextual Factors
- **Weather**: Impact on customer footfall and preferences
- **Events**: Boost demand during special occasions
- **Seasonality**: Long-term trends and patterns
- **Location**: Outlet-specific performance characteristics

## ⚙️ Technical Implementation

### Backend Stack
- **FastAPI**: Modern, fast web framework for APIs
- **Uvicorn**: ASGI server for high-performance async operations
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: Database ORM (when using PostgreSQL)
- **Redis**: Caching and session management (optional)

### ML Stack
- **Scikit-learn**: Machine learning algorithms and preprocessing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and array operations
- **Joblib**: Model serialization and parallel processing

### Demo Mode Features
- **Standalone Operation**: Works without external databases
- **Sample Data**: Realistic demo data generation
- **Graceful Degradation**: Automatic fallback when services unavailable
- **Production Simulation**: Mimics real-world API behavior

## 🔄 Data Flow

### Request Processing
1. **Input Validation**: Pydantic models validate request data
2. **Feature Engineering**: Transform inputs into ML features
3. **Model Prediction**: Generate demand forecasts
4. **Explanation Generation**: Calculate SHAP-style feature importance
5. **Response Formatting**: Structure output for frontend consumption

### Error Handling
- **Graceful Failures**: Comprehensive exception handling
- **Fallback Mechanisms**: Demo data when services unavailable
- **Logging**: Detailed logging for debugging and monitoring
- **Health Checks**: Service status monitoring endpoints

## 🚀 Deployment

### Local Development
```bash
cd FORECASTER/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Support
- **Dockerfile**: Container configuration for backend service
- **Multi-stage Build**: Optimized production image
- **Environment Configuration**: Flexible deployment options

### Service Dependencies
- **PostgreSQL**: Optional database for data persistence
- **Redis**: Optional caching for performance optimization
- **External APIs**: Weather data integration (future enhancement)

## 📊 Performance Characteristics

### Response Times
- **Health Check**: <100ms typical response
- **Forecast Generation**: <2s for 7-day predictions
- **Batch Processing**: Efficient handling of multiple requests
- **Caching**: Significantly improved performance for repeated queries

### Scalability
- **Async Operations**: Non-blocking request handling
- **Horizontal Scaling**: Multiple instance support
- **Database Pooling**: Efficient connection management
- **Load Balancing**: Ready for production deployment

## 🔧 Configuration

### Environment Variables
- **Database Settings**: PostgreSQL connection parameters
- **Redis Settings**: Cache configuration options
- **API Settings**: CORS, security, and performance tuning
- **ML Parameters**: Model configuration and feature settings

### Demo Mode Settings
- **Automatic Detection**: Seamless fallback when dependencies unavailable
- **Sample Data Generation**: Realistic data patterns
- **Performance Simulation**: Mimics production API behavior

## 📊 Current Status
- ✅ **Fully Operational**: Complete ML forecasting pipeline
- ✅ **Demo Mode**: Works independently without external services
- ✅ **API Documentation**: Comprehensive Swagger/ReDoc documentation
- ✅ **Error Handling**: Robust exception handling and logging
- ✅ **Performance Optimized**: Fast response times and efficient processing
- ✅ **Production Ready**: Docker support and deployment configurations

---
*AI-powered backend providing intelligent demand forecasting for restaurant operations* 