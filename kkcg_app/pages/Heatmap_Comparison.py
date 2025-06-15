import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

# Import custom utilities
from data_simulation import generate_demand_data, SOUTH_INDIAN_DISHES, OUTLETS
from heatmap_utils import generate_heatmap, generate_trend_chart, generate_comparison_bar_chart
from insights import compute_business_insights, generate_insight_texts, generate_recommendations

# Page configuration
st.set_page_config(
    page_title="🔥 Heatmap Analytics | KKCG",
    page_icon="🔥",
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
    
    /* Dark theme for the app */
    .stApp {
        background: #1a1a2e;
        color: white;
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
    
    .alert-card {
        background: #2a2a3e;
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        border-left: 4px solid #FF6B35;
        transition: all 0.3s ease;
    }
    
    .alert-card:hover {
        background: #3a3a4e;
        border: 1px solid rgba(255,107,53,0.2);
        border-left: 4px solid #FF6B35;
    }
    
    /* KPI styling */
    .kpi-number {
        font-size: 2rem;
        font-weight: 700;
        color: #FF6B35;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .kpi-label {
        color: #E8F4FD;
        font-size: 1rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    
    .kpi-delta {
        color: #A0A0A0;
        font-size: 0.9rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #2a2a3e;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Enhanced text styling */
    .section-header {
        color: #FF6B35;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Table styling */
    .dataframe {
        background-color: #2a2a3e !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Cache the data generation to improve performance
@st.cache_data
def load_data():
    """Load and cache the demand data"""
    return generate_demand_data()

def create_kpi_card(title, value, delta, icon="📊"):
    """Create a beautiful KPI card with neumorphism styling"""
    return f"""
    <div class="metric-card">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="kpi-number">{value}</div>
        <div class="kpi-label">{title}</div>
        <div class="kpi-delta">{delta}</div>
    </div>
    """

def create_insight_card(title, content):
    """Create an insight card with neumorphism styling"""
    return f"""
    <div class="insight-card">
        <h4 style="color: #FF6B35; margin-bottom: 1rem;">{title}</h4>
        <p style="color: #E8F4FD; margin: 0; line-height: 1.6;">{content}</p>
    </div>
    """

def create_alert_card(content, alert_type="info"):
    """Create an alert card with neumorphism styling"""
    icon_map = {
        "success": "✅",
        "warning": "⚠️",
        "critical": "🚨",
        "info": "💡"
    }
    icon = icon_map.get(alert_type, "💡")
    
    return f"""
    <div class="alert-card">
        <p style="color: #E8F4FD; margin: 0; line-height: 1.6;">
            {icon} {content}
        </p>
    </div>
    """

def main():
    """Enhanced main application function with improved layout and organization"""
    
    # Header with beautiful styling
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🔥 Demand Heatmap & Analytics</h1>
        <p class="main-subtitle">Visualize demand patterns and discover business insights with AI-powered analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top navigation bar with perfect symmetry
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.success("🏠 Navigate to Home page using the sidebar!")
    
    with nav_col2:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; padding: 1rem 0;">
            <span style="background: linear-gradient(145deg, #4CAF50, #45a049); color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; box-shadow: 0 4px 6px rgba(76,175,80,0.3);">📊 Analytics Ready</span>
        </div>
        """, unsafe_allow_html=True)
    
    with nav_col3:
        if st.button("📋 Export Data", use_container_width=True):
            st.info("📊 Use the export options in the insights sections below!")
    
    # Load data
    with st.spinner("🔄 Loading demand analytics..."):
        df = load_data()
    
    # Enhanced Sidebar with collapsible sections
    st.sidebar.header("🎛️ Analytics Controls")
    st.sidebar.markdown("---")
    
    # Display Controls Section
    with st.sidebar.expander("📊 Display Controls", expanded=True):
        # Dish selection method
        selection_method = st.radio(
            "Dish Selection Method",
            options=["Top N Dishes", "Custom Selection"],
            help="Choose how to filter dishes for visualization"
        )
        
        if selection_method == "Top N Dishes":
            top_n_dishes = st.slider(
                "Number of Top Dishes",
                min_value=5,
                max_value=len(SOUTH_INDIAN_DISHES),
                value=20,
                step=5,
                help="Select the number of top-performing dishes to display"
            )
            selected_dishes = None
        else:
            selected_dishes = st.multiselect(
                "Select Specific Dishes",
                options=sorted(SOUTH_INDIAN_DISHES),
                default=sorted(SOUTH_INDIAN_DISHES)[:10],
                help="Choose specific dishes to analyze"
            )
            top_n_dishes = None
        
        # Demand mode selection
        demand_mode = st.selectbox(
            "Demand Calculation Mode",
            options=["total", "average"],
            format_func=lambda x: "📊 Total Demand" if x == "total" else "📈 Average Daily Demand",
            help="Choose between total demand and average daily demand"
        )
        
        # Normalization option
        normalize_demand = st.checkbox(
            "🔢 Normalize Demand per Outlet",
            value=False,
            help="Normalize demand values per outlet for better comparison"
        )
    
    # Filters Section
    with st.sidebar.expander("🔍 Filters", expanded=False):
        # Outlet filter
        selected_outlets = st.multiselect(
            "Select Outlets",
            options=OUTLETS,
            default=OUTLETS,
            help="Filter data by specific outlets"
        )
        
        # Date range info
        st.info("📅 **Data Period**: 7-day forecast\n" + 
               f"From {df['date'].min()} to {df['date'].max()}")
        
        # Demand threshold filter
        min_demand = st.number_input(
            "Minimum Demand Threshold",
            min_value=0,
            max_value=int(df['predicted_demand'].max()),
            value=0,
            help="Filter out dishes with demand below this threshold"
        )
    
    # Quick stats in sidebar
    with st.sidebar.expander("📈 Quick Stats", expanded=False):
        st.metric("Total Dishes", df['dish'].nunique())
        st.metric("Total Outlets", df['outlet'].nunique())
        st.metric("Total Records", f"{len(df):,}")
        st.metric("Max Daily Demand", f"{df['predicted_demand'].max():,}")
        st.metric("Avg Daily Demand", f"{df['predicted_demand'].mean():.0f}")
    
    # Filter data based on selections
    filtered_df = df.copy()
    if selected_outlets:
        filtered_df = filtered_df[filtered_df['outlet'].isin(selected_outlets)]
    if min_demand > 0:
        filtered_df = filtered_df[filtered_df['predicted_demand'] >= min_demand]
    if selected_dishes is not None:
        filtered_df = filtered_df[filtered_df['dish'].isin(selected_dishes)]
    
    # Compute insights based on filtered data
    insights = compute_business_insights(filtered_df)
    
    # Enhanced KPI Cards Section with perfect symmetry
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 2rem;">🎯 Key Performance Indicators</h2>
        <p style="color: #BDC3C7; font-size: 1rem; margin-bottom: 2rem;">Real-time insights into demand patterns and performance metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top 3 KPI cards with perfect symmetry
    kpi_col1, kpi_col2, kpi_col3 = st.columns([1, 1, 1], gap="large")
    
    # Create the KPI data
    kpi_data = [
        {
            "icon": "🏆",
            "title": "Top Performing Dish",
            "value": insights['top_dish'],
            "subtitle": f"{insights['top_dish_demand']:,} total demand",
            "trend": "📈 Trending" if insights['top_dish_demand'] > insights['avg_demand_per_dish'] * 5 else "📊 Stable"
        },
        {
            "icon": "🏢",
            "title": "Leading Outlet",
            "value": insights['top_outlet'],
            "subtitle": f"{insights['top_outlet_demand']:,} total demand",
            "trend": "🔥 High Traffic" if insights['top_outlet'] in ["Chennai Central", "Jubilee Hills"] else "⭐ Premium"
        },
        {
            "icon": "⚖️",
            "title": "Most Variable Dish",
            "value": insights['most_unbalanced_dish'],
            "subtitle": f"CV: {insights['unbalance_coefficient']:.2f}",
            "trend": "🚨 High Risk" if insights['unbalance_coefficient'] > 0.5 else "⚠️ Monitor"
        }
    ]
    
    for col, kpi in zip([kpi_col1, kpi_col2, kpi_col3], kpi_data):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="height: 280px; display: flex; flex-direction: column; padding: 1.2rem 1rem 2rem 1rem;">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.6rem;">{kpi["icon"]}</div>
                    <h3 style="color: #FF6B35; margin: 0; font-size: 0.95rem; text-align: center; line-height: 1.1; font-weight: 600;">{kpi["title"]}</h3>
                </div>
                <div style="text-align: center; margin-bottom: 1rem;">
                    <h2 style="color: #E8F4FD; margin: 0 0 0.6rem 0; font-size: 1.05rem; text-align: center; line-height: 1.1; word-wrap: break-word; font-weight: 700;">{kpi["value"]}</h2>
                    <p style="color: #BDC3C7; margin: 0; font-size: 0.8rem; text-align: center; line-height: 1.1;">{kpi["subtitle"]}</p>
                </div>
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <p style="color: #FF6B35; margin: 0; font-size: 0.7rem; text-align: center; font-weight: bold; line-height: 1.0;">{kpi["trend"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Operational metrics section with symmetry
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 1.8rem;">📊 Operational Metrics</h2>
        <p style="color: #BDC3C7; font-size: 1rem;">Essential operational insights for daily management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Four-column layout for operational metrics
    op_col1, op_col2, op_col3, op_col4 = st.columns([1, 1, 1, 1], gap="medium")
    
    avg_demand = int(filtered_df['predicted_demand'].mean())
    total_demand = int(filtered_df['predicted_demand'].sum())
    
    operational_metrics = [
        {
            "label": "📅 Peak Day",
            "value": insights['peak_day'].strftime("%a, %b %d"),
            "delta": f"{insights['peak_day_demand']:,} demand"
        },
        {
            "label": "🎯 Most Consistent",
            "value": insights['most_consistent_dish'],
            "delta": "Low variance"
        },
        {
            "label": "📈 Avg Daily Demand",
            "value": f"{avg_demand:,}",
            "delta": f"Per dish: {insights['avg_demand_per_dish']:.1f}"
        },
        {
            "label": "💰 Total Demand",
            "value": f"{total_demand:,}",
            "delta": f"Across {filtered_df['outlet'].nunique()} outlets"
        }
    ]
    
    for col, metric in zip([op_col1, op_col2, op_col3, op_col4], operational_metrics):
        with col:
            st.metric(
                metric["label"],
                metric["value"],
                metric["delta"]
            )
    
    st.markdown("---")
    
    # Enhanced Main heatmap section with perfect symmetry
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 2rem;">🔥 Interactive Demand Heatmap</h2>
        <p style="color: #BDC3C7; font-size: 1rem;">Visualize demand patterns across dishes and outlets with advanced filtering</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Heatmap controls with perfect balance
    control_col1, control_col2, control_col3 = st.columns([2, 1, 1], gap="medium")
    
    with control_col1:
        st.markdown(f"""
        <div style="padding: 1rem; background: #2a2a3e; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); text-align: center;">
            <h4 style="color: #FF6B35; margin: 0 0 0.5rem 0;">📊 Data Overview</h4>
            <p style="color: #E8F4FD; margin: 0; font-size: 0.9rem;">
                <strong>{len(filtered_df):,} records</strong> across <strong>{filtered_df['outlet'].nunique()} outlets</strong> and <strong>{filtered_df['dish'].nunique()} dishes</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with control_col2:
        heatmap_mode = st.selectbox(
            "🎨 Heatmap Mode",
            ["Absolute Demand", "Normalized Demand"],
            help="Choose between absolute values or normalized per outlet"
        )
    
    with control_col3:
        color_scale = st.selectbox(
            "🌈 Color Scale",
            ["Viridis", "Inferno", "Plasma", "Turbo"],
            help="Select color scale for the heatmap"
        )
    
    # Generate enhanced heatmap
    use_normalized = normalize_demand or (heatmap_mode == "Normalized Demand")
    heatmap_fig = generate_heatmap(
        filtered_df, 
        value_mode=demand_mode, 
        top_n_dishes=top_n_dishes,
        normalize=use_normalized,
        color_scale=color_scale.lower()
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    # Additional charts in tabs with enhanced styling
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 2rem;">📊 Detailed Analytics</h2>
        <p style="color: #BDC3C7; font-size: 1rem;">Comprehensive analysis across multiple dimensions</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Demand Trends", 
        "🏢 Outlet Comparison", 
        "🍽️ Dish Analysis", 
        "💡 Business Insights"
    ])
    
    with tab1:
        st.markdown("### 📈 Demand Trends Over Time")
        
        # Filter options for trend analysis
        col1, col2 = st.columns(2)
        
        with col1:
            selected_dish = st.selectbox(
                "Select Dish for Trend Analysis (Optional)",
                options=[None] + sorted(df['dish'].unique().tolist()),
                format_func=lambda x: "All Dishes" if x is None else x
            )
        
        with col2:
            selected_outlet = st.selectbox(
                "Select Outlet for Trend Analysis (Optional)",
                options=[None] + sorted(df['outlet'].unique().tolist()),
                format_func=lambda x: "All Outlets" if x is None else x
            )
        
        # Generate trend chart
        trend_fig = generate_trend_chart(df, dish_name=selected_dish, outlet_name=selected_outlet)
        st.plotly_chart(trend_fig, use_container_width=True)
        
        # Enhanced Daily demand summary
        if selected_dish is None and selected_outlet is None:
            st.markdown("#### 📅 Daily Demand Summary")
            
            # Create enhanced daily summary
            try:
                daily_summary = df.groupby('date')['predicted_demand'].agg(['sum', 'mean', 'std']).round(1)
                daily_summary.reset_index(inplace=True)
                
                # Ensure date column is datetime
                if not pd.api.types.is_datetime64_any_dtype(daily_summary['date']):
                    daily_summary['date'] = pd.to_datetime(daily_summary['date'])
                
                # Add day names and formatted dates
                daily_summary['Day'] = daily_summary['date'].dt.strftime('%A')
                daily_summary['Date'] = daily_summary['date'].dt.strftime('%Y-%m-%d')
                
                # Format numbers properly
                daily_summary['Total Demand'] = daily_summary['sum'].apply(lambda x: f"{x:,.0f}")
                daily_summary['Average Demand'] = daily_summary['mean'].apply(lambda x: f"{x:.1f}")
                daily_summary['Std Deviation'] = daily_summary['std'].apply(lambda x: f"{x:.1f}")
                
                # Create styled display dataframe
                display_df = daily_summary[['Day', 'Date', 'Total Demand', 'Average Demand', 'Std Deviation']].copy()
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Add summary insights below the table
                total_week_demand = daily_summary['sum'].sum()
                peak_day = daily_summary.loc[daily_summary['sum'].idxmax()]
                lowest_day = daily_summary.loc[daily_summary['sum'].idxmin()]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Weekly Total", f"{total_week_demand:,.0f}", "All outlets combined")
                with col2:
                    st.metric("🔥 Peak Day", f"{peak_day['Day']}", f"{peak_day['sum']:,.0f} demand")
                with col3:
                    st.metric("📉 Lowest Day", f"{lowest_day['Day']}", f"{lowest_day['sum']:,.0f} demand")
                    
            except Exception as e:
                st.error(f"Error creating daily summary: {str(e)}")
                # Fallback to simple table
                simple_summary = df.groupby('date')['predicted_demand'].agg(['sum', 'mean', 'std']).round(1)
                simple_summary.columns = ['Total Demand', 'Average Demand', 'Std Deviation']
                st.dataframe(simple_summary, use_container_width=True)
    
    with tab2:
        st.markdown("### 🏢 Outlet Performance Comparison")
        
        # Outlet comparison bar chart
        outlet_fig = generate_comparison_bar_chart(df, comparison_type="outlet")
        st.plotly_chart(outlet_fig, use_container_width=True)
        
        # Outlet performance table
        outlet_performance = df.groupby('outlet').agg({
            'predicted_demand': ['sum', 'mean', 'std', 'count']
        }).round(2)
        outlet_performance.columns = ['Total Demand', 'Avg Demand', 'Std Deviation', 'Dish Varieties']
        outlet_performance = outlet_performance.sort_values('Total Demand', ascending=False)
        outlet_performance['Rank'] = range(1, len(outlet_performance) + 1)
        
        st.markdown("#### 🏆 Outlet Performance Rankings")
        st.dataframe(outlet_performance[['Rank', 'Total Demand', 'Avg Demand', 'Dish Varieties']], use_container_width=True)
        
        # Best dish per outlet
        st.markdown("#### 🌟 Champion Dishes by Outlet")
        for outlet, data in insights['best_dish_per_outlet'].items():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{outlet}**")
            with col2:
                st.write(f"{data['dish']}")
            with col3:
                st.write(f"{data['demand']:,}")
    
    with tab3:
        st.markdown("### 🍽️ Dish Performance Analysis")
        
        # Top dishes bar chart
        dish_fig = generate_comparison_bar_chart(df, comparison_type="dish")
        st.plotly_chart(dish_fig, use_container_width=True)
        
        # Dish performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Top Performing Dishes")
            top_dishes = df.groupby('dish')['predicted_demand'].sum().nlargest(10)
            for i, (dish, demand) in enumerate(top_dishes.items(), 1):
                st.write(f"{i}. **{dish}**: {demand:,}")
        
        with col2:
            st.markdown("#### ⚖️ Most Consistent Dishes")
            # Calculate coefficient of variation for dishes
            dish_cv = df.groupby('dish')['predicted_demand'].agg(['mean', 'std'])
            dish_cv['cv'] = dish_cv['std'] / dish_cv['mean']
            most_consistent = dish_cv.nsmallest(10, 'cv')
            for i, (dish, data) in enumerate(most_consistent.iterrows(), 1):
                st.write(f"{i}. **{dish}**: CV = {data['cv']:.2f}")
        
        # Detailed dish statistics
        st.markdown("#### 📊 Detailed Dish Statistics")
        dish_stats = df.groupby('dish').agg({
            'predicted_demand': ['sum', 'mean', 'std', 'min', 'max']
        }).round(1)
        dish_stats.columns = ['Total', 'Mean', 'Std Dev', 'Min', 'Max']
        dish_stats = dish_stats.sort_values('Total', ascending=False)
        
        # Add search functionality
        search_dish = st.text_input("🔍 Search for a specific dish:", placeholder="Type dish name...")
        if search_dish:
            filtered_stats = dish_stats[dish_stats.index.str.contains(search_dish, case=False)]
            st.dataframe(filtered_stats, use_container_width=True)
        else:
            st.dataframe(dish_stats.head(20), use_container_width=True)
    
    with tab4:
        st.markdown('<div class="section-header">💡 Business Intelligence Dashboard</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #A0A0A0; margin-bottom: 2rem;'>AI-powered insights and actionable recommendations for strategic decision making</p>", unsafe_allow_html=True)
        
        # Generate insight texts
        insight_texts = generate_insight_texts(insights)
        recommendations = generate_recommendations(insights)
        
        # Smart Business Alerts Section
        st.markdown("### 🚨 Smart Business Alerts")
        
        # Create different types of alerts based on data patterns
        alert_col1, alert_col2 = st.columns(2)
        
        with alert_col1:
            # Underperforming dish alert
            worst_dish = min(insights['worst_dish_per_outlet'].items(), 
                           key=lambda x: x[1]['demand'])
            st.markdown(create_alert_card(
                f"**Low Performance Alert**: {worst_dish[1]['dish']} at {worst_dish[0]} shows concerning demand of only {worst_dish[1]['demand']:,} units. Consider promotional activities or menu optimization.",
                "warning"
            ), unsafe_allow_html=True)
            
            # Demand spike detection
            peak_outlet_dish = max(insights['best_dish_per_outlet'].items(), 
                                 key=lambda x: x[1]['demand'])
            st.markdown(create_alert_card(
                f"**Success Story**: {peak_outlet_dish[1]['dish']} at {peak_outlet_dish[0]} is performing exceptionally with {peak_outlet_dish[1]['demand']:,} demand. Replicate this success across other outlets!",
                "success"
            ), unsafe_allow_html=True)
        
        with alert_col2:
            # Consistency alert
            if insights['unbalance_coefficient'] > 0.4:
                st.markdown(create_alert_card(
                    f"**Consistency Alert**: {insights['most_unbalanced_dish']} shows high variation (CV: {insights['unbalance_coefficient']:.2f}) across outlets. Standardize recipes and training for better consistency.",
                    "critical"
                ), unsafe_allow_html=True)
            else:
                st.markdown(create_alert_card(
                    f"**Stability Indicator**: {insights['most_consistent_dish']} shows excellent consistency across all outlets. This dish is a reliable revenue driver.",
                    "info"
                ), unsafe_allow_html=True)
            
            # Peak day preparation
            st.markdown(create_alert_card(
                f"**Operational Insight**: {insights['peak_day'].strftime('%A')}s generate highest demand ({insights['peak_day_demand']:,} units). Ensure adequate staffing and inventory for this day.",
                "info"
            ), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Key Business Insights Cards
        st.markdown("### 🔍 Key Business Insights")
        
        insight_cols = st.columns(2)
        for i, insight in enumerate(insight_texts[:6]):  # Show first 6 insights
            with insight_cols[i % 2]:
                st.markdown(create_insight_card(
                    f"Insight {i+1}",
                    insight
                ), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Actionable Recommendations
        st.markdown("### 🚀 Strategic Recommendations")
        
        for i, recommendation in enumerate(recommendations, 1):
            alert_type = "success" if i <= 2 else "info"  # First 2 as high priority
            st.markdown(create_alert_card(
                f"**Priority {i}**: {recommendation}", 
                alert_type
            ), unsafe_allow_html=True)
        
        # Export options
        st.markdown("---")
        st.markdown("### 📥 Export Analytics")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            # Export full dataset
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Full Dataset",
                data=csv_data,
                file_name=f"kkcg_demand_analytics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with export_col2:
            # Export insights summary
            insights_text = "\n".join([f"• {insight}" for insight in insight_texts])
            recommendations_text = "\n".join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])
            
            summary_report = f"""
KKCG Analytics Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

KEY INSIGHTS:
{insights_text}

RECOMMENDATIONS:
{recommendations_text}

DATA SUMMARY:
- Total Records: {len(filtered_df):,}
- Outlets Analyzed: {filtered_df['outlet'].nunique()}
- Dishes Analyzed: {filtered_df['dish'].nunique()}
- Total Demand: {filtered_df['predicted_demand'].sum():,}
"""
            
            st.download_button(
                label="📄 Download Insights Report",
                data=summary_report,
                file_name=f"kkcg_insights_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    main() 