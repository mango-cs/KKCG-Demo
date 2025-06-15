# 🍛 Restaurant Demand Forecasting Dashboard

## 📊 Overview

A comprehensive Streamlit dashboard for AI-powered restaurant demand forecasting. This interface connects to the FastAPI backend to provide real-time demand predictions for South Indian dishes across multiple outlets.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r ml_pipeline/requirements_streamlit.txt
```

### 2. Start the Backend (if not already running)
```bash
docker-compose up backend postgres redis -d
```

### 3. Launch Dashboard
```bash
streamlit run ml_pipeline/streamlit_demo.py --server.port 8501
```

### 4. Access Dashboard
Open [http://localhost:8501](http://localhost:8501) in your browser

## 🎛️ Dashboard Features

### **Sidebar Controls**
- **🍽️ Dish Selection**: Choose from 10 South Indian dishes
  - Masala Dosa, Idli, Filter Coffee, Sambar Rice, Vada, Upma, Curd Rice, Rasam Rice, Rava Dosa, Uttapam
- **🏪 Outlet Selection**: Pick from 6 restaurant locations
  - Chennai Central, Bangalore Koramangala, Hyderabad Banjara Hills, Coimbatore, Kochi, Jubilee Hills
- **📅 Date Range**: Select forecast period (up to 30 days)
- **🌤️ Weather** (Optional): Sunny, Rainy, Cloudy, Stormy
- **🎉 Events** (Optional): Cricket Finals, Festivals, Diwali, Pongal, Holidays

### **Interactive Visualizations**

#### **📈 Demand Forecast Chart**
- Line chart with demand predictions over time
- Shaded confidence interval bands (±15%)
- Interactive hover tooltips
- Professional styling with grid lines

#### **🧠 Feature Impact Analysis**
- Bar chart showing SHAP-style explanations
- Color-coded impacts (green = positive, red = negative)
- Feature contribution values
- Horizontal zero line for reference

### **Business Intelligence**

#### **📊 Key Metrics**
- **Total Forecasted Demand**: Sum across all forecast days
- **Average Daily Demand**: Mean daily units predicted
- **Peak Demand Day**: Highest predicted demand with date

#### **📋 Data Tables**
- **Forecast Summary**: Detailed daily predictions with bounds
- **Feature Explanations**: Impact scores for each factor

## 🔧 Technical Features

### **API Integration**
- **Live Connection**: Real-time data from FastAPI backend at `http://localhost:8000`
- **Error Handling**: Graceful fallback to sample data when backend is offline
- **Timeout Protection**: 10-second timeout for API requests
- **Status Feedback**: Clear success/error messages

### **User Experience**
- **Loading Spinners**: Visual feedback during API calls
- **Input Validation**: Date range and parameter validation
- **Expandable Sections**: Collapsible parameter review
- **Responsive Layout**: Two-column design for optimal viewing

### **Fallback Mode**
When the backend is unavailable, the dashboard automatically:
- Shows sample forecast data
- Displays warning message
- Provides instructions to start the backend
- Maintains full functionality for demonstration

## 📊 Sample Usage Scenarios

### **Scenario 1: Festival Planning**
- **Dish**: Masala Dosa
- **Outlet**: Chennai Central
- **Event**: Diwali
- **Expected**: 80% demand increase due to festival

### **Scenario 2: Weather Impact**
- **Dish**: Filter Coffee
- **Outlet**: Bangalore Koramangala
- **Weather**: Rainy
- **Expected**: 20% demand decrease due to weather

### **Scenario 3: Baseline Forecasting**
- **Dish**: Idli
- **Outlet**: Hyderabad Banjara Hills
- **Period**: Next 7 days
- **Expected**: Normal demand patterns with weekend peaks

## 🏗️ Architecture

```
User Interface (Streamlit)
          ↓
Dashboard (streamlit_demo.py)
          ↓
HTTP Request (requests)
          ↓
FastAPI Backend (:8000)
          ↓
Forecast Service
          ↓
Business Logic + SHAP Explanations
```

## 🎯 Business Value

### **Operational Benefits**
- **Inventory Planning**: Reduce waste by 25-30%
- **Staff Scheduling**: Optimize workforce allocation
- **Revenue Growth**: Dynamic pricing opportunities
- **Customer Satisfaction**: Avoid stock-outs

### **Decision Support**
- **Visual Insights**: Easy-to-understand charts
- **Factor Analysis**: Understand demand drivers
- **Scenario Planning**: Test different conditions
- **Data-Driven**: Move from intuition to analytics

## 🚨 Troubleshooting

### **Dashboard Won't Start**
```bash
# Check Python version (3.8+)
python --version

# Reinstall dependencies
pip install -r ml_pipeline/requirements_streamlit.txt

# Run dashboard
streamlit run ml_pipeline/streamlit_demo.py
```

### **API Connection Error**
```bash
# Check backend status
curl http://localhost:8000/health

# Start backend if needed
docker-compose up backend -d

# Check API endpoint
curl -X POST http://localhost:8000/api/v1/forecasts \
  -H "Content-Type: application/json" \
  -d '{"dish":"Masala Dosa","outlet":"Chennai Central","date_range":["2025-06-15"]}'
```

### **Port Already in Use**
```bash
# Use different port
streamlit run ml_pipeline/streamlit_demo.py --server.port 8502
```

## 🔮 Future Enhancements

- **Real-time Updates**: Auto-refresh forecasts
- **Historical Analysis**: Compare actual vs predicted
- **Multi-model Support**: Switch between Prophet, XGBoost, LSTM
- **Export Features**: Download forecasts as CSV/PDF
- **Advanced Filtering**: Custom date ranges and bulk operations
- **Alert System**: Notifications for unusual demand patterns

## 📝 Development Notes

### **File Structure**
```
ml_pipeline/
├── streamlit_demo.py           # Main dashboard application
├── requirements_streamlit.txt  # Python dependencies
└── README_DASHBOARD.md        # This documentation
```

### **Key Functions**
- `call_forecast_api()`: API communication
- `create_forecast_chart()`: Demand visualization
- `create_explanation_chart()`: Feature impact chart
- `get_sample_response()`: Fallback data

### **Dependencies**
- **streamlit**: Web interface framework
- **requests**: HTTP client for API calls
- **pandas**: Data manipulation
- **plotly**: Interactive charts
- **python-dateutil**: Date handling

---

🎉 **Ready to forecast restaurant demand with AI!** Open the dashboard and start exploring how different factors impact customer demand across your restaurant chain. 