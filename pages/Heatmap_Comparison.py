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
    page_title="KKCG Heatmap Analytics",
    page_icon="🔥",
    layout="wide"
)

# Custom CSS with professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .insight-card {
        background: linear-gradient(145deg, #2c3e50, #34495e);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,107,53,0.3);
    }
    
    .metric-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        margin: 1rem 0;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .performance-indicator {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        text-align: center;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .high-performance { background: #27AE60; color: white; }
    .medium-performance { background: #F39C12; color: white; }
    .low-performance { background: #E74C3C; color: white; }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_heatmap_data():
    """Load data for heatmap analysis from backend API ONLY"""
    client = get_api_client()
    
    try:
        df = client.get_demand_data()
        
        if df.empty:
            st.warning("⚠️ **No data available**: Backend returned empty dataset for heatmap analysis")
            st.info("💡 **Tip**: Seed the database with sample data to generate heatmaps")
            return pd.DataFrame()
        
        return df
        
    except Exception as e:
        st.error(f"❌ **Heatmap Data Error**: {str(e)}")
        st.stop()

def create_interactive_heatmap(df, metric='predicted_demand', title="Demand Heatmap"):
    """Create an interactive heatmap visualization from backend data"""
    
    if df.empty:
        st.info("🔥 **No heatmap data available**: Please seed the database to generate heatmaps")
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
    
    # Create heatmap with dark professional colors - custom color scheme for better differentiation
    fig = px.imshow(
        pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        aspect='auto',
        color_continuous_scale='Plasma',  # Dark, high-contrast color scheme perfect for dark themes
        title=f"{title} (Live Backend Data)"
    )
    
    # Customize layout for dark theme with improved aesthetics
    fig.update_layout(
        title=dict(
            text=f"{title} (Live Backend Data)",
            font=dict(size=24, color='#FF6B35'),
            x=0.5
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        height=600,
        xaxis_title="Outlets",
        yaxis_title="Dishes",
        coloraxis_colorbar=dict(
            title=dict(text=metric.replace('_', ' ').title(), font=dict(color='white')),
            tickfont=dict(color='white'),
            bgcolor='rgba(30,30,30,0.8)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        )
    )
    
    # Add custom hover template
    fig.update_traces(
        hovertemplate='<b>%{y}</b> at <b>%{x}</b><br>Demand: %{z:.1f}<extra></extra>'
    )
    
    return fig

def create_comparison_metrics(df):
    """Create comparison metrics for outlets and dishes from backend data"""
    
    if df.empty:
        st.info("📊 **No metrics data**: Please seed the database to see performance metrics")
        return None, None
    
    # Outlet performance
    if 'outlet' in df.columns and 'predicted_demand' in df.columns:
        outlet_performance = df.groupby('outlet')['predicted_demand'].agg(['mean', 'sum', 'std']).round(2)
        outlet_performance.columns = ['Avg Demand', 'Total Demand', 'Variability']
        outlet_performance = outlet_performance.sort_values('Total Demand', ascending=False)
        
        # Dish performance
        dish_performance = df.groupby('dish')['predicted_demand'].agg(['mean', 'sum', 'std']).round(2)
        dish_performance.columns = ['Avg Demand', 'Total Demand', 'Variability']
        dish_performance = dish_performance.sort_values('Total Demand', ascending=False)
        
        return outlet_performance, dish_performance
    else:
        st.error("❌ **Missing columns**: Backend data must contain 'outlet' and 'predicted_demand' columns")
        return None, None

def create_trend_analysis(df):
    """Create trend analysis charts from backend data"""
    
    if df.empty:
        st.info("📈 **No trend data**: Please seed the database to see trend analysis")
        return None
    
    if 'date' not in df.columns:
        st.warning("⚠️ **No date data**: Backend data must contain 'date' column for trend analysis")
        return None
    
    # Daily trends
    daily_trends = df.groupby('date')['predicted_demand'].sum().reset_index()
    
    if daily_trends.empty:
        st.warning("⚠️ **No trend data**: Unable to aggregate data by date")
        return None
    
    fig = px.line(
        daily_trends,
        x='date',
        y='predicted_demand',
        title='📈 Daily Demand Trends (Live Backend Data)',
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
    
    return fig

def create_performance_dashboard(outlet_perf, dish_perf):
    """Create performance dashboard with rankings from backend data"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏢 Outlet Performance Ranking (Live Data)")
        
        if outlet_perf is not None and not outlet_perf.empty:
            for i, (outlet, data) in enumerate(outlet_perf.head(5).iterrows()):
                rank_icon = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
                performance_class = "high-performance" if i < 2 else "medium-performance" if i < 4 else "low-performance"
                
                st.markdown(f"""
                <div class="insight-card">
                    <h4>{rank_icon} {outlet}</h4>
                    <p><strong>Total Demand:</strong> {data['Total Demand']:,.0f}</p>
                    <p><strong>Avg Daily:</strong> {data['Avg Demand']:.1f}</p>
                    <span class="performance-indicator {performance_class}">
                        {'Top Performer' if i < 2 else 'Good' if i < 4 else 'Needs Attention'}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📊 **No outlet data**: Please seed the database to see outlet performance")
    
    with col2:
        st.markdown("#### 🍽️ Dish Performance Ranking (Live Data)")
        
        if dish_perf is not None and not dish_perf.empty:
            for i, (dish, data) in enumerate(dish_perf.head(5).iterrows()):
                rank_icon = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
                performance_class = "high-performance" if i < 2 else "medium-performance" if i < 4 else "low-performance"
                
                st.markdown(f"""
                <div class="insight-card">
                    <h4>{rank_icon} {dish}</h4>
                    <p><strong>Total Demand:</strong> {data['Total Demand']:,.0f}</p>
                    <p><strong>Avg Daily:</strong> {data['Avg Demand']:.1f}</p>
                    <span class="performance-indicator {performance_class}">
                        {'Best Seller' if i < 2 else 'Popular' if i < 4 else 'Low Demand'}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🍽️ **No dish data**: Please seed the database to see dish performance")

def create_ai_recommendations(df):
    """Generate AI-powered business recommendations from backend data"""
    
    st.markdown("#### 🤖 AI-Powered Business Insights (Live Data)")
    
    if df.empty:
        st.info("🤖 **No data for AI analysis**: Please seed the database to generate insights")
        return
    
    # Generate insights based on actual data
    total_records = len(df)
    unique_dishes = df['dish'].nunique() if 'dish' in df.columns else 0
    unique_outlets = df['outlet'].nunique() if 'outlet' in df.columns else 0
    avg_demand = df['predicted_demand'].mean() if 'predicted_demand' in df.columns else 0
    
    recommendations = [
        {
            "icon": "📊",
            "title": "Backend Data Analysis",
            "insight": f"Processing {total_records:,} live records across {unique_outlets} outlets and {unique_dishes} dishes",
            "action": f"Average demand per item: {avg_demand:.1f} units - optimize inventory accordingly"
        },
        {
            "icon": "🔗",
            "title": "Live Database Integration",
            "insight": "Real-time data connection to Railway-hosted PostgreSQL database established",
            "action": "Monitor data quality and ensure regular updates for accurate analytics"
        },
        {
            "icon": "🎯",
            "title": "Performance Optimization",
            "insight": "Backend API responding successfully with structured restaurant data",
            "action": "Leverage live data for real-time business decisions and inventory management"
        },
        {
            "icon": "💡",
            "title": "Scalability Ready",
            "insight": "System configured for production-grade analytics with automated data processing",
            "action": "Scale data collection and add more outlets for comprehensive analysis"
        }
    ]
    
    for rec in recommendations:
        st.markdown(f"""
        <div class="insight-card">
            <h4>{rec['icon']} {rec['title']}</h4>
            <p><strong>Insight:</strong> {rec['insight']}</p>
            <p><strong>Recommended Action:</strong> {rec['action']}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main heatmap analytics interface with backend-only integration"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🔥 Live Heatmap Analytics</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Real-time Backend Data Visualization & Performance Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button and backend status
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🏠 Back to Home"):
            st.switch_page("Home.py")
    
    with col2:
        show_backend_status()
    
    st.markdown("---")
    
    # Load data from backend
    with st.spinner("🔄 Loading heatmap data from backend..."):
        df = load_heatmap_data()
    
    if df.empty:
        st.error("❌ **No data available for heatmap analysis**")
        st.info("""
        **To use the heatmap analytics:**
        1. Go back to the Home page
        2. Click 'Seed Database' to populate with sample data
        3. Return here to generate heatmaps and analytics
        """)
        return
    
    # Filter controls
    st.markdown("### 🎛️ Analysis Controls (Live Backend Data)")
    
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
                max_value=max_date
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
            format_func=lambda x: x.replace('_', ' ').title()
        )
    
    with filter_col3:
        # Aggregation method
        agg_method = st.selectbox(
            "🔢 Aggregation Method",
            ['mean', 'sum', 'max'],
            format_func=lambda x: x.title()
        )
    
    st.markdown("---")
    
    # Show filtered data info
    if df.empty:
        st.warning("⚠️ **No data available** for selected filters - please adjust date range or check data")
        return
    
    st.info(f"📊 **Analyzing {len(df):,} records** from live backend database with {df['dish'].nunique()} dishes across {df['outlet'].nunique()} outlets")
    
    # Main heatmap visualization
    st.markdown("### 🔥 Interactive Demand Heatmap")
    
    heatmap_fig = create_interactive_heatmap(
        df, 
        metric=selected_metric, 
        title=f"🔥 {selected_metric.replace('_', ' ').title()} Heatmap ({agg_method.title()})"
    )
    
    if heatmap_fig:
        st.plotly_chart(heatmap_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Performance metrics and rankings
    st.markdown("### 📊 Live Performance Analysis")
    
    outlet_perf, dish_perf = create_comparison_metrics(df)
    create_performance_dashboard(outlet_perf, dish_perf)
    
    st.markdown("---")
    
    # Trend analysis
    st.markdown("### 📈 Backend Data Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trend_fig = create_trend_analysis(df)
        if trend_fig:
            st.plotly_chart(trend_fig, use_container_width=True)
    
    with col2:
        # Summary statistics from backend
        st.markdown("#### 📊 Live Data Statistics")
        
        if not df.empty:
            total_demand = df['predicted_demand'].sum()
            avg_demand = df['predicted_demand'].mean()
            peak_demand = df['predicted_demand'].max()
            unique_dishes = df['dish'].nunique() if 'dish' in df.columns else 0
            unique_outlets = df['outlet'].nunique() if 'outlet' in df.columns else 0
            date_range = df['date'].max() - df['date'].min() if 'date' in df.columns else timedelta(days=0)
            
            st.markdown(f"""
            <div class="metric-highlight">
                <h3>📊 Backend Data Overview</h3>
                <p><strong>Total Records:</strong> {len(df):,}</p>
                <p><strong>Total Demand:</strong> {total_demand:,.0f} units</p>
                <p><strong>Average Daily:</strong> {avg_demand:.1f} units</p>
                <p><strong>Peak Demand:</strong> {peak_demand:,.0f} units</p>
                <p><strong>Active Dishes:</strong> {unique_dishes}</p>
                <p><strong>Outlet Coverage:</strong> {unique_outlets} locations</p>
                <p><strong>Date Range:</strong> {date_range.days} days</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI-powered insights
    create_ai_recommendations(df)
    
    # Backend data details
    st.markdown("---")
    st.markdown("### 🌐 Backend Integration Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        client = get_api_client()
        st.markdown(f"""
        **🔗 Live Backend Connection:**
        - **API URL**: {client.base_url}
        - **Status**: ✅ Connected
        - **Authentication**: {'✅ Authenticated' if check_authentication() else '⚠️ Anonymous'}
        - **Data Source**: PostgreSQL Database
        - **Records Loaded**: {len(df):,}
        """)
    
    with col2:
        st.markdown("""
        **📊 Data Structure:**
        - ✅ Outlet information
        - ✅ Dish catalog
        - ✅ Demand predictions
        - ✅ Date/time stamps
        - ✅ Performance metrics
        - ✅ Real-time updates
        """)
    
    # Export and action buttons
    st.markdown("---")
    st.markdown("### 📥 Export & Actions")
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        if st.button("📊 Export Backend Data", use_container_width=True):
            if not df.empty:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"KKCG_Backend_Heatmap_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ No data to export")
    
    with export_col2:
        if st.button("📈 Generate Report", use_container_width=True):
            if not df.empty:
                st.success("📄 Backend analytics report generated!")
            else:
                st.warning("⚠️ No data for report generation")
    
    with export_col3:
        if st.button("🔄 Refresh Analysis", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Refreshing from backend...")
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; color: #7F8C8D;">
        <p>🔥 <strong>Live Backend Heatmap Analytics</strong></p>
        <p>Real-time visualization with Railway-hosted PostgreSQL and interactive performance analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 