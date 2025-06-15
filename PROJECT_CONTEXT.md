# 🍛 KKCG Analytics System - Project Context

## Overview
**Kodi Kura Chitti Gaare (KKCG) Analytics System** is a comprehensive AI-powered analytics platform for South Indian restaurant chain management. The system combines demand forecasting with business intelligence to help restaurant operators make data-driven decisions.

## 🏗️ System Architecture

### Frontend: Streamlit Dashboard (`kkcg_app/`)
- **Technology**: Streamlit, Plotly, Pandas
- **Purpose**: Interactive web dashboard for analytics and forecasting
- **Features**: Dark theme UI, real-time charts, KPI cards, export functionality

### Backend: FastAPI ML Service (`FORECASTER/`)
- **Technology**: FastAPI, scikit-learn, PostgreSQL, Redis
- **Purpose**: ML-powered demand forecasting API with SHAP explanations
- **Mode**: Demo mode (works without external dependencies)

## 📊 Core Features

### 1. AI-Powered Demand Forecasting
- **ML Models**: Scikit-learn based demand prediction
- **Factors**: Weather conditions, special events, seasonal trends
- **Output**: 7-day forecasts with confidence intervals
- **Explainability**: SHAP-style feature importance analysis

### 2. Interactive Heatmap Analytics  
- **Visualization**: Demand patterns across dishes and outlets
- **Comparison**: Performance analysis between locations
- **Insights**: AI-generated business recommendations
- **Filtering**: Advanced filtering and normalization options

### 3. Business Intelligence Dashboard
- **KPI Cards**: Key performance indicators with clean styling
- **Trend Analysis**: Time-series demand patterns
- **Export Options**: CSV and JSON data downloads
- **Professional UI**: Dark theme with saffron accent colors

## 🎯 Target Users
- **Restaurant Managers**: Daily operations and inventory planning
- **Chain Executives**: Multi-location performance analysis  
- **Data Analysts**: Advanced analytics and reporting
- **Operations Teams**: Demand forecasting and resource allocation

## 🚀 Quick Start
```bash
# Option 1: Full system (recommended)
.\start_kkcg_system.bat

# Option 2: Dashboard only
.\start_kkcg_app_only.bat

# Option 3: Interactive menu
.\launch_kkcg.bat
```

## 🔧 Technical Stack

### Frontend Technologies
- **Streamlit**: Web application framework
- **Plotly**: Interactive charting and visualization
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Backend Technologies  
- **FastAPI**: High-performance API framework
- **Uvicorn**: ASGI server for FastAPI
- **Scikit-learn**: Machine learning algorithms
- **PostgreSQL**: Database (optional, demo mode available)
- **Redis**: Caching layer (optional, demo mode available)

### UI/UX Design
- **Dark Theme**: Professional dark blue color scheme
- **Saffron Accent**: #FF6B35 primary color
- **Typography**: Poppins (headers) + Inter (body text)
- **Layout**: Symmetric, clean card-based design

## 📁 Project Structure
```
KKCG TOOLS/
├── kkcg_app/                 # Streamlit dashboard application
├── FORECASTER/               # FastAPI backend and ML pipeline  
├── *.bat                     # System startup/management scripts
├── PROJECT_CONTEXT.md        # This file - main project overview
└── README files              # Component-specific documentation
```

## 🎨 Current Status (June 2025)
- ✅ **Fully Functional**: Both frontend and backend working
- ✅ **Clean UI**: Professional dark theme with perfect symmetry
- ✅ **Reliable Backend**: Demo mode works without external dependencies
- ✅ **Status System**: Accurate backend connectivity detection
- ✅ **Export Features**: CSV and JSON data downloads
- ✅ **Production Ready**: Comprehensive error handling and fallbacks

## 🔄 System Management
- **Startup**: Automated batch files handle service orchestration
- **Status Monitoring**: Real-time backend connectivity checking
- **Error Handling**: Graceful fallback to demo mode when services unavailable
- **Logging**: Comprehensive logging for troubleshooting

## 💡 Business Value
- **Reduce Food Waste**: Accurate demand forecasting prevents over-preparation
- **Optimize Inventory**: Data-driven purchasing decisions
- **Improve Efficiency**: Identify peak patterns and staff accordingly
- **Strategic Planning**: Multi-location performance insights
- **Cost Reduction**: Better resource allocation and waste reduction

## 🔧 Maintenance Notes
- **Demo Mode**: System works independently without external databases
- **Scalability**: Designed for easy expansion to real data sources
- **Documentation**: Context files in each major component folder
- **Clean Code**: Professional, well-organized codebase with 2,400+ lines

---
*Built with ❤️ for data-driven restaurant success* 