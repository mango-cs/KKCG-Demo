import pandas as pd
import numpy as np
from datetime import datetime

def compute_business_insights(df):
    """
    Compute comprehensive business insights from demand data
    
    Args:
        df: DataFrame with columns [date, dish, outlet, predicted_demand]
    
    Returns:
        Dictionary containing various business insights
    """
    
    insights = {}
    
    # Top performing dish overall
    dish_totals = df.groupby('dish')['predicted_demand'].sum()
    insights['top_dish'] = dish_totals.idxmax()
    insights['top_dish_demand'] = dish_totals.max()
    
    # Top performing outlet
    outlet_totals = df.groupby('outlet')['predicted_demand'].sum()
    insights['top_outlet'] = outlet_totals.idxmax()
    insights['top_outlet_demand'] = outlet_totals.max()
    
    # Peak demand day
    daily_totals = df.groupby('date')['predicted_demand'].sum()
    peak_date = daily_totals.idxmax()
    insights['peak_day'] = peak_date
    insights['peak_day_demand'] = daily_totals.max()
    
    # Most consistent dish (lowest coefficient of variation)
    dish_consistency = df.groupby('dish')['predicted_demand'].agg(['mean', 'std'])
    dish_consistency['cv'] = dish_consistency['std'] / dish_consistency['mean']
    insights['most_consistent_dish'] = dish_consistency['cv'].idxmin()
    
    # Most variable dish (highest coefficient of variation)
    insights['most_unbalanced_dish'] = dish_consistency['cv'].idxmax()
    insights['unbalance_coefficient'] = dish_consistency['cv'].max()
    
    # Average demand per dish
    insights['avg_demand_per_dish'] = df.groupby('dish')['predicted_demand'].mean().mean()
    
    # Best performing dish per outlet
    best_dish_per_outlet = {}
    for outlet in df['outlet'].unique():
        outlet_data = df[df['outlet'] == outlet]
        dish_sums = outlet_data.groupby('dish')['predicted_demand'].sum()
        best_dish = dish_sums.idxmax()
        best_dish_per_outlet[outlet] = {
            'dish': best_dish,
            'demand': dish_sums.max()
        }
    insights['best_dish_per_outlet'] = best_dish_per_outlet
    
    # Worst performing dish per outlet
    worst_dish_per_outlet = {}
    for outlet in df['outlet'].unique():
        outlet_data = df[df['outlet'] == outlet]
        dish_sums = outlet_data.groupby('dish')['predicted_demand'].sum()
        worst_dish = dish_sums.idxmin()
        worst_dish_per_outlet[outlet] = {
            'dish': worst_dish,
            'demand': dish_sums.min()
        }
    insights['worst_dish_per_outlet'] = worst_dish_per_outlet
    
    return insights

def generate_insight_texts(insights):
    """
    Generate human-readable insight texts from computed insights
    
    Args:
        insights: Dictionary from compute_business_insights()
    
    Returns:
        List of insight text strings
    """
    
    texts = []
    
    # Top dish insight
    texts.append(f"🏆 **{insights['top_dish']}** is your star performer with {insights['top_dish_demand']:,} total demand across all outlets.")
    
    # Top outlet insight
    texts.append(f"🏢 **{insights['top_outlet']}** leads in performance, generating {insights['top_outlet_demand']:,} total demand this week.")
    
    # Peak day insight
    peak_day_name = insights['peak_day'].strftime('%A')
    texts.append(f"📅 **{peak_day_name}s** are your busiest days with {insights['peak_day_demand']:,} demand recorded.")
    
    # Consistency insight
    texts.append(f"⚖️ **{insights['most_consistent_dish']}** shows the most consistent demand across all outlets, indicating reliable customer preference.")
    
    # Variability insight
    if insights['unbalance_coefficient'] > 0.4:
        texts.append(f"⚠️ **{insights['most_unbalanced_dish']}** shows high demand variation (CV: {insights['unbalance_coefficient']:.2f}) - consider standardizing preparation or pricing.")
    else:
        texts.append(f"✅ **{insights['most_unbalanced_dish']}** has moderate variation, suggesting good operational consistency.")
    
    # Outlet-specific insights
    for outlet, data in insights['best_dish_per_outlet'].items():
        texts.append(f"🌟 At **{outlet}**, **{data['dish']}** dominates with {data['demand']:,} demand.")
    
    return texts

def generate_recommendations(insights):
    """
    Generate actionable business recommendations
    
    Args:
        insights: Dictionary from compute_business_insights()
    
    Returns:
        List of recommendation strings
    """
    
    recommendations = []
    
    # Top dish recommendation
    recommendations.append(f"Capitalize on {insights['top_dish']}'s success by ensuring consistent quality and availability. Consider featuring it in promotional campaigns.")
    
    # Top outlet recommendation
    recommendations.append(f"Study {insights['top_outlet']}'s operations as a benchmark. Implement their best practices across other outlets.")
    
    # Peak day preparation
    peak_day_name = insights['peak_day'].strftime('%A')
    recommendations.append(f"Optimize staffing and inventory for {peak_day_name}s to handle the {insights['peak_day_demand']:,} demand surge efficiently.")
    
    # Consistency optimization
    if insights['unbalance_coefficient'] > 0.5:
        recommendations.append(f"Address {insights['most_unbalanced_dish']}'s inconsistent performance through standardized recipes and staff training.")
    
    # Outlet-specific recommendations
    outlet_demands = {k: v['demand'] for k, v in insights['best_dish_per_outlet'].items()}
    min_outlet = min(outlet_demands, key=outlet_demands.get)
    max_outlet = max(outlet_demands, key=outlet_demands.get)
    
    recommendations.append(f"Consider menu optimization at {min_outlet} by introducing successful items from {max_outlet}.")
    
    # Performance improvement
    recommendations.append("Implement cross-outlet knowledge sharing sessions to standardize high-performing practices across all locations.")
    
    return recommendations

def create_kpi_summary(df):
    """
    Create a summary of key performance indicators
    
    Args:
        df: DataFrame with demand data
    
    Returns:
        Dictionary with KPI values
    """
    
    kpis = {
        'total_demand': df['predicted_demand'].sum(),
        'avg_daily_demand': df.groupby('date')['predicted_demand'].sum().mean(),
        'total_dishes': df['dish'].nunique(),
        'total_outlets': df['outlet'].nunique(),
        'peak_single_day': df.groupby('date')['predicted_demand'].sum().max(),
        'best_dish_overall': df.groupby('dish')['predicted_demand'].sum().idxmax(),
        'best_outlet_overall': df.groupby('outlet')['predicted_demand'].sum().idxmax(),
        'demand_range': {
            'min': df['predicted_demand'].min(),
            'max': df['predicted_demand'].max(),
            'std': df['predicted_demand'].std()
        }
    }
    
    return kpis 