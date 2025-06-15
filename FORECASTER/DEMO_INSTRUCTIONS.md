# 🍛 AI-Powered Restaurant Demand Forecasting - Demo Instructions

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Docker & Docker Compose installed
- 8GB+ RAM available
- Ports 3000, 5000, 8000, 8080, 9090, 3001 available

### 1. Clone and Start
```bash
# Clone the repository
git clone <your-repo-url>
cd KKCG

# Start the entire system (Linux/Mac)
./start.sh

# Or manually (Windows/All platforms)
docker-compose up -d
```

### 2. Access the Dashboard
- **Main Dashboard**: http://localhost:3000
- **Login**: admin / admin123

## 📊 Demo Walkthrough

### Dashboard Overview
1. **Real-time Metrics**: View live demand forecasts, revenue trends, and alert status
2. **Demand Heatmap**: Interactive visualization of dish demand across outlets and time
3. **Top Performing Dishes**: Real-time ranking of best-selling items
4. **Alert Panel**: Immediate notifications for inventory and demand anomalies

### Forecasting Features
1. **Navigate to Forecasting** (http://localhost:3000/forecasting)
2. **Select Parameters**:
   - Dish: Try "Masala Dosa" (popular breakfast item)
   - Outlet: "Chennai Central" (high traffic location)
   - Model: Prophet (with seasonality)
   - Horizon: 7 days
3. **View Results**:
   - Predictions with confidence intervals
   - SHAP explanations
   - Model performance metrics

### What-If Analysis
1. **Go to What-If Scenarios** (http://localhost:3000/what-if)
2. **Test Scenarios**:
   - **Festival Impact**: Set event multiplier to 1.8 for Diwali effect
   - **Rainy Day**: Set weather multiplier to 0.7 for monsoon impact
   - **Promotion**: Set promotion multiplier to 1.3 for discount effect
3. **Compare Results**: See how external factors affect demand predictions

### Model Comparison
1. **Access ML Models** section
2. **Compare Performance**:
   - Prophet: Best for seasonal patterns
   - XGBoost: Best for feature importance
   - LSTM: Best for complex sequences
3. **View Metrics**: MAE, MAPE, RMSE across different models

### Analytics Deep Dive
1. **Visit Analytics Page** (http://localhost:3000/analytics)
2. **Explore Patterns**:
   - Peak hours analysis (breakfast: 7-9 AM, lunch: 12-2 PM, dinner: 7-9 PM)
   - Weekend vs weekday patterns
   - Seasonal trends and festival impacts
3. **Revenue Analysis**: Profitability by dish, outlet, and time period

## 🎯 Key Demo Points

### Business Value
- **Inventory Optimization**: Reduce waste by 25-30% through accurate demand prediction
- **Staff Planning**: Optimize staffing based on predicted peak hours
- **Revenue Growth**: Identify high-demand periods for dynamic pricing
- **Cost Reduction**: Minimize ingredient spoilage and overstocking

### Technical Excellence
- **Real-time Processing**: Sub-200ms API responses with Redis caching
- **Scalable Architecture**: Microservices with Docker orchestration
- **ML Pipeline**: Automated model training, validation, and deployment
- **Monitoring**: Comprehensive system health and performance tracking

### Data Insights
- **40 South Indian Dishes**: From Dosa varieties to traditional sweets
- **5 Geographic Outlets**: Different traffic patterns and preferences
- **90 Days of Data**: Realistic patterns with seasonality and events
- **External Factors**: Weather, festivals, promotions impact modeling

## 🔧 System Components

### Frontend (Port 3000)
- **React 18** with Tailwind CSS
- **Interactive Charts** with Recharts
- **Real-time Updates** via WebSocket
- **Responsive Design** for mobile/tablet

### Backend (Port 8000)
- **FastAPI** with async processing
- **PostgreSQL** with TimescaleDB for time series
- **Redis** for caching and sessions
- **Celery** for background ML tasks

### ML Pipeline
- **Prophet**: Time series forecasting with holidays
- **XGBoost**: Gradient boosting with feature importance
- **LSTM**: Deep learning for sequential patterns
- **MLflow**: Experiment tracking and model registry

### Monitoring (Ports 9090, 3001)
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Airflow**: ML workflow orchestration
- **Health Checks**: Service status monitoring

## 📈 Sample Data Patterns

### Dish Categories
- **Rice Dishes**: High lunch demand (Sambar Rice, Rasam Rice)
- **Dosa Varieties**: Peak breakfast/dinner (Plain, Masala, Onion)
- **Beverages**: Steady throughout day (Filter Coffee, Tea)
- **Sweets**: Weekend and festival spikes (Payasam, Halwa)

### Outlet Characteristics
- **Chennai Central**: High traffic, premium pricing
- **Bangalore Koramangala**: Tech crowd, evening peaks
- **Hyderabad Banjara Hills**: Family dining, weekend focus
- **Coimbatore RS Puram**: Traditional, steady patterns
- **Kochi Marine Drive**: Tourist area, varied timing

### Seasonal Patterns
- **Monsoon (Jun-Sep)**: 30% demand drop on rainy days
- **Summer (Mar-May)**: 20% increase in beverages
- **Festival Days**: 50-80% demand spike
- **Weekends**: 20-40% higher than weekdays

## 🚨 Alert System Demo

### Inventory Alerts
- Navigate to Alerts section
- See low inventory warnings for high-demand dishes
- Review recommended reorder quantities

### Demand Spikes
- Weekend surge notifications
- Festival preparation alerts
- Unusual pattern detection

### Model Performance
- Accuracy degradation warnings
- Data drift detection
- Retraining recommendations

## 🔍 API Exploration

### Interactive API Docs
- Visit: http://localhost:8000/docs
- Test endpoints directly in browser
- View request/response schemas

### Key Endpoints
```bash
# Generate forecast
POST /api/v1/forecasts/generate

# Compare models
POST /api/v1/forecasts/compare-models

# What-if analysis
POST /api/v1/forecasts/what-if

# Get sales data
GET /api/v1/sales/data

# View alerts
GET /api/v1/alerts/active
```

## 📊 MLflow Integration

### Experiment Tracking
- Access: http://localhost:5000
- View model experiments and metrics
- Compare different algorithm runs
- Download trained models

### Model Registry
- Production model versioning
- A/B testing capabilities
- Performance monitoring over time

## ⚡ Airflow Workflows

### Access Airflow UI
- URL: http://localhost:8080
- Login: admin / admin

### Available DAGs
- **Daily Data Generation**: Simulate new sales data
- **Model Retraining**: Automated ML pipeline
- **Performance Monitoring**: Track model accuracy
- **Data Quality Checks**: Validate input data

## 🛠️ Troubleshooting

### Common Issues
1. **Port Conflicts**: Ensure ports 3000, 5000, 8000, 8080, 9090, 3001 are free
2. **Memory Issues**: Docker needs at least 8GB RAM
3. **Startup Time**: Initial startup takes 3-5 minutes for all services

### Useful Commands
```bash
# View all services status
docker-compose ps

# View logs for specific service
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Generate fresh data
docker-compose exec backend python ml_pipeline/data_simulation/generate_data.py

# Stop everything
docker-compose down
```

### Service Health Checks
- **Backend Health**: http://localhost:8000/health
- **Database**: Check via backend logs
- **Redis**: Check via backend logs
- **Frontend**: Should load React app

## 🎓 Learning Objectives

After this demo, you'll understand:
1. **Time Series Forecasting**: Prophet, ARIMA, and deep learning approaches
2. **Feature Engineering**: Creating predictive features from raw data
3. **Model Selection**: Comparing algorithms for different use cases
4. **Production ML**: Deploying and monitoring ML systems
5. **Business Intelligence**: Translating predictions into actionable insights

## 📞 Support

### Documentation
- **API Docs**: http://localhost:8000/docs
- **System Metrics**: http://localhost:9090
- **Monitoring**: http://localhost:3001

### Logs and Debugging
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend

# Real-time logs
docker-compose logs -f backend
```

---

**🎬 Ready to explore? Start with the main dashboard at http://localhost:3000!** 