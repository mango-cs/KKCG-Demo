import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def generate_heatmap(df, value_mode="total", top_n_dishes=None, normalize=False, color_scale="viridis"):
    """
    Generate enhanced interactive heatmap with outlets as Y-axis and dishes as X-axis
    
    Args:
        df: DataFrame with columns [dish, outlet, predicted_demand, date]
        value_mode: "total" for sum, "average" for mean per date
        top_n_dishes: Number of top dishes to display (None for all)
        normalize: Whether to normalize demand per outlet
        color_scale: Color scale for the heatmap
    
    Returns:
        Plotly figure object
    """
    
    # Aggregate data based on value_mode
    if value_mode == "total":
        pivot_data = df.groupby(['outlet', 'dish'])['predicted_demand'].sum().reset_index()
        title_suffix = "Total Demand"
        hover_template = "<b>%{y}</b><br>%{x}<br><b>Total Demand: %{z}</b><extra></extra>"
    else:  # average
        pivot_data = df.groupby(['outlet', 'dish'])['predicted_demand'].mean().reset_index()
        title_suffix = "Average Daily Demand"
        hover_template = "<b>%{y}</b><br>%{x}<br><b>Avg Daily Demand: %{z:.0f}</b><extra></extra>"
    
    # Filter top N dishes if specified
    if top_n_dishes:
        top_dishes = pivot_data.groupby('dish')['predicted_demand'].sum().nlargest(top_n_dishes).index
        pivot_data = pivot_data[pivot_data['dish'].isin(top_dishes)]
    
    # Create pivot table for heatmap
    heatmap_data = pivot_data.pivot(index='outlet', columns='dish', values='predicted_demand')
    
    # Fill NaN values with 0
    heatmap_data = heatmap_data.fillna(0)
    
    # Apply normalization if requested
    if normalize:
        # Normalize each row (outlet) to show relative performance
        heatmap_data = heatmap_data.div(heatmap_data.sum(axis=1), axis=0).fillna(0)
        title_suffix += " (Normalized)"
        if value_mode == "total":
            hover_template = "<b>%{y}</b><br>%{x}<br><b>Relative Demand: %{z:.2%}</b><extra></extra>"
        else:
            hover_template = "<b>%{y}</b><br>%{x}<br><b>Relative Avg Demand: %{z:.2%}</b><extra></extra>"
    
    # Sort outlets (put Jubilee Hills first as it's premium)
    outlet_order = ["Jubilee Hills", "Chennai Central", "Madhapur"]
    heatmap_data = heatmap_data.reindex([o for o in outlet_order if o in heatmap_data.index])
    
    # Sort dishes by total demand (descending)
    if normalize:
        # For normalized data, sort by original totals
        original_totals = pivot_data.groupby('dish')['predicted_demand'].sum().sort_values(ascending=False)
        available_dishes = [dish for dish in original_totals.index if dish in heatmap_data.columns]
        heatmap_data = heatmap_data[available_dishes]
    else:
        dish_totals = heatmap_data.sum(axis=0).sort_values(ascending=False)
        heatmap_data = heatmap_data[dish_totals.index]
    
    # Create the enhanced heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale=color_scale.title(),
        hovertemplate=hover_template,
        showscale=True,
        colorbar={
            "title": title_suffix,
            "titleside": "right"
        }
    ))
    
    # Add text annotations on cells (only for top values to avoid clutter)
    if len(heatmap_data.columns) <= 20:  # Only show annotations for smaller heatmaps
        for i, outlet in enumerate(heatmap_data.index):
            for j, dish in enumerate(heatmap_data.columns):
                value = heatmap_data.iloc[i, j]
                if value > 0:  # Only show non-zero values
                    if normalize:
                        display_text = f"{value:.1%}" if value >= 0.01 else ""  # Show as percentage
                    else:
                        display_text = str(int(value)) if value >= 10 else ""  # Only show significant values
                    
                    if display_text:
                        fig.add_annotation(
                            x=j, y=i,
                            text=display_text,
                            showarrow=False,
                            font=dict(color="white", size=9, family="Inter"),
                            bgcolor="rgba(0,0,0,0.4)",
                            bordercolor="rgba(255,255,255,0.2)",
                            borderwidth=1
                        )
    
    # Update layout for dark theme
    fig.update_layout(
        title=dict(
            text=f"<b>🔥 Demand Heatmap - {title_suffix}</b>",
            x=0.5,
            font=dict(size=20, color='white', family="Inter")
        ),
        xaxis=dict(
            title="<b>Dishes</b>",
            tickfont=dict(size=10, color='white'),
            tickangle=45,
            side='bottom'
        ),
        yaxis=dict(
            title="<b>Outlets</b>",
            tickfont=dict(size=12, color='white')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color='white'),
        height=400,
        margin=dict(t=80, b=120, l=120, r=80)
    )
    
    return fig

def generate_trend_chart(df, dish_name=None, outlet_name=None):
    """
    Generate a trend line chart for demand over time
    
    Args:
        df: DataFrame with demand data
        dish_name: Specific dish to filter (optional)
        outlet_name: Specific outlet to filter (optional)
    
    Returns:
        Plotly figure object
    """
    
    # Filter data if specified
    filtered_df = df.copy()
    if dish_name:
        filtered_df = filtered_df[filtered_df['dish'] == dish_name]
    if outlet_name:
        filtered_df = filtered_df[filtered_df['outlet'] == outlet_name]
    
    # Group by date and sum demand
    trend_data = filtered_df.groupby('date')['predicted_demand'].sum().reset_index()
    
    # Create line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_data['date'],
        y=trend_data['predicted_demand'],
        mode='lines+markers',
        name='Demand',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=8, color='#FF6B35'),
        hovertemplate="<b>Date: %{x}</b><br>Demand: %{y}<extra></extra>"
    ))
    
    # Update layout
    title_text = "Demand Trend"
    if dish_name and outlet_name:
        title_text += f" - {dish_name} at {outlet_name}"
    elif dish_name:
        title_text += f" - {dish_name}"
    elif outlet_name:
        title_text += f" - {outlet_name}"
    
    fig.update_layout(
        title=dict(
            text=f"<b>📈 {title_text}</b>",
            x=0.5,
            font=dict(size=18, color='white', family="Inter")
        ),
        xaxis=dict(
            title="<b>Date</b>",
            tickfont=dict(size=10, color='white'),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title="<b>Predicted Demand</b>",
            tickfont=dict(size=10, color='white'),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color='white'),
        height=300,
        showlegend=False
    )
    
    return fig

def generate_comparison_bar_chart(df, comparison_type="outlet"):
    """
    Generate bar chart comparing demand across outlets or dishes
    
    Args:
        df: DataFrame with demand data
        comparison_type: "outlet" or "dish"
    
    Returns:
        Plotly figure object
    """
    
    if comparison_type == "outlet":
        grouped_data = df.groupby('outlet')['predicted_demand'].sum().sort_values(ascending=True)
        title = "Total Demand by Outlet"
        x_title = "Total Demand"
        y_title = "Outlets"
    else:  # dish
        grouped_data = df.groupby('dish')['predicted_demand'].sum().sort_values(ascending=False).head(10)
        title = "Top 10 Dishes by Demand"
        x_title = "Dishes"
        y_title = "Total Demand"
    
    fig = go.Figure()
    
    if comparison_type == "outlet":
        fig.add_trace(go.Bar(
            x=grouped_data.values,
            y=grouped_data.index,
            orientation='h',
            marker=dict(color='#FF6B35'),
            hovertemplate="<b>%{y}</b><br>Total Demand: %{x}<extra></extra>"
        ))
    else:
        fig.add_trace(go.Bar(
            x=grouped_data.index,
            y=grouped_data.values,
            marker=dict(color='#FF6B35'),
            hovertemplate="<b>%{x}</b><br>Total Demand: %{y}<extra></extra>"
        ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>📊 {title}</b>",
            x=0.5,
            font=dict(size=18, color='white', family="Inter")
        ),
        xaxis=dict(
            title=f"<b>{x_title}</b>",
            tickfont=dict(size=10, color='white'),
            tickangle=45 if comparison_type == "dish" else 0
        ),
        yaxis=dict(
            title=f"<b>{y_title}</b>",
            tickfont=dict(size=10, color='white')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color='white'),
        height=400,
        showlegend=False
    )
    
    return fig 