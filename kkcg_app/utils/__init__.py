# KKCG Analytics Utilities Package
# This package contains utility modules for the KKCG multipage Streamlit app

from .data_simulation import generate_demand_data, SOUTH_INDIAN_DISHES, OUTLETS
from .heatmap_utils import generate_heatmap, generate_trend_chart, generate_comparison_bar_chart
from .insights import compute_business_insights, generate_insight_texts, generate_recommendations

__all__ = [
    'generate_demand_data',
    'SOUTH_INDIAN_DISHES', 
    'OUTLETS',
    'generate_heatmap',
    'generate_trend_chart', 
    'generate_comparison_bar_chart',
    'compute_business_insights',
    'generate_insight_texts',
    'generate_recommendations'
] 