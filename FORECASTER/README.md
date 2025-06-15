# 🍛 AI-Powered Demand Forecasting System for South Indian Restaurant Chain

A comprehensive ML-driven demand forecasting platform that predicts dish demand across multiple restaurant outlets using advanced time series models and interactive dashboards.

## 🎯 Project Overview

This system simulates and forecasts demand for 40 South Indian dishes across 5 restaurant outlets using:
- **90 days** of simulated hourly sales data
- **3 ML models**: Prophet, XGBoost, and LSTM
- **Interactive dashboards** with real-time forecasting
- **What-if scenarios** for business planning
- **Alert system** for inventory management

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │────│  FastAPI Backend │────│   PostgreSQL    │
│   (Port 3000)   │    │   (Port 8000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────│     Redis       │──────────────┘
                        │   (Port 6379)   │
                        └─────────────────┘
                                 │
                    ┌─────────────────────────────┐
                    │      ML Pipeline            │
                    │  ┌─────────┬─────────────┐  │
                    │  │ Prophet │   XGBoost   │  │
                    │  │  Model  │    Model    │  │
                    │  └─────────┴─────────────┘  │
                    │  ┌─────────┬─────────────┐  │
                    │  │  LSTM   │   MLflow    │  │
                    │  │  Model  │  Tracking   │  │
                    │  └─────────┴─────────────┘  │
                    └─────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for development)
- Python 3.9+ (for development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd KKCG
cp .env.example .env
```

### 2. Start with Docker
```bash
# Start all services
docker-compose up -d

# Check services status
docker-compose ps
```

### 3. Access the Application
- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000
- **Airflow UI**: http://localhost:8080

### 4. Initialize Data
```bash
# Generate sample data and train models
docker-compose exec backend python -m app.ml.data_simulation.generate_data
docker-compose exec backend python -m app.ml.train_models
```

## 📊 Features

### 🔢 Data Simulation
- **40 South Indian dishes** (Dosa, Idli, Sambar, etc.)
- **5 restaurant outlets** across different locations
- **90 days** of hourly sales data
- **Realistic patterns**: weekend spikes, weather effects, festival impacts
- **External factors**: IPL matches, Pongal festival, monsoon effects

### 🤖 ML Models
1. **Prophet Model**
   - Holiday and weekly seasonality
   - Automatic trend detection
   - Confidence intervals

2. **XGBoost Model**
   - Feature importance analysis
   - External factor integration
   - SHAP value explanations

3. **LSTM Model**
   - Multivariate time series
   - Deep learning approach
   - Sequential pattern recognition

### 📈 Interactive Dashboard
- **Forecast Visualization**: Multi-line charts with confidence ribbons
- **Heatmap Matrix**: Dishes × Days × Outlets demand patterns
- **What-If Simulator**: Test scenarios (weather, festivals, promotions)
- **Alert System**: Low inventory warnings, demand spikes
- **Model Comparison**: A/B testing interface

### 🛠️ Advanced Features
- **Drift Detection**: Model performance monitoring
- **Feature Store**: Reusable ML pipeline components
- **Experiment Tracking**: MLflow integration
- **Workflow Orchestration**: Apache Airflow DAGs
- **Caching**: Redis for fast response times

## 🏛️ Tech Stack

### Frontend
- **React 18** with hooks and context
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Recharts** for interactive charts
- **React Query** for state management

### Backend
- **FastAPI** with async/await
- **PostgreSQL** with TimescaleDB extension
- **SQLAlchemy** ORM
- **Celery** for background tasks
- **Redis** for caching and task queue

### ML & Data
- **scikit-learn** for preprocessing
- **Prophet** for time series forecasting
- **XGBoost** for gradient boosting
- **TensorFlow/Keras** for LSTM
- **SHAP** for model explainability
- **MLflow** for experiment tracking

### DevOps
- **Docker** containers
- **Docker Compose** for orchestration
- **Apache Airflow** for workflows
- **Prometheus** for monitoring
- **Grafana** for metrics visualization

## 📁 Project Structure

```
KKCG/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── db/             # Database models
│   │   ├── ml/             # ML pipeline
│   │   └── main.py         # App entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── Dockerfile
├── ml_pipeline/            # ML workflows
│   ├── data_simulation/    # Data generation
│   ├── models/             # Model definitions
│   ├── feature_store/      # Feature engineering
│   └── airflow_dags/       # Workflow DAGs
├── data/                   # Data storage
├── monitoring/             # Monitoring configs
├── docker-compose.yml      # Service orchestration
├── .env.example           # Environment template
└── README.md              # This file
```

## 🎯 Use Cases

### 1. Daily Operations
- **Morning Planning**: Check today's demand forecast
- **Inventory Management**: Adjust procurement based on predictions
- **Staff Scheduling**: Optimize staffing for peak hours

### 2. Strategic Planning
- **Menu Optimization**: Identify high/low performing dishes
- **Seasonal Planning**: Prepare for festival seasons
- **Expansion Planning**: Analyze demand patterns for new outlets

### 3. Real-time Decisions
- **Dynamic Pricing**: Adjust prices based on demand
- **Promotion Timing**: Optimize promotional campaigns
- **Supply Chain**: Coordinate with suppliers

## 📈 Key Metrics

- **Forecast Accuracy**: MAPE < 15% for 7-day forecasts
- **Response Time**: API < 200ms, Dashboard < 2s
- **Availability**: 99.9% uptime
- **Scalability**: Support 100+ concurrent users

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### ML Pipeline Development
```bash
cd ml_pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python data_simulation/generate_data.py
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# ML pipeline tests
cd ml_pipeline
python -m pytest tests/
```

## 📊 Sample Data

The system generates realistic data including:
- **Dishes**: Masala Dosa, Plain Dosa, Idli, Vada, Sambar, Rasam, etc.
- **Outlets**: Chennai Central, Bangalore Koramangala, Hyderabad Banjara Hills, etc.
- **Events**: Pongal, Diwali, IPL Finals, Monsoon Season
- **Patterns**: Weekend spikes, lunch/dinner peaks, weather correlations

## 🔐 Security

- **Authentication**: JWT-based user authentication
- **Authorization**: Role-based access control
- **Data Protection**: Encrypted sensitive data
- **API Security**: Rate limiting and CORS protection

## 🚀 Deployment

### Production Deployment
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale backend=3
```

### Cloud Deployment (AWS/GCP/Azure)
- Use managed databases (RDS/Cloud SQL)
- Container orchestration (EKS/GKE/AKS)
- Load balancing and auto-scaling
- CI/CD pipeline integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🎬 Demo

For a live demo of the system:
1. Follow the Quick Start guide
2. Access the dashboard at http://localhost:3000
3. Navigate through the forecasting features
4. Try the what-if scenarios
5. Monitor the alert system

## 📞 Support

For questions or support:
- 📧 Email: support@restaurant-ai.com
- 📖 Documentation: https://docs.restaurant-ai.com
- 🐛 Issues: GitHub Issues page

---

**Built with ❤️ for South Indian restaurant chains** 