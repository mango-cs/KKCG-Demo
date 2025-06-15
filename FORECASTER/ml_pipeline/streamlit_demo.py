import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import warnings
import numpy as np

# Suppress warnings for cleaner demo
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Page configuration
st.set_page_config(
    page_title="🍛 Restaurant Demand Forecasting",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_BASE_URL = "http://localhost:8000"
FORECAST_ENDPOINT = f"{API_BASE_URL}/api/v1/forecasts"

# South Indian dishes based on our backend implementation
DISHES = [
    "Masala Dosa",
    "Idli", 
    "Filter Coffee",
    "Sambar Rice",
    "Vada",
    "Upma",
    "Curd Rice",
    "Rasam Rice",
    "Rava Dosa",
    "Uttapam"
]

# Outlets based on our backend implementation
OUTLETS = [
    "Chennai Central",
    "Bangalore Koramangala", 
    "Hyderabad Banjara Hills",
    "Coimbatore",
    "Kochi",
    "Jubilee Hills"
]

# Weather options
WEATHER_OPTIONS = ["Sunny", "Rainy", "Cloudy", "Stormy"]

# Event options
EVENT_OPTIONS = [
    "Normal",
    "Cricket Finals", 
    "Festival",
    "Holiday",
    "Diwali",
    "Pongal"
]

def get_sample_response():
    """Fallback sample data when API is offline"""
    return {
        "forecast": [
            {"date": "2025-06-13", "predicted_demand": 180, "lower_bound": 153, "upper_bound": 207},
            {"date": "2025-06-14", "predicted_demand": 195, "lower_bound": 166, "upper_bound": 224},
            {"date": "2025-06-15", "predicted_demand": 220, "lower_bound": 187, "upper_bound": 253},
            {"date": "2025-06-16", "predicted_demand": 205, "lower_bound": 174, "upper_bound": 236},
            {"date": "2025-06-17", "predicted_demand": 190, "lower_bound": 162, "upper_bound": 218},
            {"date": "2025-06-18", "predicted_demand": 210, "lower_bound": 179, "upper_bound": 241},
            {"date": "2025-06-19", "predicted_demand": 235, "lower_bound": 200, "upper_bound": 270}
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

def call_forecast_api(dish, outlet, date_range, weather=None, event=None):
    """Call the FastAPI forecast endpoint"""
    try:
        # Prepare request payload
        payload = {
            "dish": dish,
            "outlet": outlet,
            "date_range": [date.strftime("%Y-%m-%d") for date in date_range],
            "weather": weather.lower() if weather and weather != "Sunny" else None,
            "event": event if event and event != "Normal" else None
        }
        
        # Make API request with timeout
        response = requests.post(
            FORECAST_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.ConnectionError:
        return None, "Connection Error: Backend server is not accessible"
    except requests.exceptions.Timeout:
        return None, "Timeout Error: API request took too long"
    except Exception as e:
        return None, f"Unexpected Error: {str(e)}"

def create_forecast_chart(forecast_data):
    """Create interactive line chart for demand forecast"""
    df = pd.DataFrame(forecast_data)
    
    # Fix datetime conversion to avoid FutureWarning
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    
    # Convert to numpy arrays to avoid pandas deprecation warnings
    dates = df['date'].values
    predicted_demand = df['predicted_demand'].values
    upper_bound = df['upper_bound'].values
    lower_bound = df['lower_bound'].values
    
    # Create line chart with confidence bands
    fig = go.Figure()
    
    # Add confidence band (fill area)
    fig.add_trace(go.Scatter(
        x=np.concatenate([dates, dates[::-1]]),
        y=np.concatenate([upper_bound, lower_bound[::-1]]),
        fill='toself',
        fillcolor='rgba(0,150,136,0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Confidence Interval'
    ))
    
    # Add predicted demand line
    fig.add_trace(go.Scatter(
        x=dates,
        y=predicted_demand,
        mode='lines+markers',
        name='Predicted Demand',
        line=dict(color='#1565C0', width=4),
        marker=dict(size=10, color='#1565C0', line=dict(width=2, color='white')),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Demand: %{y} units<br>Range: %{customdata[0]}--%{customdata[1]}<extra></extra>',
        customdata=list(zip(lower_bound, upper_bound))
    ))
    
    fig.update_layout(
        title=dict(
            text="📈 Daily Demand Forecast",
            font=dict(size=20, color='#1565C0'),
            x=0.5
        ),
        xaxis_title="Date",
        yaxis_title="Predicted Demand (Units)",
        hovermode='x unified',
        plot_bgcolor='rgba(248,250,252,0.8)',
        paper_bgcolor='white',
        font=dict(size=12),
        height=450,
        margin=dict(t=60, b=40, l=60, r=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(0,0,0,0.1)',
        tickformat='%Y-%m-%d'
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(0,0,0,0.1)',
        zeroline=True,
        zerolinecolor='rgba(0,0,0,0.3)',
        zerolinewidth=1
    )
    
    return fig

def create_explanation_chart(explanations):
    """Create bar chart for SHAP-style feature explanations"""
    features = list(explanations.keys())
    values = list(explanations.values())
    
    # Enhanced colors for better visual appeal
    colors = []
    for v in values:
        if v > 0:
            colors.append('#4CAF50')  # Green for positive
        elif v < 0:
            colors.append('#F44336')  # Red for negative
        else:
            colors.append('#9E9E9E')  # Gray for neutral
    
    # Format feature names for better display
    formatted_features = [f.replace('_', ' ').title() for f in features]
    
    fig = go.Figure(data=[
        go.Bar(
            x=formatted_features,
            y=values,
            marker_color=colors,
            marker_line=dict(width=1, color='rgba(0,0,0,0.3)'),
            text=[f"{v:+.3f}" for v in values],
            textposition='auto',
            textfont=dict(color='white', size=11, family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Impact: %{y:.3f}<br>' +
                         '<i>%{customdata}</i><extra></extra>',
            customdata=[
                'Increases demand' if v > 0 else 'Decreases demand' if v < 0 else 'Neutral'
                for v in values
            ]
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="🧠 Feature Impact Analysis (SHAP-style)",
            font=dict(size=20, color='#1565C0'),
            x=0.5
        ),
        xaxis_title="Features",
        yaxis_title="Impact Score",
        plot_bgcolor='rgba(248,250,252,0.8)',
        paper_bgcolor='white',
        font=dict(size=12),
        height=450,
        margin=dict(t=60, b=40, l=60, r=40)
    )
    
    fig.update_xaxes(
        showgrid=False,
        tickangle=45
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(0,0,0,0.1)',
        zeroline=True,
        zerolinecolor='rgba(0,0,0,0.5)',
        zerolinewidth=2
    )
    
    # Add horizontal line at y=0 with better styling
    fig.add_hline(y=0, line_color="rgba(0,0,0,0.5)", line_width=2)
    
    return fig

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🍛 AI-Powered Restaurant Demand Forecasting")
    st.markdown("**Predict demand for South Indian dishes across multiple outlets**")
    
    # Add status indicator
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("---")
    with col2:
        # Check API status
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                st.success("🟢 Backend Online")
            else:
                st.warning("🟡 Backend Issues")
        except:
            st.error("🔴 Backend Offline")
    with col3:
        st.info("📊 Demo Ready")
    
    st.markdown("---")
    
    # Sidebar for input controls
    st.sidebar.header("🎛️ Forecast Parameters")
    
    # Dish selection
    selected_dish = st.sidebar.selectbox(
        "🍽️ Select Dish:",
        options=DISHES,
        index=0,
        help="Choose a South Indian dish to forecast"
    )
    
    # Outlet selection
    selected_outlet = st.sidebar.selectbox(
        "🏪 Select Outlet:",
        options=OUTLETS,
        index=0,
        help="Choose the restaurant outlet location"
    )
    
    # Date range picker
    st.sidebar.subheader("📅 Forecast Period")
    today = datetime.now().date()
    default_end = today + timedelta(days=7)
    
    start_date = st.sidebar.date_input(
        "Start Date:",
        value=today,
        min_value=today,
        max_value=today + timedelta(days=30),
        help="Select forecast start date"
    )
    
    end_date = st.sidebar.date_input(
        "End Date:",
        value=default_end,
        min_value=start_date,
        max_value=today + timedelta(days=30),
        help="Select forecast end date"
    )
    
    # Optional parameters
    st.sidebar.subheader("🌟 Optional Factors")
    
    selected_weather = st.sidebar.selectbox(
        "🌤️ Weather Condition:",
        options=["None"] + WEATHER_OPTIONS,
        index=0,
        help="Select expected weather condition"
    )
    
    selected_event = st.sidebar.selectbox(
        "🎉 Special Event:",
        options=["None"] + EVENT_OPTIONS,
        index=0,
        help="Select any special event or festival"
    )
    
    # Generate forecast button
    st.sidebar.markdown("---")
    generate_button = st.sidebar.button(
        "🚀 Generate Forecast",
        type="primary",
        use_container_width=True
    )
    
    # Main content area
    if generate_button:
        # Validate date range
        if start_date >= end_date:
            st.error("❌ End date must be after start date!")
            return
        
        # Create date range
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        
        if len(date_range) > 30:
            st.error("❌ Maximum forecast period is 30 days!")
            return
        
        # Prepare parameters
        weather = selected_weather if selected_weather != "None" else None
        event = selected_event if selected_event != "None" else None
        
        # Show forecast parameters
        with st.expander("📋 Forecast Parameters", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Dish:** {selected_dish}")
                st.write(f"**Outlet:** {selected_outlet}")
                st.write(f"**Period:** {len(date_range)} days")
            with col2:
                st.write(f"**Weather:** {weather or 'Not specified'}")
                st.write(f"**Event:** {event or 'Normal'}")
                st.write(f"**Date Range:** {start_date} to {end_date}")
        
        # Make API call with loading spinner
        with st.spinner("🔄 Generating forecast..."):
            forecast_data, error = call_forecast_api(
                selected_dish, selected_outlet, date_range, weather, event
            )
        
        # Handle API response
        if forecast_data:
            st.success("✅ Forecast generated successfully!")
            st.balloons()  # Celebration animation
            
            # Display results in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                # Forecast chart
                forecast_chart = create_forecast_chart(forecast_data["forecast"])
                st.plotly_chart(forecast_chart, use_container_width=True)
                
                # Forecast summary table
                st.subheader("📊 Forecast Summary")
                df_forecast = pd.DataFrame(forecast_data["forecast"])
                df_forecast['date'] = pd.to_datetime(df_forecast['date']).dt.strftime('%Y-%m-%d')
                df_forecast.columns = ['Date', 'Predicted Demand', 'Lower Bound', 'Upper Bound']
                
                # Style the dataframe
                styled_df = df_forecast.style.format({
                    'Predicted Demand': '{:.0f}',
                    'Lower Bound': '{:.0f}',
                    'Upper Bound': '{:.0f}'
                }).background_gradient(subset=['Predicted Demand'], cmap='Blues')
                
                st.dataframe(styled_df, use_container_width=True)
            
            with col2:
                # Explanation chart
                explanation_chart = create_explanation_chart(forecast_data["explanations"])
                st.plotly_chart(explanation_chart, use_container_width=True)
                
                # Feature explanations
                st.subheader("🔍 Feature Explanations")
                explanations_data = []
                for k, v in forecast_data["explanations"].items():
                    impact_description = "Increases demand" if v > 0 else "Decreases demand" if v < 0 else "Neutral"
                    explanations_data.append({
                        "Feature": k.replace("_", " ").title(),
                        "Impact Score": f"{v:+.3f}",
                        "Effect": impact_description,
                        "Magnitude": abs(v)
                    })
                
                explanations_df = pd.DataFrame(explanations_data)
                explanations_df = explanations_df.sort_values('Magnitude', ascending=False)
                
                # Style the explanations table
                styled_explanations = explanations_df.drop('Magnitude', axis=1).style.apply(
                    lambda x: ['color: green' if '+' in str(x['Impact Score']) 
                              else 'color: red' if '-' in str(x['Impact Score'])
                              else 'color: gray' for _ in x], axis=1
                )
                
                st.dataframe(styled_explanations, use_container_width=True)
            
            # Business insights
            st.markdown("---")
            st.subheader("💡 Business Insights")
            
            total_demand = sum(item["predicted_demand"] for item in forecast_data["forecast"])
            avg_daily_demand = total_demand / len(forecast_data["forecast"])
            max_demand_day = max(forecast_data["forecast"], key=lambda x: x["predicted_demand"])
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                st.metric(
                    label="Total Forecasted Demand",
                    value=f"{total_demand} units",
                    delta=f"{len(date_range)} days"
                )
            
            with insight_col2:
                st.metric(
                    label="Average Daily Demand",
                    value=f"{avg_daily_demand:.0f} units/day"
                )
            
            with insight_col3:
                st.metric(
                    label="Peak Demand Day",
                    value=f"{max_demand_day['predicted_demand']} units",
                    delta=max_demand_day['date']
                )
                
        else:
            # API failed - use sample data
            st.warning(f"⚠️ API Error: {error}")
            st.info("📊 Showing sample forecast data as fallback")
            
            sample_data = get_sample_response()
            
            # Display sample results
            col1, col2 = st.columns(2)
            
            with col1:
                forecast_chart = create_forecast_chart(sample_data["forecast"])
                st.plotly_chart(forecast_chart, use_container_width=True)
            
            with col2:
                explanation_chart = create_explanation_chart(sample_data["explanations"])
                st.plotly_chart(explanation_chart, use_container_width=True)
            
            st.info("💡 This is sample data. Start the FastAPI backend to get real predictions!")
    
    else:
        # Welcome screen when no forecast is generated
        st.markdown("""
        ### 🎯 How to Use This Dashboard
        
        1. **Select Parameters** in the left sidebar:
           - Choose your dish and outlet
           - Set the forecast date range
           - Optionally specify weather and events
        
        2. **Click "Generate Forecast"** to get AI predictions
        
        3. **View Results**:
           - Line chart shows daily demand predictions
           - Bar chart explains which factors impact demand
           - Summary tables provide detailed numbers
        
        ### 🏪 Available Outlets
        """)
        
        # Display outlet information
        outlet_info = {
            "Chennai Central": "🏢 Major business district, high foot traffic",
            "Bangalore Koramangala": "💼 Tech hub, young professionals",
            "Hyderabad Banjara Hills": "🌟 Upscale area, affluent customers", 
            "Coimbatore": "🏭 Industrial city, traditional preferences",
            "Kochi": "⛵ Coastal city, diverse customer base",
            "Jubilee Hills": "🏡 Residential area, family-oriented"
        }
        
        for outlet, desc in outlet_info.items():
            st.write(f"**{outlet}:** {desc}")
        
        st.markdown("---")
        st.markdown("📡 **Backend Status:** Connect to `http://localhost:8000` for live predictions")

if __name__ == "__main__":
    main() 