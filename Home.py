import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🍛 KKCG Analytics Dashboard",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for neumorphism design
st.markdown("""
<style>
    /* Main container styling */
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 
            20px 20px 60px #bebebe,
            -20px -20px 60px #ffffff;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 
            inset 5px 5px 10px rgba(0,0,0,0.2),
            inset -5px -5px 10px rgba(255,255,255,0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #FF6B35;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Poppins', sans-serif;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #E8F4FD;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Navigation cards */
    .nav-card {
        background: #2a2a3e;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        text-decoration: none;
        display: block;
        height: 100%;
    }
    
    .nav-card:hover {
        background: #3a3a4e;
        border: 1px solid rgba(255,107,53,0.3);
        transform: translateY(-5px);
    }
    
    .nav-card-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .nav-card-icon {
        font-size: 3rem;
        margin-right: 1rem;
        color: #FF6B35;
    }
    
    .nav-card-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #E8F4FD;
        margin: 0;
        font-family: 'Poppins', sans-serif;
    }
    
    .nav-card-description {
        color: #E8F4FD;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .nav-card-features {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .nav-card-features li {
        padding: 0.3rem 0;
        color: #BDC3C7;
        font-size: 0.95rem;
    }
    
    .nav-card-features li:before {
        content: "✅ ";
        margin-right: 0.5rem;
    }
    
    /* Benefits section */
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .benefit-card {
        background: #2a2a3e;
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .benefit-card:hover {
        background: #3a3a4e;
        border: 1px solid rgba(255,107,53,0.2);
    }
    
    .benefit-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #FF6B35;
    }
    
    .benefit-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #E8F4FD;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .benefit-text {
        color: #E8F4FD;
        font-size: 1rem;
        line-height: 1.5;
        font-family: 'Inter', sans-serif;
    }
    
    /* Stats section */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: #2a2a3e;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        background: #3a3a4e;
        border: 1px solid rgba(255,107,53,0.2);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FF6B35;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .stat-label {
        color: #E8F4FD;
        font-size: 1rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    
    /* CTA section */
    .cta-button {
        background: linear-gradient(145deg, #FF6B35, #FF8C42);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 
            10px 10px 20px rgba(255,107,53,0.3),
            -10px -10px 20px rgba(255,255,255,0.1);
    }
    
    .cta-button:hover {
        transform: translateY(-5px);
        box-shadow: 
            15px 15px 30px rgba(255,107,53,0.4),
            -15px -15px 30px rgba(255,255,255,0.2);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #7F8C8D;
        font-size: 0.9rem;
        border-top: 1px solid #E8E8E8;
        margin-top: 3rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    # Simple direct navigation - no session state needed
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🍛 Kodi Kura Chitti Gaare</h1>
        <p class="hero-subtitle">AI-Powered Analytics Dashboard for South Indian Restaurant Chain</p>
        <p style="color: #BDC3C7; font-size: 1.1rem;">Unlock the power of data-driven decision making with our comprehensive analytics platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif;">AI-Powered Restaurant Analytics</h2>
        <p style="color: #BDC3C7; font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.5;">
            Predict demand, optimize operations, and make data-driven decisions for your restaurant chain.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Deployment info for Community Cloud
    st.info("🚀 **Deployed on Streamlit Community Cloud** - This is a demo version showcasing AI-powered restaurant analytics capabilities.")
    
    # Debug section - Remove this after testing
    if st.button("🔄 Clear Cache & Reload", key="debug_clear"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    
    # Navigation Cards Section
    st.markdown("""
    <div style="margin: 4rem 0;">
        <h2 style='text-align: center; color: #E8F4FD; margin-bottom: 3rem; font-family: "Poppins", sans-serif; font-size: 2rem;'>🚀 Choose Your Analytics Tool</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Perfectly centered columns with equal spacing
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-header">
                <div class="nav-card-icon">🔮</div>
                <h3 class="nav-card-title">Demand Forecasting</h3>
            </div>
            <p class="nav-card-description">
                Predict future demand using AI algorithms with weather and event factors.
            </p>
            <ul class="nav-card-features">
                <li>7-day demand forecasting</li>
                <li>Weather & event analysis</li>
                <li>Interactive visualizations</li>
                <li>Export capabilities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔮 Launch Forecasting Tool", key="forecast_btn", use_container_width=True):
            st.switch_page("pages/Forecasting_Tool.py")
    
    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-header">
                <div class="nav-card-icon">🔥</div>
                <h3 class="nav-card-title">Demand Heatmap & Analytics</h3>
            </div>
            <p class="nav-card-description">
                Visualize demand patterns and compare performance across dishes and outlets.
            </p>
            <ul class="nav-card-features">
                <li>Interactive heatmaps</li>
                <li>Performance comparisons</li>
                <li>AI business insights</li>
                <li>Professional reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔥 Launch Heatmap Analytics", key="heatmap_btn", use_container_width=True):
            st.switch_page("pages/Heatmap_Comparison.py")
    
    # Key Benefits Section (Simplified)
    st.markdown("<h2 style='text-align: center; color: #E8F4FD; margin: 3rem 0 2rem 0; font-family: \"Poppins\", sans-serif;'>🎯 Key Benefits</h2>", unsafe_allow_html=True)
    
    benefits_html = """
    <div class="benefits-grid">
        <div class="benefit-card">
            <div class="benefit-icon">📊</div>
            <h3 class="benefit-title">Data-Driven Decisions</h3>
            <p class="benefit-text">Make informed decisions with AI-powered insights.</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">💰</div>
            <h3 class="benefit-title">Reduce Food Waste</h3>
            <p class="benefit-text">Optimize inventory with accurate forecasting.</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">⚡</div>
            <h3 class="benefit-title">Operational Efficiency</h3>
            <p class="benefit-text">Streamline operations with predictive analytics.</p>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon">🎯</div>
            <h3 class="benefit-title">Strategic Planning</h3>
            <p class="benefit-text">Identify trends and growth opportunities.</p>
        </div>
    </div>
    """
    st.markdown(benefits_html, unsafe_allow_html=True)
    
    # Key Statistics
    st.markdown("<h2 style='text-align: center; color: #E8F4FD; margin: 3rem 0 2rem 0; font-family: \"Poppins\", sans-serif;'>📈 Platform Statistics</h2>", unsafe_allow_html=True)
    
    stats_html = """
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">40+</div>
            <div class="stat-label">Authentic Dishes</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">6</div>
            <div class="stat-label">Outlet Locations</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">7</div>
            <div class="stat-label">Day Forecasts</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">95%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)
    
    # Simple Call to Action
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif;">Ready to Get Started?</h2>
        <p style="color: #BDC3C7; font-size: 1.1rem; margin-bottom: 2rem;">
            Choose a tool above and start analyzing your restaurant data.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🍛 <strong>Kodi Kura Chitti Gaare</strong> - Powered by AI & Analytics</p>
        <p>Built with ❤️ using Streamlit, Plotly, and advanced machine learning</p>
        <p><em>Deployed on Streamlit Community Cloud - """ + datetime.now().strftime("%B %Y") + """</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 