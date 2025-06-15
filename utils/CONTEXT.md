# 🛠️ KKCG Dashboard Utilities - Context

## Purpose
This folder contains **utility modules** that provide core functionality for the KKCG Streamlit dashboard. These modules handle data generation, visualization, and business intelligence features.

## 📁 Module Overview

### `data_simulation.py`
**Purpose**: Generates realistic demo data for analytics and visualizations

**Key Functions**:
- `generate_demand_data()`: Creates comprehensive demand dataset
- `simulate_seasonal_patterns()`: Adds realistic seasonal variations
- `add_noise_and_outliers()`: Introduces realistic data variations
- `create_outlet_specific_patterns()`: Outlet-based demand characteristics

**Data Features**:
- **Time Range**: 7-day forecast periods
- **Dishes**: 40+ South Indian dishes with authentic names
- **Outlets**: 6 restaurant locations across South India
- **Realistic Patterns**: Seasonal trends, day-of-week variations
- **Business Logic**: Higher demand on weekends, festival impacts

### `heatmap_utils.py`
**Purpose**: Chart generation and visualization utilities for analytics dashboard

**Key Functions**:
- `generate_heatmap()`: Creates interactive demand heatmaps
- `generate_trend_chart()`: Time-series trend visualizations
- `generate_comparison_bar_chart()`: Outlet performance comparisons
- `apply_dark_theme()`: Consistent dark theme styling

**Visualization Features**:
- **Dark Theme Integration**: Matches app's `#1a1a2e` color scheme
- **Interactive Charts**: Plotly-based with hover details
- **Responsive Design**: Adapts to different screen sizes
- **Export Ready**: Charts optimized for data export

### `insights.py`
**Purpose**: Business intelligence engine and recommendation system

**Key Functions**:
- `compute_business_insights()`: Generates comprehensive KPI analysis
- `generate_insight_texts()`: Creates human-readable business insights
- `generate_recommendations()`: AI-powered business recommendations
- `identify_trends()`: Pattern recognition and trend analysis

**Analytics Capabilities**:
- **KPI Calculation**: Top performers, variability analysis
- **Trend Detection**: Peak patterns, seasonal identification
- **Risk Assessment**: Demand variability and consistency metrics
- **Business Recommendations**: Actionable insights for operations

## 🔧 Technical Implementation

### Data Generation (`data_simulation.py`)
```python
# Core data structure
def generate_demand_data() -> pd.DataFrame:
    # Creates realistic demand patterns
    # Includes seasonal, weekly, and random variations
    # Returns: DataFrame with dates, dishes, outlets, demand
```

**Features**:
- **Realistic Patterns**: Weekend peaks, seasonal variations
- **Outlet Diversity**: Location-specific performance characteristics
- **Dish Popularity**: Authentic South Indian dish preferences
- **Time Series**: Complete 7-day forecast datasets

### Visualization Engine (`heatmap_utils.py`)
```python
# Heatmap generation
def generate_heatmap(df, value_mode='total', normalize=False):
    # Creates interactive demand heatmaps
    # Supports aggregation modes and normalization
    # Returns: Plotly figure with dark theme
```

**Chart Types**:
- **Demand Heatmaps**: Dish vs Outlet demand visualization
- **Trend Charts**: Time-series demand patterns
- **Comparison Charts**: Performance analysis across dimensions
- **Dark Theme**: Consistent `#2a2a3e` backgrounds

### Business Intelligence (`insights.py`)
```python
# KPI computation
def compute_business_insights(df) -> dict:
    # Analyzes demand data for business metrics
    # Calculates performance indicators
    # Returns: Comprehensive insights dictionary
```

**Insight Categories**:
- **Performance Metrics**: Top dishes, outlets, peak periods
- **Variability Analysis**: Consistency and risk assessment  
- **Trend Identification**: Growth patterns and seasonality
- **Business Recommendations**: Actionable operational insights

## 📊 Data Structures

### Core Data Schema
```python
# Primary dataset structure
columns = [
    'date',           # Forecast date (YYYY-MM-DD)
    'dish',           # South Indian dish name
    'outlet',         # Restaurant location
    'predicted_demand' # Forecasted demand units
]
```

### Insights Output Format
```python
insights = {
    'top_dish': str,                    # Best performing dish
    'top_dish_demand': int,             # Peak demand value
    'top_outlet': str,                  # Leading outlet
    'top_outlet_demand': int,           # Outlet peak demand
    'peak_day': datetime,               # Highest demand date
    'peak_day_demand': int,             # Peak day total
    'most_consistent_dish': str,        # Lowest variability
    'most_unbalanced_dish': str,        # Highest variability
    'unbalance_coefficient': float,     # Variability metric
    'avg_demand_per_dish': float        # Average demand
}
```

## 🎨 Styling and Theming

### Color Palette
- **Primary Background**: `#1a1a2e` (Dark blue)
- **Secondary Background**: `#2a2a3e` (Darker blue)
- **Accent Color**: `#FF6B35` (Saffron)
- **Text Colors**: `#E8F4FD` (Light), `#BDC3C7` (Gray)

### Chart Styling
- **Plotly Themes**: Custom dark theme configurations
- **Grid Lines**: Subtle white gridlines with low opacity
- **Hover Effects**: Enhanced interactivity with tooltips
- **Responsive Layout**: Adapts to container dimensions

## 🔄 Integration Points

### With Streamlit Pages
- **Home.py**: Statistics display and overview metrics
- **Forecasting_Tool.py**: Real-time chart generation
- **Heatmap_Comparison.py**: Core analytics and KPI dashboard

### With Backend API
- **Data Fallback**: Demo data when API unavailable
- **Format Compatibility**: Matches FastAPI response structure
- **Real-time Updates**: Seamless integration with live data

## 📦 Dependencies

### Core Libraries
- **pandas**: DataFrame operations and data manipulation
- **numpy**: Numerical computing and statistical operations
- **plotly**: Interactive chart generation and visualization
- **datetime**: Date and time handling for time series

### Streamlit Integration
- **st.cache_data**: Performance optimization for data generation
- **Plotly Integration**: Native Streamlit chart rendering
- **Session State**: State management for user interactions

## 🚀 Performance Optimization

### Caching Strategy
- **Data Generation**: Cached to avoid repeated computation
- **Chart Creation**: Efficient rendering with Plotly
- **Insight Computation**: Cached business intelligence calculations

### Memory Management
- **Efficient DataFrames**: Optimized data structures
- **Lazy Loading**: Generate data only when needed
- **Resource Cleanup**: Proper memory management

## 📊 Current Status
- ✅ **Fully Functional**: All utility modules working correctly
- ✅ **Performance Optimized**: Caching and efficient algorithms
- ✅ **Dark Theme Compliant**: Consistent styling across all charts
- ✅ **Well Documented**: Clear function signatures and docstrings
- ✅ **Integration Ready**: Seamless integration with dashboard pages

---
*Utility modules providing core functionality for restaurant analytics dashboard* 