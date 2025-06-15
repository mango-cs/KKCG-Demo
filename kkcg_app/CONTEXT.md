# 📊 KKCG Streamlit Dashboard - Context

## Purpose
This folder contains the **Streamlit frontend application** for the KKCG Analytics System. It provides an interactive web dashboard for restaurant analytics, demand forecasting, and business intelligence.

## 🏗️ Architecture

### Main Application
- **`Home.py`**: Landing page with navigation cards and system overview
- **`.streamlit/config.toml`**: Dark theme configuration and app settings

### Pages (`pages/`)
- **`Forecasting_Tool.py`**: AI-powered demand forecasting interface
- **`Heatmap_Comparison.py`**: Interactive analytics and KPI dashboard

### Utilities (`utils/`)  
- **`data_simulation.py`**: Generates realistic demo data for analytics
- **`heatmap_utils.py`**: Chart generation and visualization functions
- **`insights.py`**: Business intelligence and recommendation engine

## 🎨 UI Design System

### Color Scheme
- **Primary Background**: `#1a1a2e` (Dark blue)
- **Secondary Background**: `#2a2a3e` (Darker blue)
- **Accent Color**: `#FF6B35` (Saffron)
- **Text Colors**: `#E8F4FD` (Light blue), `#BDC3C7` (Gray)

### Typography
- **Headers**: Poppins font family
- **Body Text**: Inter font family  
- **Consistent Sizing**: Hierarchical font sizes for readability

### Layout Principles
- **Perfect Symmetry**: All column layouts use exact proportions
- **Consistent Heights**: Cards have uniform 240px height
- **Clean Spacing**: 1rem margins, proper text alignment
- **Professional Cards**: Dark theme with subtle borders and hover effects

## 🔧 Key Features

### Home Page
- **Hero Section**: Gradient background with system branding
- **Navigation Cards**: Clean 2-column layout for tool selection
- **Benefits Grid**: 3-column symmetric layout showcasing value
- **Statistics Display**: Platform metrics and capabilities

### Forecasting Tool
- **Parameter Controls**: Sidebar with dish/outlet/date selection
- **Status Monitoring**: Real-time backend connectivity display
- **Interactive Charts**: Dark-themed Plotly visualizations
- **SHAP Explanations**: ML model interpretability features
- **Export Options**: CSV and JSON download capabilities

### Heatmap Analytics
- **KPI Cards**: Clean 240px height cards with consistent spacing
- **Interactive Heatmaps**: Demand visualization across dimensions
- **Filtering System**: Advanced filtering and normalization
- **Business Insights**: AI-generated recommendations
- **Comparison Tools**: Performance analysis between outlets

## 🔄 Data Flow

### Input Sources
- **Live API**: Real-time data from FastAPI backend (when available)
- **Demo Data**: Simulated data for offline operation
- **User Parameters**: Interactive form inputs and filters

### Processing
- **Data Transformation**: Pandas-based data manipulation
- **Visualization**: Plotly chart generation with dark theme
- **Business Logic**: KPI calculations and insight generation

### Output
- **Interactive Dashboards**: Real-time updated visualizations
- **Export Files**: CSV and JSON data downloads
- **Status Feedback**: User notifications and system status

## 🎯 User Experience

### Navigation
- **Sidebar Navigation**: Streamlit's built-in page navigation
- **Status Indicators**: Real-time backend connectivity display
- **Refresh Controls**: Manual status checking capabilities

### Responsiveness
- **Adaptive Layout**: Responsive column layouts for different screen sizes
- **Loading States**: Spinners and progress indicators
- **Error Handling**: Graceful fallback to demo mode

### Performance
- **Caching**: Streamlit caching for data generation functions
- **Lazy Loading**: Components load as needed
- **Optimized Charts**: Efficient Plotly rendering

## 📦 Dependencies

### Core Framework
- **streamlit**: Web application framework
- **plotly**: Interactive charting library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

### Additional Libraries
- **requests**: HTTP client for API communication
- **datetime**: Date and time handling
- **json**: Data serialization

## 🔧 Configuration

### Streamlit Settings
- **Dark Theme**: Configured in `.streamlit/config.toml`
- **Port**: Default 8501 for dashboard access
- **Layout**: Wide mode for better screen utilization

### API Integration
- **Backend URL**: `http://localhost:8000` for FastAPI connection
- **Health Checks**: Automatic backend status monitoring
- **Timeout Handling**: Graceful fallback for connection issues

## 🚀 Deployment

### Local Development
```bash
cd kkcg_app
streamlit run Home.py --server.port 8501
```

### Production Considerations
- **Environment Variables**: API endpoints configurable
- **Logging**: Streamlit's built-in logging for debugging
- **Error Boundaries**: Comprehensive exception handling

## 📊 Current Status
- ✅ **Fully Functional**: All features working correctly
- ✅ **Professional UI**: Clean dark theme implementation
- ✅ **Status System**: Reliable backend connectivity monitoring
- ✅ **Export Features**: CSV and JSON download capabilities
- ✅ **Mobile Friendly**: Responsive design for various screen sizes

---
*Frontend dashboard providing intuitive access to restaurant analytics* 