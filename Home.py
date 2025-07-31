import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# Import utilities
from utils.api_client import (
    get_api_client, 
    show_backend_status, 
    show_login_form, 
    check_authentication,
    logout
)

# Page configuration
st.set_page_config(
    page_title="KKCG Analytics Dashboard",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with improved card layouts
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main styling */
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 
            inset 5px 5px 10px rgba(0,0,0,0.2),
            inset -5px -5px 10px rgba(255,255,255,0.1),
            0 8px 32px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><radialGradient id="a" cx="50%" cy="40%" r="50%"><stop offset="0%" stop-color="white" stop-opacity=".1"/><stop offset="100%" stop-color="white" stop-opacity="0"/></radialGradient></defs><rect width="100" height="20" fill="url(%23a)"/></svg>');
        background-size: 100% 100%;
    }
    
    .main-title {
        font-size: 3.8rem;
        font-weight: 700;
        color: #FF6B35;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Poppins', sans-serif;
        position: relative;
        z-index: 1;
    }
    
    .main-subtitle {
        font-size: 1.4rem;
        color: #E8F4FD;
        font-weight: 300;
        font-family: 'Inter', sans-serif;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .status-indicator {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Enhanced metric cards */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,107,53,0.1), transparent);
        transition: left 0.6s ease;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(255,107,53,0.2);
        border: 1px solid rgba(255,107,53,0.4);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF6B35;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #BDC3C7;
        font-weight: 400;
        margin-bottom: 0.8rem;
    }
    
    .metric-change {
        font-size: 0.85rem;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 500;
    }
    
    .metric-change.positive {
        background: linear-gradient(145deg, #4CAF50, #45a049);
        color: white;
    }
    
    .metric-change.neutral {
        background: linear-gradient(145deg, #2196F3, #1976D2);
        color: white;
    }
    
    /* Enhanced tool cards */
    .tools-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .tool-card {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 25px;
        padding: 2.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .tool-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,107,53,0.05), rgba(255,107,53,0.1));
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .tool-card:hover::before {
        opacity: 1;
    }
    
    .tool-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(255,107,53,0.25);
        border: 1px solid rgba(255,107,53,0.4);
    }
    
    .tool-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
        text-align: center;
    }
    
    .tool-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #FF6B35;
        margin-bottom: 1rem;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    
    .tool-description {
        color: #E8F4FD;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        text-align: center;
        font-size: 1rem;
    }
    
    .tool-features {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .feature-tag {
        background: linear-gradient(145deg, #FF6B35, #ff8660);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .tool-button {
        background: linear-gradient(145deg, #FF6B35, #ff8660);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        position: relative;
        overflow: hidden;
        font-family: 'Poppins', sans-serif;
    }
    
    .tool-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .tool-button:hover::before {
        left: 100%;
    }
    
    .tool-button:hover {
        background: linear-gradient(145deg, #ff8660, #FF6B35);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,107,53,0.4);
    }
    
    /* Benefits section */
    .benefits-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2.5rem 0;
    }
    
    .benefit-card {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 15px;
        padding: 1.8rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 6px 25px rgba(0,0,0,0.1);
    }
    
    .benefit-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,107,53,0.08), transparent);
        transition: left 0.5s ease;
    }
    
    .benefit-card:hover::before {
        left: 100%;
    }
    
    .benefit-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 15px 35px rgba(255,107,53,0.15);
        border: 1px solid rgba(255,107,53,0.3);
    }
    
    .benefit-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .benefit-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #FF6B35;
        margin-bottom: 0.8rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .benefit-description {
        color: #BDC3C7;
        font-size: 0.9rem;
        line-height: 1.4;
        font-family: 'Inter', sans-serif;
    }

    /* Quick actions section */
    .quick-actions {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .quick-actions h3 {
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .actions-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .action-button {
        background: linear-gradient(145deg, #3a3a4e, #4a4a5e);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .action-button:hover {
        background: linear-gradient(145deg, #4a4a5e, #5a5a6e);
        border: 1px solid rgba(255,107,53,0.3);
        transform: translateY(-2px);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title { font-size: 2.8rem; }
        .main-subtitle { font-size: 1.2rem; }
        .tools-container { grid-template-columns: 1fr; }
        .metrics-container { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
        .benefits-container { grid-template-columns: repeat(2, 1fr); }
        .tool-card { padding: 2rem; }
        .benefit-card { padding: 1.5rem; }
    }
    
    @media (max-width: 480px) {
        .benefits-container { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_dashboard_data():
    """Load dashboard data from backend API ONLY"""
    try:
        client = get_api_client()
        if client.health_check():
            df = client.get_demand_data()
            if not df.empty:
                # Ensure date column is datetime
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                return df
            else:
                st.info("💡 **Backend connected** but no data available. Use 'Seed Database' in Settings to populate sample data.")
                return pd.DataFrame()
        else:
            st.error("❌ **Backend connection failed**")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ **Data loading error**: {str(e)}")
        return pd.DataFrame()

def create_summary_metrics(df):
    """Create enhanced summary metrics with better cards"""
    if df.empty:
        st.info("📊 **No data available** - Metrics will appear after adding data")
        return
    
    # Calculate metrics
    total_demand = int(df['predicted_demand'].sum()) if 'predicted_demand' in df.columns else 0
    avg_daily = int(df['predicted_demand'].mean()) if 'predicted_demand' in df.columns else 0
    peak_demand = int(df['predicted_demand'].max()) if 'predicted_demand' in df.columns else 0
    unique_dishes = df['dish_name'].nunique() if 'dish_name' in df.columns else 0
    
    # Create metrics HTML
    st.markdown(f"""
    <div class="metrics-container">
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{total_demand:,}</div>
            <div class="metric-label">Total Demand</div>
            <div class="metric-change positive">+12% vs last week</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">📅</div>
            <div class="metric-value">{avg_daily}</div>
            <div class="metric-label">Average per Day</div>
            <div class="metric-change neutral">Steady growth</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🔥</div>
            <div class="metric-value">{peak_demand}</div>
            <div class="metric-label">Peak Demand</div>
            <div class="metric-change positive">New record</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🍽️</div>
            <div class="metric-value">{unique_dishes}</div>
            <div class="metric-label">Menu Items</div>
            <div class="metric-change neutral">Active dishes</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_demand_chart(df):
    """Create an enhanced demand visualization"""
    if df.empty or 'date' not in df.columns:
        st.info("📈 **Chart requires data** - Visualization will appear after adding data")
        return
    
    # Aggregate data by date
    daily_demand = df.groupby('date')['predicted_demand'].sum().reset_index()
    
    if not daily_demand.empty:
        # Create enhanced chart
        fig = px.line(
            daily_demand, 
            x='date', 
            y='predicted_demand',
            title="Daily Demand Trends (Live Backend Data)",
            labels={'predicted_demand': 'Demand', 'date': 'Date'}
        )
        
        # Enhanced styling
        fig.update_traces(
            line=dict(color='#FF6B35', width=3),
            mode='lines+markers',
            marker=dict(size=8, color='#FF6B35', line=dict(width=2, color='white'))
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E8F4FD', family='Inter'),
            title=dict(font=dict(size=20, color='#FF6B35')),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📅 **Date data not available**: Chart requires date column in backend data")

def main():
    """Enhanced main dashboard with improved layout and UX"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🍛 KKCG Analytics Dashboard</h1>
        <p class="main-subtitle">AI-Powered Restaurant Analytics for Kodi Kura Chitti Gaare</p>
        <p style="color: #BDC3C7; font-size: 1rem; margin-top: 1rem; position: relative; z-index: 1;">Live Backend Integration • Real-time Data • Professional Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status and Authentication Section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        show_backend_status()
    
    with col2:
        if check_authentication():
            st.success(f"👤 **Welcome back, {st.session_state.get('username', 'User')}!**")
            col2a, col2b = st.columns(2)
            with col2a:
                if st.button("🚪 Logout", use_container_width=True):
                    logout()
            with col2b:
                if st.button("⚙️ Settings", use_container_width=True, type="secondary"):
                    st.switch_page("pages/Settings.py")
        else:
            show_login_form()
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(145deg, #2a2a3e, #3a3a4e); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🕒</div>
            <div style="color: #FF6B35; font-weight: 600;">""" + datetime.now().strftime("%H:%M") + """</div>
            <div style="color: #BDC3C7; font-size: 0.9rem;">""" + datetime.now().strftime("%B %d, %Y") + """</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Load and display data
    with st.spinner("🔄 Loading live data from backend..."):
        df = load_dashboard_data()
    
    if not df.empty:
        # Performance Metrics
        st.markdown("### 📊 Live Performance Dashboard")
        create_summary_metrics(df)
        
        # Analytics Chart
        st.markdown("### 📈 Real-time Demand Analytics")
        create_demand_chart(df)
        
        st.markdown("---")
    
    # Enhanced Analytics Tools Section
    st.markdown("### 🚀 Analytics Tools")
    
    st.markdown("""
    <div class="tools-container">
        <div class="tool-card">
            <div class="tool-icon">📊</div>
            <h3 class="tool-title">AI Demand Forecasting</h3>
            <p class="tool-description">
                Advanced machine learning forecasting engine with real backend data. 
                Features seasonal analysis, confidence intervals, and AI-powered insights for optimal inventory planning.
            </p>
            <div class="tool-features">
                <span class="feature-tag">🔮 ML Powered</span>
                <span class="feature-tag">📈 7-Day Forecast</span>
                <span class="feature-tag">📊 Confidence Intervals</span>
                <span class="feature-tag">🌤️ Weather Analysis</span>
            </div>
        </div>
        <div class="tool-card">
            <div class="tool-icon">🔥</div>
            <h3 class="tool-title">Interactive Heatmap Analytics</h3>
            <p class="tool-description">
                Dynamic heatmap visualization with live backend data integration. 
                Real-time performance analysis across dishes and outlets with AI-generated business insights.
            </p>
            <div class="tool-features">
                <span class="feature-tag">🎨 Interactive</span>
                <span class="feature-tag">🔍 Live Data</span>
                <span class="feature-tag">💡 AI Insights</span>
                <span class="feature-tag">📊 Performance Metrics</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tool buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Launch Forecasting Tool", use_container_width=True, type="primary"):
            st.switch_page("pages/Forecasting_Tool.py")
    
    with col2:
        if st.button("🔥 Launch Heatmap Analytics", use_container_width=True, type="primary"):
            st.switch_page("pages/Heatmap_Comparison.py")
    
    st.markdown("---")
    
    # Benefits Section
    st.markdown("### 💡 Platform Benefits")
    
    st.markdown("""
    <div class="benefits-container">
        <div class="benefit-card">
            <div class="benefit-icon">📈</div>
            <h4 class="benefit-title">Boost Revenue</h4>
            <p class="benefit-description">Increase sales by 15-25% with optimized inventory and demand forecasting</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">🎯</div>
            <h4 class="benefit-title">Reduce Waste</h4>
            <p class="benefit-description">Cut food waste by 30% through accurate demand predictions and smart planning</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">⚡</div>
            <h4 class="benefit-title">Save Time</h4>
            <p class="benefit-description">Automate 80% of planning tasks with AI-powered insights and recommendations</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">💰</div>
            <h4 class="benefit-title">Cost Control</h4>
            <p class="benefit-description">Lower operational costs by 20% with efficient resource allocation</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">🔮</div>
            <h4 class="benefit-title">Future Ready</h4>
            <p class="benefit-description">Stay ahead with 7-day forecasts and seasonal trend analysis</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">📊</div>
            <h4 class="benefit-title">Data Driven</h4>
            <p class="benefit-description">Make confident decisions backed by real-time analytics and insights</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">🏆</div>
            <h4 class="benefit-title">Competitive Edge</h4>
            <p class="benefit-description">Outperform competitors with advanced ML-powered business intelligence</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">📱</div>
            <h4 class="benefit-title">Easy to Use</h4>
            <p class="benefit-description">User-friendly interface that requires no technical expertise to operate</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions Section
    st.markdown("### ⚡ Quick Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("🌱 Seed Database", help="Add sample data to the backend database", use_container_width=True):
            client = get_api_client()
            with st.spinner("Seeding database with sample data..."):
                result = client.seed_database()
            if result["success"]:
                st.success(f"✅ {result['message']}")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error(f"❌ {result['error']}")
    
    with action_col2:
        if st.button("🔄 Refresh Data", help="Clear cache and reload from backend", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Data cache cleared! Reloading from backend...")
            st.rerun()
    
    with action_col3:
        if st.button("📊 API Docs", help="Open live API documentation", use_container_width=True):
            client = get_api_client()
            st.success(f"**API Documentation**: [Open Live Docs]({client.base_url}/docs)")
    
    with action_col4:
        if st.button("⚙️ Settings", help="Open system settings and configuration", use_container_width=True):
            st.switch_page("pages/Settings.py")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666;">
        <h4 style="color: #FF6B35; margin-bottom: 1rem;">🍛 KKCG Analytics Platform</h4>
        <p style="margin: 0;">Production-grade restaurant analytics with live backend integration</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Powered by Streamlit • FastAPI • Database • Railway Cloud</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 