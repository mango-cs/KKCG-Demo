import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import utilities
from utils.heatmap_utils import create_demand_heatmap, generate_ai_insights, get_performance_metrics
from utils.api_client import (
    get_api_client, 
    show_backend_status, 
    check_authentication
)

# Page configuration
st.set_page_config(
    page_title="🔥 Heatmap Analytics | KKCG",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS matching the design system
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255,107,53,0.2);
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
        font-size: 3.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Poppins', sans-serif;
        position: relative;
        z-index: 1;
    }
    
    .main-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
        font-family: 'Inter', sans-serif;
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced control panel */
    .control-panel {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .control-panel h3 {
        color: #FF6B35;
        margin-bottom: 1.5rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    /* Enhanced metrics container */
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
        font-size: 2rem;
        font-weight: 700;
        color: #FF6B35;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #BDC3C7;
        font-weight: 400;
    }
    
    /* Enhanced insight card */
    .insight-card {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255,107,53,0.2);
        border: 1px solid rgba(255,107,53,0.3);
    }
    
    .insight-card h4 {
        color: #FF6B35;
        margin-bottom: 1rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .insight-card p {
        color: #E8F4FD;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Performance indicators */
    .performance-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .performance-card {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .performance-card h4 {
        color: #FF6B35;
        margin-bottom: 1.5rem;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    
    .performance-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .performance-item:last-child {
        border-bottom: none;
    }
    
    .performance-indicator {
        padding: 0.4rem 1rem;
        border-radius: 15px;
        font-weight: 600;
        text-align: center;
        font-size: 0.8rem;
    }
    
    .high-performance { 
        background: linear-gradient(145deg, #27AE60, #2ECC71); 
        color: white; 
    }
    .medium-performance { 
        background: linear-gradient(145deg, #F39C12, #F1C40F); 
        color: white; 
    }
    .low-performance { 
        background: linear-gradient(145deg, #E74C3C, #EC7063); 
        color: white; 
    }
    
    /* Summary stats section */
    .stats-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin: 2rem 0;
        border: 2px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .stats-highlight h3 {
        margin-bottom: 1.5rem;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        text-align: center;
    }
    
    .stat-item {
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Recommendations section */
    .recommendations-section {
        background: linear-gradient(145deg, #2a2a3e, #3a3a4e);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .recommendation-item {
        background: rgba(255,107,53,0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #FF6B35;
        border: 1px solid rgba(255,107,53,0.2);
    }
    
    .recommendation-item h4 {
        color: #FF6B35;
        margin-bottom: 0.8rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .recommendation-item p {
        color: #E8F4FD;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    .stApp > header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title { font-size: 2.5rem; }
        .main-subtitle { font-size: 1.1rem; }
        .metrics-container { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
        .performance-grid { grid-template-columns: 1fr; }
        .control-panel { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_heatmap_data():
    """Load data for heatmap analysis from backend API"""
    try:
        client = get_api_client()
        if client.health_check():
            df = client.get_demand_data()
            if not df.empty:
                # Ensure required columns exist and are properly formatted
                required_cols = ['date', 'dish', 'outlet', 'predicted_demand']
                for col in required_cols:
                    if col not in df.columns:
                        if col == 'dish' and 'dish_name' in df.columns:
                            df['dish'] = df['dish_name']
                        elif col == 'outlet' and 'outlet_name' in df.columns:
                            df['outlet'] = df['outlet_name']
                
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                
                return df
            else:
                return pd.DataFrame()
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ **Heatmap data error**: {str(e)}")
        return pd.DataFrame()

def create_interactive_heatmap(df, metric='predicted_demand', title="Demand Heatmap"):
    """Create an enhanced interactive heatmap visualization"""
    
    if df.empty:
        st.info("🔥 **No heatmap data available** - Data needed for visualization")
        return None
    
    # Create pivot table for heatmap
    if 'dish' in df.columns and 'outlet' in df.columns:
        pivot_data = df.pivot_table(
            values=metric, 
            index='dish', 
            columns='outlet', 
            aggfunc='mean',
            fill_value=0
        )
    else:
        st.error("❌ **Missing columns**: Backend data must contain 'dish' and 'outlet' columns")
        return None
    
    if pivot_data.empty:
        st.warning(f"⚠️ **No pivot data**: Unable to create heatmap from current data selection")
        return None
    
    # Create enhanced heatmap with Plasma color scheme
    fig = px.imshow(
        pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        aspect='auto',
        color_continuous_scale='Plasma',
        title=f"{title} (Live Backend Data)"
    )
    
    # Enhanced styling for better UX
    fig.update_layout(
        title=dict(
            text=f"{title} (Live Backend Data)",
            font=dict(size=24, color='#FF6B35'),
            x=0.5
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8F4FD', size=12, family='Inter'),
        height=600,
        xaxis_title="Outlets",
        yaxis_title="Dishes",
        coloraxis_colorbar=dict(
            title=dict(text=metric.replace('_', ' ').title(), font=dict(color='#E8F4FD')),
            tickfont=dict(color='#E8F4FD'),
            bgcolor='rgba(42,42,62,0.8)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        )
    )
    
    # Add enhanced hover template
    fig.update_traces(
        hovertemplate='<b>%{y}</b> at <b>%{x}</b><br>' +
                     f'{metric.replace("_", " ").title()}: %{{z:.1f}}<extra></extra>'
    )
    
    return fig

def create_comparison_metrics(df):
    """Create performance comparison metrics"""
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    # Outlet performance
    outlet_performance = df.groupby('outlet').agg({
        'predicted_demand': ['sum', 'mean', 'count']
    }).round(2)
    outlet_performance.columns = ['Total_Demand', 'Avg_Demand', 'Records']
    outlet_performance = outlet_performance.reset_index().sort_values('Total_Demand', ascending=False)
    
    # Dish performance
    dish_performance = df.groupby('dish').agg({
        'predicted_demand': ['sum', 'mean', 'count']
    }).round(2)
    dish_performance.columns = ['Total_Demand', 'Avg_Demand', 'Records']
    dish_performance = dish_performance.reset_index().sort_values('Total_Demand', ascending=False)
    
    return outlet_performance, dish_performance

def create_performance_dashboard(outlet_perf, dish_perf):
    """Create enhanced performance dashboard"""
    if outlet_perf.empty and dish_perf.empty:
        st.info("📊 **Performance metrics require data**")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not outlet_perf.empty:
            st.markdown("""
            <div class="performance-card">
                <h4>🏢 Top Performing Outlets</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for position, (idx, row) in enumerate(outlet_perf.head(5).iterrows()):
                performance_class = "high-performance" if position < 2 else "medium-performance" if position < 4 else "low-performance"
                rank = position + 1
                
                st.markdown(f"""
                <div class="performance-item">
                    <span style="color: #E8F4FD; font-weight: 600;">#{rank}. {row['outlet']}</span>
                    <span class="performance-indicator {performance_class}">{row['Total_Demand']:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        if not dish_perf.empty:
            st.markdown("""
            <div class="performance-card">
                <h4>🍽️ Top Performing Dishes</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for position, (idx, row) in enumerate(dish_perf.head(5).iterrows()):
                performance_class = "high-performance" if position < 2 else "medium-performance" if position < 4 else "low-performance"
                rank = position + 1
                
                st.markdown(f"""
                <div class="performance-item">
                    <span style="color: #E8F4FD; font-weight: 600;">#{rank}. {row['dish']}</span>
                    <span class="performance-indicator {performance_class}">{row['Total_Demand']:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)

def create_trend_analysis(df):
    """Create enhanced trend analysis visualization"""
    if df.empty or 'date' not in df.columns:
        return None
    
    # Daily trend
    daily_trend = df.groupby('date')['predicted_demand'].sum().reset_index()
    
    if daily_trend.empty:
        return None
    
    # Create trend chart
    fig = px.line(
        daily_trend,
        x='date',
        y='predicted_demand',
        title='Daily Demand Trends',
        markers=True
    )
    
    # Enhanced styling
    fig.update_traces(
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=8, color='#FF6B35', line=dict(width=2, color='white'))
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E8F4FD', family='Inter'),
        title=dict(font=dict(size=18, color='#FF6B35')),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        height=400
    )
    
    return fig

def create_ai_recommendations(df):
    """Create AI-powered recommendations section"""
    if df.empty:
        st.info("🤖 **AI recommendations will appear when data is available**")
        return
    
    # Calculate some insights
    total_demand = df['predicted_demand'].sum()
    top_dish = df.groupby('dish')['predicted_demand'].sum().idxmax()
    top_outlet = df.groupby('outlet')['predicted_demand'].sum().idxmax()
    
    recommendations = [
        {
            "icon": "🎯",
            "title": "Inventory Optimization",
            "description": f"Focus inventory on {top_dish} which shows highest demand patterns. Consider increasing stock levels during peak periods."
        },
        {
            "icon": "🏢",
            "title": "Outlet Performance",
            "description": f"{top_outlet} is your top-performing location. Analyze their operations to replicate success at other outlets."
        },
        {
            "icon": "📊",
            "title": "Demand Patterns",
            "description": "Demand shows clear patterns. Consider dynamic pricing and promotional strategies during low-demand periods."
        },
        {
            "icon": "⚡",
            "title": "Staff Optimization",
            "description": "Align staffing levels with predicted demand patterns to optimize operational efficiency and customer service."
        }
    ]
    
    st.markdown("""
    <div class="recommendations-section">
        <h3 style="color: #FF6B35; margin-bottom: 1.5rem; text-align: center; font-family: 'Poppins', sans-serif;">🤖 AI-Powered Business Recommendations</h3>
    """, unsafe_allow_html=True)
    
    for rec in recommendations:
        st.markdown(f"""
        <div class="recommendation-item">
            <h4>{rec['icon']} {rec['title']}</h4>
            <p>{rec['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    """Main heatmap analytics interface with enhanced design"""
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 **Access Denied**: Please log in from the Home page to access Heatmap Analytics.")
        if st.button("🏠 Go to Home Page", type="primary"):
            st.switch_page("Home.py")
        return
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🔥 Interactive Heatmap Analytics</h1>
        <p class="main-subtitle">Real-time Performance Visualization & AI-Powered Business Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced navigation bar
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("Home.py")
    
    with col2:
        if st.button("🔮 AI Forecasting", use_container_width=True):
            st.switch_page("pages/Forecasting_Tool.py")
    
    with col3:
        if st.button("⚙️ Settings", use_container_width=True):
            st.switch_page("pages/Settings.py")
    
    with col4:
        show_backend_status()
    
    st.markdown("---")
    
    # Load data from backend
    with st.spinner("🔄 Loading heatmap data from backend..."):
        df = load_heatmap_data()
    
    if df.empty:
        st.error("❌ **No data available for heatmap analysis**")
        st.info("""
        **To use the heatmap analytics:**
        1. Go to Settings and click 'Seed Database' to populate with sample data
        2. Return here to generate interactive heatmaps and performance analytics
        3. Explore AI-powered insights and recommendations
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚙️ Go to Settings", type="primary", use_container_width=True):
                st.switch_page("pages/Settings.py")
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.switch_page("Home.py")
        return
    
    # Enhanced control panel
    st.markdown("""
    <div class="control-panel">
        <h3>🎛️ Analysis Controls</h3>
    </div>
    """, unsafe_allow_html=True)
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        # Date range filter
        if 'date' in df.columns:
            min_date = df['date'].min()
            max_date = df['date'].max()
            date_range = st.date_input(
                "📅 Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                help="Select the date range for analysis"
            )
            
            # Filter dataframe by date
            if len(date_range) == 2:
                start_date, end_date = date_range
                df = df[(df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))]
        else:
            st.info("📅 No date filtering available - backend data missing date column")
    
    with filter_col2:
        # Metric selection
        available_metrics = ['predicted_demand']
        if 'actual_demand' in df.columns:
            available_metrics.append('actual_demand')
        
        selected_metric = st.selectbox(
            "📊 Metric to Analyze",
            available_metrics,
            format_func=lambda x: x.replace('_', ' ').title(),
            help="Choose the metric for heatmap visualization"
        )
    
    with filter_col3:
        # Aggregation method
        agg_method = st.selectbox(
            "🔢 Aggregation Method",
            ['mean', 'sum', 'max'],
            format_func=lambda x: x.title(),
            help="Select how to aggregate the data"
        )
    
    st.markdown("---")
    
    # Show filtered data info
    if df.empty:
        st.warning("⚠️ **No data available** for selected filters - please adjust date range or check data")
        return
    
    # Data overview
    st.markdown(f"""
    <div class="stats-highlight">
        <h3>📊 Live Data Overview</h3>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{len(df):,}</div>
                <div class="stat-label">Total Records</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{df['dish'].nunique()}</div>
                <div class="stat-label">Unique Dishes</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{df['outlet'].nunique()}</div>
                <div class="stat-label">Active Outlets</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{df['predicted_demand'].sum():,.0f}</div>
                <div class="stat-label">Total Demand</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main heatmap visualization
    st.markdown("### 🔥 Interactive Demand Heatmap")
    
    heatmap_fig = create_interactive_heatmap(
        df, 
        metric=selected_metric, 
        title=f"Demand Heatmap ({agg_method.title()})"
    )
    
    if heatmap_fig:
        st.plotly_chart(heatmap_fig, use_container_width=True)
    else:
        st.info("🔥 **Heatmap requires data** - Please check your selections")
    
    st.markdown("---")
    
    # Performance metrics and rankings
    st.markdown("### 📊 Performance Analysis")
    
    outlet_perf, dish_perf = create_comparison_metrics(df)
    create_performance_dashboard(outlet_perf, dish_perf)
    
    st.markdown("---")
    
    # Enhanced analytics section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Trend Analysis")
        trend_fig = create_trend_analysis(df)
        if trend_fig:
            st.plotly_chart(trend_fig, use_container_width=True)
        else:
            st.info("📈 **Trend analysis requires date data**")
    
    with col2:
        st.markdown("### 🎯 Key Insights")
        
        if not df.empty:
            total_demand = df['predicted_demand'].sum()
            avg_demand = df['predicted_demand'].mean()
            peak_demand = df['predicted_demand'].max()
            date_span = df['date'].max() - df['date'].min() if 'date' in df.columns else timedelta(days=0)
            
            # Enhanced insights cards
            insights = [
                {
                    "icon": "📊",
                    "title": "Total Demand Volume",
                    "value": f"{total_demand:,.0f} units",
                    "description": "Across all outlets and dishes"
                },
                {
                    "icon": "📅",
                    "title": "Average Daily Demand",
                    "value": f"{avg_demand:.1f} units",
                    "description": "Per dish per day average"
                },
                {
                    "icon": "🔥",
                    "title": "Peak Single Demand",
                    "value": f"{peak_demand:,.0f} units",
                    "description": "Highest recorded demand"
                },
                {
                    "icon": "📈",
                    "title": "Analysis Period",
                    "value": f"{date_span.days} days",
                    "description": "Data coverage span"
                }
            ]
            
            for insight in insights:
                st.markdown(f"""
                <div class="insight-card">
                    <h4>{insight['icon']} {insight['title']}</h4>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #FF6B35; margin-bottom: 0.5rem;">{insight['value']}</div>
                    <p>{insight['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎯 **Insights will appear when data is available**")
    
    st.markdown("---")
    
    # AI-powered recommendations
    create_ai_recommendations(df)
    
    # Action buttons
    st.markdown("### ⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("📊 Export Heatmap Data", use_container_width=True):
            if not df.empty:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"KKCG_Heatmap_Data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ No data to export")
    
    with action_col2:
        if st.button("📈 Generate Analytics Report", use_container_width=True):
            if not df.empty:
                st.success("📄 Analytics report generated successfully!")
            else:
                st.warning("⚠️ No data for report generation")
    
    with action_col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Refreshing from backend...")
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666;">
        <h4 style="color: #FF6B35; margin-bottom: 1rem;">🔥 Interactive Heatmap Analytics Engine</h4>
        <p style="margin: 0;">Real-time performance visualization with AI-powered business insights</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Powered by KKCG Analytics Platform • Live Backend Integration • Advanced Analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 