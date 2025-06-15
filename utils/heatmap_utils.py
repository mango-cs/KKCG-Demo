"""
Heatmap utilities for KKCG Analytics Dashboard
Backend-only mode utility functions
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_demand_heatmap(data, value_mode='predicted_demand', top_n_dishes=None, normalize=False, color_scale='viridis'):
    """
    Create a demand heatmap from backend data
    """
    if data.empty:
        return None
    
    try:
        # Ensure required columns exist
        if 'dish' not in data.columns or 'outlet' not in data.columns or value_mode not in data.columns:
            return None
        
        # Filter top dishes if specified
        if top_n_dishes and top_n_dishes > 0:
            top_dishes = data.groupby('dish')[value_mode].sum().nlargest(top_n_dishes).index
            data = data[data['dish'].isin(top_dishes)]
        
        # Create pivot table
        pivot_data = data.pivot_table(
            values=value_mode,
            index='dish',
            columns='outlet',
            aggfunc='mean',
            fill_value=0
        )
        
        if pivot_data.empty:
            return None
        
        # Normalize if requested
        if normalize:
            pivot_data = pivot_data.div(pivot_data.max(axis=1), axis=0).fillna(0)
        
        # Create heatmap
        fig = px.imshow(
            pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            aspect='auto',
            color_continuous_scale=color_scale,
            title=f"Demand Heatmap - {value_mode.replace('_', ' ').title()}"
        )
        
        # Update layout for dark theme
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=20,
            title_font_color='#FF6B35'
        )
        
        return fig
        
    except Exception as e:
        return None

def generate_ai_insights(data):
    """
    Generate AI insights from backend data
    """
    insights = []
    
    if data.empty:
        return ["No data available for analysis"]
    
    try:
        # Basic insights based on data
        total_demand = data['predicted_demand'].sum() if 'predicted_demand' in data.columns else 0
        avg_demand = data['predicted_demand'].mean() if 'predicted_demand' in data.columns else 0
        unique_dishes = data['dish'].nunique() if 'dish' in data.columns else 0
        unique_outlets = data['outlet'].nunique() if 'outlet' in data.columns else 0
        
        insights = [
            f"📊 Total demand across all outlets: {total_demand:,.0f} units",
            f"📈 Average demand per item: {avg_demand:.1f} units",
            f"🍽️ Active menu items: {unique_dishes} dishes",
            f"🏢 Restaurant locations: {unique_outlets} outlets",
            f"🎯 Data coverage: {len(data):,} records analyzed"
        ]
        
        # Add performance insights
        if 'dish' in data.columns and 'predicted_demand' in data.columns:
            top_dish = data.groupby('dish')['predicted_demand'].sum().idxmax()
            insights.append(f"🥇 Top performing dish: {top_dish}")
        
        if 'outlet' in data.columns and 'predicted_demand' in data.columns:
            top_outlet = data.groupby('outlet')['predicted_demand'].sum().idxmax()
            insights.append(f"🏆 Top performing outlet: {top_outlet}")
        
        return insights
        
    except Exception:
        return ["Analysis completed with backend data"]

def get_performance_metrics(data):
    """
    Calculate performance metrics from backend data
    """
    metrics = {}
    
    if data.empty:
        return metrics
    
    try:
        if 'predicted_demand' in data.columns:
            metrics['total_demand'] = data['predicted_demand'].sum()
            metrics['average_demand'] = data['predicted_demand'].mean()
            metrics['max_demand'] = data['predicted_demand'].max()
            metrics['min_demand'] = data['predicted_demand'].min()
            metrics['demand_std'] = data['predicted_demand'].std()
        
        if 'dish' in data.columns:
            metrics['unique_dishes'] = data['dish'].nunique()
            metrics['total_records'] = len(data)
        
        if 'outlet' in data.columns:
            metrics['unique_outlets'] = data['outlet'].nunique()
        
        if 'date' in data.columns:
            metrics['date_range'] = (data['date'].max() - data['date'].min()).days
            metrics['latest_date'] = data['date'].max().strftime('%Y-%m-%d')
        
        return metrics
        
    except Exception:
        return metrics

def generate_comparison_bar_chart(data, comparison_type="outlet"):
    """
    Generate comparison bar chart for outlets or dishes
    """
    if data.empty:
        return None
    
    try:
        if comparison_type == "outlet" and 'outlet' in data.columns:
            grouped_data = data.groupby('outlet')['predicted_demand'].sum().sort_values(ascending=True)
            title = "Outlet Performance Comparison"
        elif comparison_type == "dish" and 'dish' in data.columns:
            grouped_data = data.groupby('dish')['predicted_demand'].sum().sort_values(ascending=True)
            title = "Dish Performance Comparison"
        else:
            return None
        
        fig = px.bar(
            x=grouped_data.values,
            y=grouped_data.index,
            orientation='h',
            title=title,
            labels={'x': 'Total Demand', 'y': comparison_type.title()},
            color=grouped_data.values,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=18,
            title_font_color='#FF6B35'
        )
        
        return fig
        
    except Exception:
        return None

def generate_trend_chart(data, dish_name=None, outlet_name=None):
    """
    Generate trend chart for specific dish/outlet combination
    """
    if data.empty or 'date' not in data.columns:
        return None
    
    try:
        filtered_data = data.copy()
        
        if dish_name and dish_name != "All Dishes":
            filtered_data = filtered_data[filtered_data['dish'] == dish_name]
        
        if outlet_name and outlet_name != "All Outlets":
            filtered_data = filtered_data[filtered_data['outlet'] == outlet_name]
        
        if filtered_data.empty:
            return None
        
        # Group by date
        trend_data = filtered_data.groupby('date')['predicted_demand'].sum().reset_index()
        
        fig = px.line(
            trend_data,
            x='date',
            y='predicted_demand',
            title=f"Demand Trend - {dish_name or 'All Dishes'} at {outlet_name or 'All Outlets'}",
            labels={'predicted_demand': 'Total Demand', 'date': 'Date'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=18,
            title_font_color='#FF6B35'
        )
        
        fig.update_traces(line_color='#FF6B35', line_width=3)
        
        return fig
        
    except Exception:
        return None

# Additional utility functions for compatibility
def calculate_heatmap_statistics(data):
    """Calculate statistics for heatmap display"""
    if data.empty:
        return {}
    
    try:
        stats = {
            'total_records': len(data),
            'total_demand': data['predicted_demand'].sum() if 'predicted_demand' in data.columns else 0,
            'avg_demand': data['predicted_demand'].mean() if 'predicted_demand' in data.columns else 0,
            'unique_items': data['dish'].nunique() if 'dish' in data.columns else 0,
            'unique_locations': data['outlet'].nunique() if 'outlet' in data.columns else 0
        }
        return stats
    except Exception:
        return {}

def validate_heatmap_data(data):
    """Validate data structure for heatmap creation"""
    required_columns = ['dish', 'outlet', 'predicted_demand']
    if data.empty:
        return False
    return all(col in data.columns for col in required_columns) 