import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import utilities
from utils.api_client import (
    get_api_client, 
    show_backend_status, 
    check_authentication,
    logout
)
from utils.translations import t, create_language_selector

# Page configuration
st.set_page_config(
    page_title="⚙️ Settings - KKCG Analytics",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add language selector to sidebar
with st.sidebar:
    st.markdown("---")
    create_language_selector()
    st.markdown("---")

# Custom CSS for Settings page
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    .settings-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #FF6B35 0%, #ff8660 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255,107,53,0.2);
    }
    
    .settings-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .settings-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
        font-family: 'Inter', sans-serif;
    }
    
    .settings-section {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .settings-section h3 {
        color: #FF6B35;
        margin-bottom: 1rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    .info-card {
        background: linear-gradient(145deg, #1e1e2e, #2e2e3e);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,107,53,0.2);
        border-left: 4px solid #FF6B35;
    }
    
    .endpoint-item {
        background: rgba(255,107,53,0.1);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #FF6B35;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255,107,53,0.2);
        border: 1px solid rgba(255,107,53,0.3);
    }
    
    .metric-badge {
        background: linear-gradient(145deg, #FF6B35, #ff8660);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    """Settings page with comprehensive system management"""
    
    # Check authentication
    if not check_authentication():
        st.error(f"🔒 **{t('access_denied')}**: Please log in from the Home page to access Settings.")
        if st.button(f"🏠 {t('go_to_home')}", type="primary"):
            st.switch_page("Home.py")
        return
    
    # Header
    st.markdown(f"""
    <div class="settings-header">
        <h1 class="settings-title">⚙️ {t('system_settings')}</h1>
        <p class="settings-subtitle">{t('settings_subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Backend Status Section
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(f"### 🔗 {t('backend_connection_status')}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        client = get_api_client()
        status_info = client.get_connection_status()
        
        if status_info["color"] == "green":
            st.success(f"**{status_info['status']}** Database")
        elif status_info["color"] == "orange":
            st.warning(f"**{status_info['status']}** Mode")
        else:
            st.info(f"**{status_info['status']}** Status")
    
    with col2:
        if st.button(f"🔄 {t('test_connection')}", help="Test backend connectivity", use_container_width=True):
            if client.health_check():
                st.success(f"✅ {t('connection_verified')}!")
            else:
                st.error(f"❌ {t('connection_failed')}!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # User Management Section
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(f"### 👤 {t('user_management')}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.success(f"**{t('logged_in_as')}:** {st.session_state.get('username', 'User')}")
        st.info(f"**{t('session_started')}:** {st.session_state.get('login_time', 'Unknown')}")
    
    with col2:
        if st.button(f"🚪 {t('logout')}", type="secondary", use_container_width=True):
            logout()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Database Management Section
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(f"### 🗄️ {t('database_management')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🌱 {t('seed_database')}", help="Add sample data to the backend database", use_container_width=True):
            client = get_api_client()
            with st.spinner("Seeding database with sample data..."):
                result = client.seed_database()
            if result["success"]:
                st.success(f"✅ {result['message']}")
                st.cache_data.clear()
            else:
                st.error(f"❌ {result['error']}")
    
    with col2:
        if st.button(f"🔄 {t('refresh_data')}", help="Clear cache and reload from backend", use_container_width=True):
            st.cache_data.clear()
            st.success(f"✅ Data cache cleared! {t('refreshing_from_backend')}")
            st.rerun()
    
    with col3:
        if st.button("📊 API Documentation", help="Open live API documentation", use_container_width=True):
            client = get_api_client()
            st.success(f"**API Documentation**: [Open Live Docs]({client.base_url}/docs)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # API Configuration Section
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(f"### 🌐 {t('api_configuration')}")
    
    client = get_api_client()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <h4 style="color: #FF6B35; margin-bottom: 1rem;">🔗 {t('backend_information')}</h4>
            <p><strong>URL:</strong> <code>{client.base_url}</code></p>
            <p><strong>Status:</strong> <span class="metric-badge">🟢 Connected</span></p>
            <p><strong>Platform:</strong> Railway.app</p>
            <p><strong>Database:</strong> Production</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card">
            <h4 style="color: #FF6B35; margin-bottom: 1rem;">🛡️ {t('security_features')}</h4>
            <p>✅ JWT Authentication</p>
            <p>✅ HTTPS Encryption</p>
            <p>✅ CORS Protection</p>
            <p>✅ Input Validation</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # API Endpoints Section
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown("### 📋 Available API Endpoints")
    
    endpoints = [
        ("GET", "/health", "Backend health check"),
        ("POST", "/auth/login", "User authentication"),
        ("POST", "/auth/register", "User registration"),
        ("GET", "/outlets", "Restaurant outlets data"),
        ("GET", "/dishes", "Menu items data"),
        ("GET", "/demand-data", "Historical demand data"),
        ("POST", "/seed-data", "Populate sample data"),
        ("GET", "/docs", "Interactive API documentation"),
        ("GET", "/redoc", "Alternative API documentation")
    ]
    
    for method, endpoint, description in endpoints:
        color = "#4CAF50" if method == "GET" else "#FF9800"
        st.markdown(f"""
        <div class="endpoint-item">
            <span style="background: {color}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: bold;">{method}</span>
            <strong>{endpoint}</strong> - {description}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System Information Section
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown(f"### 📊 {t('system_information')}")
    
    # Feature grid
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    # Backend Features
    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: #FF6B35; margin-bottom: 1rem;">🏗️ {t('backend_architecture')}</h4>
        <p style="color: #E8F4FD; margin-bottom: 1rem;">{t('production_grade_infrastructure')}</p>
        <div>
            <span class="metric-badge">FastAPI</span>
            <span class="metric-badge">Database</span>
            <span class="metric-badge">Railway</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Frontend Features
    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: #FF6B35; margin-bottom: 1rem;">🎨 {t('frontend_stack')}</h4>
        <p style="color: #E8F4FD; margin-bottom: 1rem;">{t('modern_web_application')}</p>
        <div>
            <span class="metric-badge">Streamlit</span>
            <span class="metric-badge">Plotly</span>
            <span class="metric-badge">Pandas</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance Features
    st.markdown(f"""
    <div class="feature-card">
        <h4 style="color: #FF6B35; margin-bottom: 1rem;">⚡ {t('performance')}</h4>
        <p style="color: #E8F4FD; margin-bottom: 1rem;">{t('optimized_for_speed')}</p>
        <div>
            <span class="metric-badge">Caching</span>
            <span class="metric-badge">CDN</span>
            <span class="metric-badge">Auto-scaling</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Application Information
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown("### 📱 Application Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🏢 KKCG Analytics Platform**
        - **Version:** 2.0.0
        - **Environment:** Production
        - **Deployment:** Streamlit Cloud
        - **Last Updated:** December 2024
        """)
    
    with col2:
        st.markdown("""
        **🔧 Technical Specifications**
        - **Backend API:** 9 endpoints
        - **Database:** Production on Railway
        - **Authentication:** JWT tokens
        - **Real-time Updates:** ✅ Enabled
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0; color: #666;">
        <p style="margin: 0;">⚙️ System settings and configuration management</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Manage your KKCG Analytics system from this central dashboard</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 