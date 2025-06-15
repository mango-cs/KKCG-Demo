import pandas as pd
import numpy as np

def compute_business_insights(df):
    """
    Compute key business insights from demand data
    
    Args:
        df: DataFrame with columns [dish, outlet, predicted_demand, date]
    
    Returns:
        Dictionary with business insights
    """
    
    # 1. Top-selling dish overall
    dish_totals = df.groupby('dish')['predicted_demand'].sum().sort_values(ascending=False)
    top_dish = dish_totals.index[0]
    top_dish_demand = dish_totals.iloc[0]
    
    # 2. Outlet with highest total demand
    outlet_totals = df.groupby('outlet')['predicted_demand'].sum().sort_values(ascending=False)
    top_outlet = outlet_totals.index[0]
    top_outlet_demand = outlet_totals.iloc[0]
    
    # 3. Dish with maximum variation across outlets (coefficient of variation)
    dish_outlet_stats = df.groupby(['dish', 'outlet'])['predicted_demand'].sum().unstack(fill_value=0)
    
    # Calculate coefficient of variation for each dish across outlets
    dish_cv = {}
    for dish in dish_outlet_stats.index:
        values = dish_outlet_stats.loc[dish].values
        if values.mean() > 0:  # Avoid division by zero
            cv = values.std() / values.mean()
            dish_cv[dish] = cv
    
    # Find dish with highest coefficient of variation
    most_unbalanced_dish = max(dish_cv.keys(), key=lambda x: dish_cv[x])
    max_cv = dish_cv[most_unbalanced_dish]
    
    # 4. Additional insights
    
    # Best performing dish per outlet
    best_dish_per_outlet = {}
    for outlet in df['outlet'].unique():
        outlet_data = df[df['outlet'] == outlet]
        best_dish = outlet_data.groupby('dish')['predicted_demand'].sum().idxmax()
        best_demand = outlet_data.groupby('dish')['predicted_demand'].sum().max()
        best_dish_per_outlet[outlet] = {
            'dish': best_dish,
            'demand': best_demand
        }
    
    # Worst performing dish per outlet
    worst_dish_per_outlet = {}
    for outlet in df['outlet'].unique():
        outlet_data = df[df['outlet'] == outlet]
        worst_dish = outlet_data.groupby('dish')['predicted_demand'].sum().idxmin()
        worst_demand = outlet_data.groupby('dish')['predicted_demand'].sum().min()
        worst_dish_per_outlet[outlet] = {
            'dish': worst_dish,
            'demand': worst_demand
        }
    
    # Day with highest demand
    daily_demand = df.groupby('date')['predicted_demand'].sum().sort_values(ascending=False)
    peak_day = daily_demand.index[0]
    peak_day_demand = daily_demand.iloc[0]
    
    # Average demand per dish
    avg_demand_per_dish = df.groupby('dish')['predicted_demand'].mean().mean()
    
    # Demand consistency (dishes with low variation across days)
    dish_daily_cv = {}
    for dish in df['dish'].unique():
        dish_data = df[df['dish'] == dish].groupby('date')['predicted_demand'].sum()
        if dish_data.mean() > 0:
            cv = dish_data.std() / dish_data.mean()
            dish_daily_cv[dish] = cv
    
    most_consistent_dish = min(dish_daily_cv.keys(), key=lambda x: dish_daily_cv[x])
    
    return {
        'top_dish': top_dish,
        'top_dish_demand': int(top_dish_demand),
        'top_outlet': top_outlet,
        'top_outlet_demand': int(top_outlet_demand),
        'most_unbalanced_dish': most_unbalanced_dish,
        'unbalance_coefficient': round(max_cv, 2),
        'best_dish_per_outlet': best_dish_per_outlet,
        'worst_dish_per_outlet': worst_dish_per_outlet,
        'peak_day': peak_day,
        'peak_day_demand': int(peak_day_demand),
        'avg_demand_per_dish': round(avg_demand_per_dish, 1),
        'most_consistent_dish': most_consistent_dish,
        'total_dishes': df['dish'].nunique(),
        'total_outlets': df['outlet'].nunique(),
        'date_range': {
            'start': df['date'].min(),
            'end': df['date'].max()
        }
    }

def generate_insight_texts(insights):
    """
    Generate human-readable insight texts for display
    
    Args:
        insights: Dictionary from compute_business_insights()
    
    Returns:
        List of insight strings
    """
    
    texts = []
    
    # Main insights
    texts.append(f"🏆 **{insights['top_dish']}** is the star performer with {insights['top_dish_demand']:,} total demand across all outlets")
    
    texts.append(f"🏢 **{insights['top_outlet']}** leads with {insights['top_outlet_demand']:,} total demand, making it our busiest location")
    
    texts.append(f"⚖️ **{insights['most_unbalanced_dish']}** shows the highest demand variation across outlets (CV: {insights['unbalance_coefficient']})")
    
    # Outlet-specific insights
    texts.append("📍 **Outlet Champions:**")
    for outlet, data in insights['best_dish_per_outlet'].items():
        texts.append(f"   • {outlet}: **{data['dish']}** ({data['demand']:,} demand)")
    
    # Performance insights
    texts.append(f"📅 Peak day was **{insights['peak_day']}** with {insights['peak_day_demand']:,} total demand")
    
    texts.append(f"🎯 **{insights['most_consistent_dish']}** shows the most consistent daily demand pattern")
    
    texts.append(f"📊 Average demand per dish: **{insights['avg_demand_per_dish']}** units")
    
    return texts

def get_outlet_comparison_insights(df):
    """
    Generate specific insights comparing outlets
    
    Args:
        df: DataFrame with demand data
    
    Returns:
        Dictionary with outlet comparison insights
    """
    
    outlet_stats = df.groupby('outlet').agg({
        'predicted_demand': ['sum', 'mean', 'std', 'count']
    }).round(2)
    
    outlet_stats.columns = ['total_demand', 'avg_demand', 'std_demand', 'dish_count']
    outlet_stats = outlet_stats.reset_index()
    
    # Performance ranking
    outlet_stats['rank'] = outlet_stats['total_demand'].rank(ascending=False)
    
    # Demand per dish variety
    outlet_stats['demand_per_variety'] = outlet_stats['total_demand'] / outlet_stats['dish_count']
    
    return outlet_stats.to_dict('records')

def get_dish_performance_insights(df, top_n=10):
    """
    Generate insights about dish performance
    
    Args:
        df: DataFrame with demand data
        top_n: Number of top dishes to analyze
    
    Returns:
        Dictionary with dish performance insights
    """
    
    # Overall dish performance
    dish_stats = df.groupby('dish').agg({
        'predicted_demand': ['sum', 'mean', 'std']
    }).round(2)
    
    dish_stats.columns = ['total_demand', 'avg_demand', 'std_demand']
    dish_stats = dish_stats.reset_index()
    
    # Add coefficient of variation
    dish_stats['cv'] = dish_stats['std_demand'] / dish_stats['avg_demand']
    
    # Top performers
    top_dishes = dish_stats.nlargest(top_n, 'total_demand')
    
    # Most consistent (low CV)
    most_consistent = dish_stats.nsmallest(5, 'cv')
    
    # Most variable (high CV)
    most_variable = dish_stats.nlargest(5, 'cv')
    
    return {
        'top_dishes': top_dishes.to_dict('records'),
        'most_consistent': most_consistent.to_dict('records'),
        'most_variable': most_variable.to_dict('records'),
        'overall_stats': {
            'total_dishes': len(dish_stats),
            'avg_demand_all': dish_stats['total_demand'].mean(),
            'median_demand': dish_stats['total_demand'].median()
        }
    }

def generate_recommendations(insights):
    """
    Generate actionable business recommendations based on insights
    
    Args:
        insights: Dictionary from compute_business_insights()
    
    Returns:
        List of recommendation strings
    """
    
    recommendations = []
    
    # Top dish recommendations
    recommendations.append(f"🚀 **Promote {insights['top_dish']}** - It's your best performer! Consider featuring it prominently in all outlets.")
    
    # Outlet optimization
    if insights['top_outlet'] == "Jubilee Hills":
        recommendations.append("💎 **Jubilee Hills** is your premium location - consider introducing high-margin specialty items here.")
    elif insights['top_outlet'] == "Chennai Central":
        recommendations.append("🚄 **Chennai Central** benefits from high foot traffic - optimize for quick service items.")
    else:
        recommendations.append("🏙️ **Madhapur** shows strong performance - replicate successful strategies across other outlets.")
    
    # Unbalanced dish optimization
    recommendations.append(f"⚡ **{insights['most_unbalanced_dish']}** performs inconsistently across outlets - investigate local preferences and adjust recipes or marketing.")
    
    # Consistent performer leverage
    recommendations.append(f"🎯 **{insights['most_consistent_dish']}** is reliable - use it as a baseline offering and build promotions around it.")
    
    # Operational insights
    recommendations.append(f"📈 **Peak day strategy**: {insights['peak_day'].strftime('%A')}s see highest demand - ensure adequate staffing and inventory.")
    
    return recommendations 