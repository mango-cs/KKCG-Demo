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

# Custom CSS with enhanced styling
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
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #FF6B35;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-subtitle {
        font-size: 1.3rem;
        color: #E8F4FD;
        font-weight: 300;
        font-family: 'Inter', sans-serif;
        margin-bottom: 1rem;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255,107,53,0.2);
        border: 1px solid rgba(255,107,53,0.3);
    }
    
    .metric-card {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(255,107,53,0.2);
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
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .tool-button:hover {
        background: linear-gradient(145deg, #ff8660, #FF6B35);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,107,53,0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title { font-size: 2.5rem; }
        .main-subtitle { font-size: 1.1rem; }
        .feature-card { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_dashboard_data():
    """Load dashboard data from backend API ONLY"""
    client = get_api_client()
    
    try:
        # Get demand data from backend
        df = client.get_demand_data()
        
        if df.empty:
            st.warning("⚠️ **No data available**: Backend returned empty dataset")
            st.info("💡 **Tip**: Try seeding the database with sample data using the 'Seed Database' button below")
            return pd.DataFrame()
        
        return df
        
    except Exception as e:
        st.error(f"❌ **Data Loading Error**: {str(e)}")
        st.stop()

def create_summary_metrics(df):
    """Create beautiful summary metrics"""
    if df.empty:
        st.info("📊 **No metrics available**: Please seed the database or check data source")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_demand = df['predicted_demand'].sum()
    avg_demand = df['predicted_demand'].mean()
    peak_demand = df['predicted_demand'].max()
    unique_dishes = df['dish'].nunique() if 'dish' in df.columns else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #FF6B35; margin: 0;">📊 Total Demand</h3>
            <h2 style="color: #E8F4FD; margin: 0.5rem 0;">{total_demand:,}</h2>
            <p style="color: #A0A0A0; margin: 0;">Units across all outlets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #FF6B35; margin: 0;">📈 Avg Daily</h3>
            <h2 style="color: #E8F4FD; margin: 0.5rem 0;">{avg_demand:.0f}</h2>
            <p style="color: #A0A0A0; margin: 0;">Average per dish/day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #FF6B35; margin: 0;">🔥 Peak Demand</h3>
            <h2 style="color: #E8F4FD; margin: 0.5rem 0;">{peak_demand:,}</h2>
            <p style="color: #A0A0A0; margin: 0;">Highest single demand</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #FF6B35; margin: 0;">🍽️ Menu Items</h3>
            <h2 style="color: #E8F4FD; margin: 0.5rem 0;">{unique_dishes}</h2>
            <p style="color: #A0A0A0; margin: 0;">Active dishes</p>
        </div>
        """, unsafe_allow_html=True)

def create_demand_chart(df):
    """Create interactive demand visualization"""
    if df.empty:
        st.info("📈 **No chart data available**: Please seed the database to see demand trends")
        return
    
    # Aggregate data by date
    if 'date' in df.columns:
        daily_demand = df.groupby('date')['predicted_demand'].sum().reset_index()
        
        fig = px.line(
            daily_demand, 
            x='date', 
            y='predicted_demand',
            title="📈 Daily Demand Trends (Live Backend Data)",
            labels={'predicted_demand': 'Total Demand', 'date': 'Date'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=20,
            title_font_color='#FF6B35'
        )
        
        fig.update_traces(line_color='#FF6B35', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📅 **Date data not available**: Chart requires date column in backend data")

def main():
    """Enhanced main dashboard with backend-only integration"""
    
    # Header with backend status
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🍛 KKCG Analytics Dashboard</h1>
        <p class="main-subtitle">AI-Powered Restaurant Analytics for Kodi Kura Chitti Gaare</p>
        <p style="color: #BDC3C7; font-size: 1rem; margin-top: 1rem;">Live Backend Integration • Real-time Data • Professional Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Backend status and authentication section
    st.markdown("---")
    
    # Backend connection status
    show_backend_status()
    
    # Authentication section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if check_authentication():
            st.success(f"👤 **Logged in as:** {st.session_state.get('username', 'User')}")
            if st.button("🚪 Logout", use_container_width=True):
                logout()
        else:
            show_login_form()
    
    st.markdown("---")
    
    # Load and display data
    with st.spinner("🔄 Loading live data from backend..."):
        df = load_dashboard_data()
    
    if not df.empty:
        # Summary metrics
        st.markdown("### 📊 Live Performance Indicators")
        create_summary_metrics(df)
        
        st.markdown("---")
        
        # Demand visualization
        st.markdown("### 📈 Real-time Demand Analytics")
        create_demand_chart(df)
        
        st.markdown("---")
    else:
        # Show help when no data
        st.markdown("### 🎯 **Getting Started**")
        st.info("""
        **Welcome to KKCG Analytics Dashboard!**
        
        Your backend is connected but no data is available yet. Here's how to get started:
        
        1. **Seed Database**: Click the 'Seed Database' button below to populate with sample data
        2. **Explore Tools**: Use the analytics tools even with empty data to see the interface
        3. **Add Real Data**: Use the API endpoints to add your restaurant's actual data
        """)
    
    # Enhanced Analytics Tools Section
    st.markdown("### 🚀 Professional Analytics Tools")
    
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        st.markdown("""
        <div class="feature-card">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 style="color: #FF6B35; margin: 0;">AI Demand Forecasting</h3>
            </div>
            <p style="color: #E8F4FD; line-height: 1.6; margin-bottom: 1.5rem;">
                Advanced machine learning forecasting engine with real backend data. 
                Features seasonal analysis, confidence intervals, and AI-powered insights.
            </p>
            <div style="margin-bottom: 1rem;">
                <span style="background: #FF6B35; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🔗 Live Backend</span>
                <span style="background: #4CAF50; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🔮 ML Powered</span>
                <span style="background: #2196F3; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">📈 Real-time</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Forecasting Tool", use_container_width=True, type="primary"):
            st.switch_page("pages/Forecasting_Tool.py")
    
    with tool_col2:
        st.markdown("""
        <div class="feature-card">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔥</div>
                <h3 style="color: #FF6B35; margin: 0;">Interactive Heatmap Analytics</h3>
            </div>
            <p style="color: #E8F4FD; line-height: 1.6; margin-bottom: 1.5rem;">
                Dynamic heatmap visualization with live backend data integration. 
                Real-time performance analysis across dishes and outlets with AI insights.
            </p>
            <div style="margin-bottom: 1rem;">
                <span style="background: #FF6B35; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🎨 Interactive</span>
                <span style="background: #9C27B0; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🔍 Live Data</span>
                <span style="background: #FF9800; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">💡 AI Insights</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔥 Launch Heatmap Analytics", use_container_width=True, type="primary"):
            st.switch_page("pages/Heatmap_Comparison.py")
    
    st.markdown("---")
    
    # Platform Features section
    st.markdown("### ✨ Live Backend Features")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #2a2a3e, #3a3a4e); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔗</div>
            <h4 style="color: #FF6B35; margin-bottom: 1rem;">Live API Integration</h4>
            <p style="color: #E8F4FD; line-height: 1.5;">Direct connection to Railway-hosted backend with PostgreSQL database and real-time data synchronization.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #2a2a3e, #3a3a4e); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔐</div>
            <h4 style="color: #FF6B35; margin-bottom: 1rem;">JWT Authentication</h4>
            <p style="color: #E8F4FD; line-height: 1.5;">Secure user authentication with token-based access control and user management system.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #2a2a3e, #3a3a4e); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚡</div>
            <h4 style="color: #FF6B35; margin-bottom: 1rem;">Production Ready</h4>
            <p style="color: #E8F4FD; line-height: 1.5;">Enterprise-grade backend infrastructure with automatic scaling and professional deployment.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Backend management section
    st.markdown("---")
    st.markdown("### 🔧 Backend Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌱 Seed Database", help="Add sample data to the backend database"):
            client = get_api_client()
            with st.spinner("Seeding database with sample data..."):
                result = client.seed_database()
            if result["success"]:
                st.success(f"✅ {result['message']}")
                st.cache_data.clear()  # Clear cache to reload data
            else:
                st.error(f"❌ {result['error']}")
    
    with col2:
        if st.button("📊 View API Documentation", help="Open live API documentation"):
            client = get_api_client()
            st.success(f"**API Documentation**: [Open Live Docs]({client.base_url}/docs)")
    
    with col3:
        if st.button("🔄 Refresh Data", help="Clear cache and reload from backend"):
            st.cache_data.clear()
            st.success("✅ Data cache cleared! Reloading from backend...")
            st.rerun()
    
    # Backend API Information
    st.markdown("---")
    st.markdown("### 🌐 API Endpoints")
    
    client = get_api_client()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **🔗 Backend URL**: `{client.base_url}`
        
        **📋 Available Endpoints**:
        - `GET /health` - Backend health check
        - `POST /auth/login` - User authentication  
        - `POST /auth/register` - User registration
        - `GET /outlets` - Restaurant outlets
        - `GET /dishes` - Menu items
        - `GET /demand-data` - Historical demand data
        - `POST /seed-data` - Populate sample data
        """)
    
    with col2:
        st.markdown("""
        **🎯 Backend Features**:
        - ✅ PostgreSQL Database
        - ✅ JWT Authentication
        - ✅ RESTful API Design
        - ✅ Automatic Scaling
        - ✅ Real-time Data
        - ✅ Professional Deployment
        - ✅ Interactive Documentation
        - ✅ Error Handling
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666;">
        <h4 style="color: #FF6B35; margin-bottom: 1rem;">🍛 KKCG Analytics Platform</h4>
        <p style="margin: 0;">Production-grade restaurant analytics with live backend integration</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Powered by Streamlit • FastAPI • PostgreSQL • Railway Cloud</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 