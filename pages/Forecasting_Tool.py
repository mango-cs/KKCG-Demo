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
    page_title="🔮 Demand Forecasting | KKCG",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the home page design
st.markdown("""
<style>
    /* Main styling to match home page */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 
            inset 5px 5px 10px rgba(0,0,0,0.2),
            inset -5px -5px 10px rgba(255,255,255,0.1);
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #FF6B35;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: #E8F4FD;
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean dark cards */
    .metric-card {
        background: #2a2a3e;
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: #3a3a4e;
        border: 1px solid rgba(255,107,53,0.2);
    }
    
    .insight-card {
        background: #2a2a3e;
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        background: #3a3a4e;
        border: 1px solid rgba(255,107,53,0.2);
    }
    
    /* Status indicators */
    .status-online {
        background: linear-gradient(145deg, #4CAF50, #45a049);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        border: none;
        box-shadow: 5px 5px 10px rgba(76,175,80,0.3);
    }
    
    .status-offline {
        background: linear-gradient(145deg, #F44336, #d32f2f);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        border: none;
        box-shadow: 5px 5px 10px rgba(244,67,54,0.3);
    }
    
    .status-demo {
        background: linear-gradient(145deg, #2196F3, #1976D2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        border: none;
        box-shadow: 5px 5px 10px rgba(33,150,243,0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Chart containers */
    .chart-container {
        background: #2a2a3e;
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        background: #3a3a4e;
        border: 1px solid rgba(255,107,53,0.2);
    }
</style>
""", unsafe_allow_html=True)

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
        fillcolor='rgba(255,107,53,0.15)',
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
        line=dict(color='#FF6B35', width=4),
        marker=dict(size=10, color='#FF6B35', line=dict(width=2, color='white')),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Demand: %{y} units<br>Range: %{customdata[0]}--%{customdata[1]}<extra></extra>',
        customdata=list(zip(lower_bound, upper_bound))
    ))
    
    fig.update_layout(
        title=dict(
            text="📈 Daily Demand Forecast",
            font=dict(size=20, color='#FF6B35'),
            x=0.5
        ),
        xaxis_title="Date",
        yaxis_title="Predicted Demand (Units)",
        hovermode='x unified',
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#2a2a3e',
        font=dict(size=12, color='#E8F4FD'),
        height=450,
        margin=dict(t=60, b=40, l=60, r=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#E8F4FD')
        )
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(255,255,255,0.1)',
        tickformat='%Y-%m-%d',
        tickfont=dict(color='#E8F4FD')
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(255,255,255,0.1)',
        zeroline=True,
        zerolinecolor='rgba(255,255,255,0.3)',
        zerolinewidth=1,
        tickfont=dict(color='#E8F4FD')
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
            font=dict(size=20, color='#FF6B35'),
            x=0.5
        ),
        xaxis_title="Features",
        yaxis_title="Impact Score",
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#2a2a3e',
        font=dict(size=12, color='#E8F4FD'),
        height=450,
        margin=dict(t=60, b=40, l=60, r=40)
    )
    
    fig.update_xaxes(
        showgrid=False,
        tickangle=45,
        tickfont=dict(color='#E8F4FD')
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='rgba(255,255,255,0.1)',
        zeroline=True,
        zerolinecolor='rgba(255,255,255,0.5)',
        zerolinewidth=2,
        tickfont=dict(color='#E8F4FD')
    )
    
    # Add horizontal line at y=0 with better styling for dark theme
    fig.add_hline(y=0, line_color="rgba(255,255,255,0.5)", line_width=2)
    
    return fig

def main():
    """Main Streamlit application"""
    
    # Header with beautiful styling
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🔮 AI-Powered Demand Forecasting</h1>
        <p class="main-subtitle">Predict demand for South Indian dishes across multiple outlets with ML precision</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top navigation bar with perfect symmetry
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("Home.py")
    
    with nav_col2:
        # Centered status indicators with equal spacing
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; padding: 1rem 0;">
        """, unsafe_allow_html=True)
        
        status_container = st.container()
        with status_container:
            status_col1, status_col2, status_col3 = st.columns([1, 1, 1])
            
            with status_col1:
                # Show status from session state (updated only when forecast is generated)
                if 'last_backend_check' not in st.session_state:
                    st.session_state.last_backend_check = "unknown"
                
                if st.session_state.last_backend_check == "online":
                    st.markdown('<div style="text-align: center;"><span class="status-online">🟢 Live Data</span></div>', unsafe_allow_html=True)
                elif st.session_state.last_backend_check == "offline":
                    st.markdown('<div style="text-align: center;"><span class="status-demo">🔄 Demo Mode</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="text-align: center;"><span class="status-demo">🚀 Ready</span></div>', unsafe_allow_html=True)
            
            with status_col2:
                st.markdown('<div style="text-align: center;"><span class="status-demo">📊 Demo Ready</span></div>', unsafe_allow_html=True)
            
            with status_col3:
                st.markdown('<div style="text-align: center;"><span class="status-demo">🤖 AI Enabled</span></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with nav_col3:
        # Add refresh button for backend status
        if st.button("🔄 Check Status", use_container_width=True):
            with st.spinner("Checking backend..."):
                try:
                    import requests
                    response = requests.get("http://localhost:8000/health", timeout=10)
                    st.info(f"Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.last_backend_check = "online"
                        st.success("✅ Backend is online!")
                        st.json(data)  # Show the response for debugging
                    else:
                        st.session_state.last_backend_check = "offline" 
                        st.error(f"❌ Backend error: {response.status_code}")
                        
                except requests.exceptions.ConnectionError as e:
                    st.session_state.last_backend_check = "offline"
                    st.error(f"❌ Connection Error: {str(e)}")
                except requests.exceptions.Timeout as e:
                    st.session_state.last_backend_check = "offline"
                    st.error(f"❌ Timeout Error: {str(e)}")
                except Exception as e:
                    st.session_state.last_backend_check = "offline"
                    st.error(f"❌ Error: {str(e)}")
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar for input controls
    st.sidebar.header("🎛️ Forecast Parameters")
    st.sidebar.markdown("Configure your demand forecasting parameters below:")
    
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
    
    # Generate forecast button with enhanced styling
    st.sidebar.markdown("---")
    generate_button = st.sidebar.button(
        "🚀 Generate Forecast",
        type="primary",
        use_container_width=True,
        help="Click to generate AI-powered demand forecast"
    )
    
    # System info in sidebar (no auto-refresh)
    with st.sidebar.expander("🔧 System Info", expanded=False):
        st.markdown("**Service Ports:**")
        st.markdown("• Frontend: Port 8501")
        st.markdown("• Backend: Port 8000")
        st.markdown("• API Docs: /docs")
        
        st.markdown("**Note:**")
        st.markdown("Status is shown in the main header above")
    
    # Quick tips in sidebar
    with st.sidebar.expander("💡 Quick Tips", expanded=False):
        st.markdown("""
        **🎯 Best Practices:**
        - Use 7-day forecasts for weekly planning
        - Consider weather for outdoor seating impact
        - Factor in local events and festivals
        - Compare different outlets for insights
        
        **📊 Reading Results:**
        - Confidence bands show uncertainty
        - SHAP values explain feature importance
        - Positive values increase demand
        - Negative values decrease demand
        
        **🔧 Troubleshooting:**
        - If backend shows offline, click "Refresh Status"
        - Wait 10-15 seconds after system startup
        - Demo mode works without backend connection
        """)
    
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
        
        # Show forecast parameters in a beautiful card
        with st.expander("📋 Forecast Parameters", expanded=False):
            param_col1, param_col2 = st.columns(2)
            with param_col1:
                st.markdown(f"""
                <div class="insight-card">
                    <h4>🍽️ Selection</h4>
                    <p><strong>Dish:</strong> {selected_dish}</p>
                    <p><strong>Outlet:</strong> {selected_outlet}</p>
                    <p><strong>Period:</strong> {len(date_range)} days</p>
                </div>
                """, unsafe_allow_html=True)
            with param_col2:
                st.markdown(f"""
                <div class="insight-card">
                    <h4>🌟 Factors</h4>
                    <p><strong>Weather:</strong> {weather or 'Not specified'}</p>
                    <p><strong>Event:</strong> {event or 'Normal'}</p>
                    <p><strong>Date Range:</strong> {start_date} to {end_date}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Make API call with loading spinner
        with st.spinner("🔄 Generating AI-powered forecast..."):
            forecast_data, error = call_forecast_api(
                selected_dish, selected_outlet, date_range, weather, event
            )
        
        # Handle API response
        if forecast_data:
            st.success("✅ Forecast generated successfully!")
            # Update backend status in session state
            st.session_state.last_backend_check = "online"
            
            # Display results in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                # Forecast chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                forecast_chart = create_forecast_chart(forecast_data["forecast"])
                st.plotly_chart(forecast_chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
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
                }).background_gradient(subset=['Predicted Demand'], cmap='Oranges')
                
                st.dataframe(styled_df, use_container_width=True)
            
            with col2:
                # Explanation chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                explanation_chart = create_explanation_chart(forecast_data["explanations"])
                st.plotly_chart(explanation_chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
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
            
            # Business insights with enhanced cards
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 1.8rem;">💡 Business Insights</h2>
                <p style="color: #BDC3C7; font-size: 1rem;">Key metrics and performance indicators for strategic decision making</p>
            </div>
            """, unsafe_allow_html=True)
            
            total_demand = sum(item["predicted_demand"] for item in forecast_data["forecast"])
            avg_daily_demand = total_demand / len(forecast_data["forecast"])
            max_demand_day = max(forecast_data["forecast"], key=lambda x: x["predicted_demand"])
            
            # Perfectly symmetric three-column layout for insights
            insight_col1, insight_col2, insight_col3 = st.columns([1, 1, 1], gap="large")
            
            metrics = [
                {
                    "icon": "📊",
                    "title": "Total Demand",
                    "value": f"{total_demand:,} units",
                    "subtitle": f"Over {len(date_range)} days"
                },
                {
                    "icon": "📈",
                    "title": "Avg Daily",
                    "value": f"{avg_daily_demand:.0f} units",
                    "subtitle": "Per day average"
                },
                {
                    "icon": "🔥",
                    "title": "Peak Day",
                    "value": f"{max_demand_day['predicted_demand']} units",
                    "subtitle": f"{max_demand_day['date']}"
                }
            ]
            
            for col, metric in zip([insight_col1, insight_col2, insight_col3], metrics):
                with col:
                    st.markdown(f"""
                    <div class="metric-card" style="height: 240px; display: flex; flex-direction: column; padding: 1rem;">
                        <div style="text-align: center; margin-bottom: 1rem;">
                            <div style="font-size: 2rem; margin-bottom: 0.6rem;">{metric["icon"]}</div>
                            <h3 style="color: #FF6B35; margin: 0; font-size: 0.95rem; text-align: center; line-height: 1.1; font-weight: 600;">{metric["title"]}</h3>
                        </div>
                        <div style="text-align: center; margin-bottom: 1rem;">
                            <h2 style="color: #E8F4FD; margin: 0 0 0.6rem 0; font-size: 1.05rem; text-align: center; line-height: 1.1; word-wrap: break-word; font-weight: 700;">{metric["value"]}</h2>
                            <p style="color: #BDC3C7; margin: 0; font-size: 0.8rem; text-align: center; line-height: 1.1;">{metric["subtitle"]}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Export options with perfect symmetry
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 1.8rem;">📥 Export Options</h2>
                <p style="color: #BDC3C7; font-size: 1rem;">Download your forecast data for further analysis</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Centered export buttons with equal spacing
            export_col1, export_spacer, export_col2 = st.columns([1, 0.5, 1])
            
            with export_col1:
                # Export forecast data
                forecast_df = pd.DataFrame(forecast_data["forecast"])
                csv_data = forecast_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Forecast CSV",
                    data=csv_data,
                    file_name=f"forecast_{selected_dish}_{selected_outlet}_{start_date}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with export_col2:
                # Export as JSON
                json_data = json.dumps(forecast_data, indent=2)
                st.download_button(
                    label="📄 Download Forecast JSON",
                    data=json_data,
                    file_name=f"forecast_{selected_dish}_{selected_outlet}_{start_date}.json",
                    mime="application/json",
                    use_container_width=True
                )
                
        else:
            # API failed - use sample data with improved messaging
            st.info("🔄 **Demo Mode Active** - Using sample data for demonstration")
            with st.expander("ℹ️ About Demo Mode", expanded=False):
                st.markdown(f"""
                **Why Demo Mode?**
                - The AI backend server is currently offline
                - This is normal for demonstration purposes
                - Sample data shows full functionality
                
                **Demo Features:**
                - ✅ Interactive forecasting charts
                - ✅ AI feature explanations (SHAP)
                - ✅ Business insights & metrics
                - ✅ Export capabilities
                
                **Technical Details:**
                - Backend Status: `{error}`
                - Sample Data: 7-day forecast with realistic patterns
                """)
                st.markdown("💡 **For Production**: Connect to live restaurant data and AI models")
            # Update backend status in session state
            st.session_state.last_backend_check = "offline"
            
            sample_data = get_sample_response()
            
            # Display sample results (same structure as above)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                forecast_chart = create_forecast_chart(sample_data["forecast"])
                st.plotly_chart(forecast_chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                explanation_chart = create_explanation_chart(sample_data["explanations"])
                st.plotly_chart(explanation_chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Welcome section with perfect symmetry
        st.markdown("""
        <div style="text-align: center; padding: 4rem 0; margin: 2rem 0;">
            <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 2.2rem; margin-bottom: 1.5rem;">Welcome to AI-Powered Demand Forecasting</h2>
            <p style="color: #BDC3C7; font-size: 1.2rem; max-width: 800px; margin: 0 auto; line-height: 1.6;">
                Configure your parameters in the sidebar and click "Generate Forecast" to get started with ML-powered demand predictions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights with perfect symmetry
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem 0;">
            <h3 style="color: #FF6B35; font-family: 'Poppins', sans-serif; font-size: 1.5rem;">🌟 Platform Features</h3>
        </div>
        """, unsafe_allow_html=True)
        
        feature_col1, feature_col2, feature_col3 = st.columns([1, 1, 1], gap="large")
        
        features = [
            {
                "icon": "🤖",
                "title": "Machine Learning",
                "description": "Advanced algorithms analyze patterns in your data to predict future demand with high accuracy."
            },
            {
                "icon": "🌤️",
                "title": "Weather & Events",
                "description": "Factor in weather conditions and special events to get more accurate forecasting results."
            },
            {
                "icon": "📊",
                "title": "Explainable AI",
                "description": "Understand why predictions are made with SHAP-style feature importance explanations."
            }
        ]
        
        for col, feature in zip([feature_col1, feature_col2, feature_col3], features):
            with col:
                st.markdown(f"""
                <div class="insight-card" style="height: 240px; display: flex; flex-direction: column; padding: 1rem;">
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.6rem;">{feature["icon"]}</div>
                        <h3 style="color: #FF6B35; margin: 0; font-size: 0.95rem; text-align: center; line-height: 1.1; font-weight: 600;">{feature["title"]}</h3>
                    </div>
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <p style="color: #E8F4FD; margin: 0; font-size: 0.8rem; text-align: center; line-height: 1.1;">{feature["description"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Call to action section
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0; padding: 2rem; background: linear-gradient(135deg, rgba(255,107,53,0.1), rgba(30,60,114,0.1)); border-radius: 15px; border: 1px solid rgba(255,107,53,0.2);">
            <h3 style="color: #FF6B35; margin-bottom: 1rem;">🚀 Ready to Start?</h3>
            <p style="color: #E8F4FD; margin: 0; font-size: 1.1rem;">Use the sidebar controls to configure your forecast parameters and generate predictions!</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 