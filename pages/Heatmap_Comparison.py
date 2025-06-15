import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import custom utilities
from utils.data_simulation import generate_demand_data, SOUTH_INDIAN_DISHES, OUTLETS
from utils.heatmap_utils import generate_heatmap, generate_trend_chart, generate_comparison_bar_chart
from utils.insights import compute_business_insights, generate_insight_texts, generate_recommendations

# Page configuration
st.set_page_config(
    page_title="🔥 Heatmap Analytics | KKCG",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: inset 5px 5px 10px rgba(0,0,0,0.2), inset -5px -5px 10px rgba(255,255,255,0.1);
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
    
    .alert-card {
        background: #2a2a3e;
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        border-left: 4px solid #FF6B35;
        transition: all 0.3s ease;
    }
    
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the demand data"""
    return generate_demand_data()

def create_insight_card(title, content):
    """Create an insight card"""
    return f"""
    <div class="insight-card">
        <h4 style="color: #FF6B35; margin-bottom: 1rem;">{title}</h4>
        <p style="color: #E8F4FD; margin: 0; line-height: 1.6;">{content}</p>
    </div>
    """

def create_alert_card(content, alert_type="info"):
    """Create an alert card"""
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
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🔥 Demand Heatmap & Analytics</h1>
        <p class="main-subtitle">Visualize demand patterns and discover business insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("Home.py")
    
    with nav_col2:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; padding: 1rem 0;">
            <span style="background: linear-gradient(145deg, #4CAF50, #45a049); color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">📊 Analytics Ready</span>
        </div>
        """, unsafe_allow_html=True)
    
    with nav_col3:
        if st.button("📋 Export Data", use_container_width=True):
            st.info("📊 Use the export options below!")
    
    # Load data
    with st.spinner("🔄 Loading analytics..."):
        df = load_data()
    
    st.info("🚀 **Analytics Dashboard Active** - Analyzing 7-day demand forecast data")
    
    # Sidebar controls
    st.sidebar.header("🎛️ Analytics Controls")
    
    with st.sidebar.expander("📊 Display Controls", expanded=True):
        selection_method = st.radio(
            "Dish Selection Method",
            options=["Top N Dishes", "Custom Selection"]
        )
        
        if selection_method == "Top N Dishes":
            top_n_dishes = st.slider("Number of Top Dishes", 5, len(SOUTH_INDIAN_DISHES), 20, 5)
            selected_dishes = None
        else:
            selected_dishes = st.multiselect(
                "Select Specific Dishes",
                options=sorted(SOUTH_INDIAN_DISHES),
                default=sorted(SOUTH_INDIAN_DISHES)[:10]
            )
            top_n_dishes = None
        
        demand_mode = st.selectbox(
            "Demand Calculation Mode",
            options=["total", "average"],
            format_func=lambda x: "📊 Total Demand" if x == "total" else "📈 Average Daily Demand"
        )
        
        normalize_demand = st.checkbox("🔢 Normalize Demand per Outlet", value=False)
    
    with st.sidebar.expander("🔍 Filters", expanded=False):
        selected_outlets = st.multiselect(
            "Select Outlets",
            options=OUTLETS,
            default=OUTLETS
        )
        
        st.info(f"📅 Data Period: 7-day forecast\nFrom {df['date'].min()} to {df['date'].max()}")
        
        min_demand = st.number_input(
            "Minimum Demand Threshold",
            min_value=0,
            max_value=int(df['predicted_demand'].max()),
            value=0
        )
    
    # Filter data
    filtered_df = df.copy()
    if selected_outlets:
        filtered_df = filtered_df[filtered_df['outlet'].isin(selected_outlets)]
    if min_demand > 0:
        filtered_df = filtered_df[filtered_df['predicted_demand'] >= min_demand]
    if selected_dishes is not None:
        filtered_df = filtered_df[filtered_df['dish'].isin(selected_dishes)]
    
    # Compute insights
    insights = compute_business_insights(filtered_df)
    
    # KPI Cards
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 2rem;">🎯 Key Performance Indicators</h2>
    </div>
    """, unsafe_allow_html=True)
    
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        st.metric(
            "🏆 Top Dish",
            insights['top_dish'],
            f"{insights['top_dish_demand']:,} demand"
        )
    
    with kpi_col2:
        st.metric(
            "🏢 Leading Outlet", 
            insights['top_outlet'],
            f"{insights['top_outlet_demand']:,} demand"
        )
    
    with kpi_col3:
        st.metric(
            "⚖️ Most Variable",
            insights['most_unbalanced_dish'],
            f"CV: {insights['unbalance_coefficient']:.2f}"
        )
    
    # Operational metrics
    op_col1, op_col2, op_col3, op_col4 = st.columns(4)
    
    avg_demand = int(filtered_df['predicted_demand'].mean())
    total_demand = int(filtered_df['predicted_demand'].sum())
    
    with op_col1:
        st.metric("📅 Peak Day", insights['peak_day'].strftime("%a, %b %d"), f"{insights['peak_day_demand']:,}")
    with op_col2:
        st.metric("🎯 Most Consistent", insights['most_consistent_dish'], "Low variance")
    with op_col3:
        st.metric("📈 Avg Daily", f"{avg_demand:,}", f"Per dish: {insights['avg_demand_per_dish']:.1f}")
    with op_col4:
        st.metric("💰 Total Demand", f"{total_demand:,}", f"{filtered_df['outlet'].nunique()} outlets")
    
    st.markdown("---")
    
    # Heatmap section
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 2rem;">🔥 Interactive Demand Heatmap</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Heatmap controls
    control_col1, control_col2, control_col3 = st.columns([2, 1, 1])
    
    with control_col1:
        st.markdown(f"""
        <div style="padding: 1rem; background: #2a2a3e; border-radius: 10px; text-align: center;">
            <h4 style="color: #FF6B35; margin: 0 0 0.5rem 0;">📊 Data Overview</h4>
            <p style="color: #E8F4FD; margin: 0; font-size: 0.9rem;">
                <strong>{len(filtered_df):,} records</strong> across <strong>{filtered_df['outlet'].nunique()} outlets</strong> and <strong>{filtered_df['dish'].nunique()} dishes</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with control_col2:
        heatmap_mode = st.selectbox("🎨 Heatmap Mode", ["Absolute Demand", "Normalized Demand"])
    
    with control_col3:
        color_scale = st.selectbox("🌈 Color Scale", ["Viridis", "Inferno", "Plasma", "Turbo"])
    
    # Generate heatmap
    use_normalized = normalize_demand or (heatmap_mode == "Normalized Demand")
    heatmap_fig = generate_heatmap(
        filtered_df, 
        value_mode=demand_mode, 
        top_n_dishes=top_n_dishes,
        normalize=use_normalized,
        color_scale=color_scale.lower()
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    # Detailed analytics tabs
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="color: #E8F4FD; font-family: 'Poppins', sans-serif; font-size: 2rem;">📊 Detailed Analytics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏢 Outlets", "🍽️ Dishes", "💡 Insights"])
    
    with tab1:
        st.markdown("### 📈 Demand Trends Over Time")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_dish = st.selectbox(
                "Select Dish (Optional)",
                options=[None] + sorted(df['dish'].unique().tolist()),
                format_func=lambda x: "All Dishes" if x is None else x
            )
        with col2:
            selected_outlet = st.selectbox(
                "Select Outlet (Optional)",
                options=[None] + sorted(df['outlet'].unique().tolist()),
                format_func=lambda x: "All Outlets" if x is None else x
            )
        
        trend_fig = generate_trend_chart(df, dish_name=selected_dish, outlet_name=selected_outlet)
        st.plotly_chart(trend_fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🏢 Outlet Performance Comparison")
        outlet_fig = generate_comparison_bar_chart(df, comparison_type="outlet")
        st.plotly_chart(outlet_fig, use_container_width=True)
        
        # Outlet performance table
        outlet_performance = df.groupby('outlet').agg({
            'predicted_demand': ['sum', 'mean', 'count']
        }).round(2)
        outlet_performance.columns = ['Total Demand', 'Avg Demand', 'Dish Count']
        st.dataframe(outlet_performance.sort_values('Total Demand', ascending=False))
    
    with tab3:
        st.markdown("### 🍽️ Dish Performance Analysis")
        dish_fig = generate_comparison_bar_chart(df, comparison_type="dish")
        st.plotly_chart(dish_fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏆 Top Performing Dishes")
            top_dishes = df.groupby('dish')['predicted_demand'].sum().nlargest(10)
            for i, (dish, demand) in enumerate(top_dishes.items(), 1):
                st.write(f"{i}. **{dish}**: {demand:,}")
        
        with col2:
            st.markdown("#### ⚖️ Most Consistent Dishes")
            dish_cv = df.groupby('dish')['predicted_demand'].agg(['mean', 'std'])
            dish_cv['cv'] = dish_cv['std'] / dish_cv['mean']
            most_consistent = dish_cv.nsmallest(10, 'cv')
            for i, (dish, data) in enumerate(most_consistent.iterrows(), 1):
                st.write(f"{i}. **{dish}**: CV = {data['cv']:.2f}")
    
    with tab4:
        st.markdown("### 💡 Business Intelligence")
        
        insight_texts = generate_insight_texts(insights)
        recommendations = generate_recommendations(insights)
        
        st.markdown("#### 🚨 Business Alerts")
        
        # Sample alerts
        col1, col2 = st.columns(2)
        with col1:
            worst_dish = min(insights['worst_dish_per_outlet'].items(), key=lambda x: x[1]['demand'])
            alert_text = f"Low Performance: {worst_dish[1]['dish']} at {worst_dish[0]} shows only {worst_dish[1]['demand']:,} demand"
            st.markdown(create_alert_card(alert_text, "warning"), unsafe_allow_html=True)
        
        with col2:
            best_dish = max(insights['best_dish_per_outlet'].items(), key=lambda x: x[1]['demand'])
            success_text = f"Success Story: {best_dish[1]['dish']} at {best_dish[0]} shows {best_dish[1]['demand']:,} demand"
            st.markdown(create_alert_card(success_text, "success"), unsafe_allow_html=True)
        
        st.markdown("#### 🔍 Key Insights")
        for i, insight in enumerate(insight_texts[:4], 1):
            st.markdown(create_insight_card(f"Insight {i}", insight), unsafe_allow_html=True)
        
        st.markdown("#### 🚀 Recommendations")
        for i, rec in enumerate(recommendations[:3], 1):
            st.markdown(create_alert_card(f"Priority {i}: {rec}", "info"), unsafe_allow_html=True)
        
        # Export options
        st.markdown("---")
        st.markdown("#### 📥 Export Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                "📊 Download Dataset",
                data=csv_data,
                file_name=f"kkcg_analytics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            insights_text = "\n".join([f"• {insight}" for insight in insight_texts])
            recommendations_text = "\n".join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])
            
            summary_report = f"""KKCG Analytics Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

KEY INSIGHTS:
{insights_text}

RECOMMENDATIONS:
{recommendations_text}

DATA SUMMARY:
- Total Records: {len(filtered_df):,}
- Outlets: {filtered_df['outlet'].nunique()}
- Dishes: {filtered_df['dish'].nunique()}
- Total Demand: {filtered_df['predicted_demand'].sum():,}
"""
            
            st.download_button(
                "📄 Download Report",
                data=summary_report,
                file_name=f"kkcg_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    main() 