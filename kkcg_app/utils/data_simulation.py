import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# South Indian dishes with authentic names
SOUTH_INDIAN_DISHES = [
    "Masala Dosa", "Plain Dosa", "Rava Dosa", "Mysore Masala Dosa", "Onion Dosa",
    "Idli", "Sambar Idli", "Rava Idli", "Mini Idli", "Ghee Idli",
    "Vada", "Sambar Vada", "Dahi Vada", "Medu Vada", "Masala Vada",
    "Uttapam", "Onion Uttapam", "Tomato Uttapam", "Mixed Veg Uttapam", "Cheese Uttapam",
    "Upma", "Rava Upma", "Vegetable Upma", "Tomato Upma", "Lemon Upma",
    "Pongal", "Ven Pongal", "Khara Pongal", "Sweet Pongal", "Ghee Pongal",
    "Sambar Rice", "Rasam Rice", "Curd Rice", "Lemon Rice", "Coconut Rice",
    "Poori", "Chapati", "Paratha", "Aloo Paratha", "Gobi Paratha",
    "Filter Coffee", "South Indian Coffee", "Masala Tea", "Buttermilk", "Fresh Lime"
]

# Restaurant outlets in South India
OUTLETS = [
    "Madhapur", "Jubilee Hills", "Chennai Central"
]

def generate_demand_data():
    """
    Generate realistic demand data for South Indian restaurant chain
    Returns DataFrame with columns: date, dish, outlet, predicted_demand
    """
    
    # Date range for 7 days (weekly forecast)
    start_date = datetime.now().date()
    date_range = [start_date + timedelta(days=i) for i in range(7)]
    
    # Base demand patterns for different dish categories
    dish_base_demand = {
        # Breakfast items (higher morning demand)
        "Idli": 120, "Dosa": 150, "Vada": 80, "Upma": 90, "Uttapam": 70,
        "Plain Dosa": 130, "Masala Dosa": 180, "Rava Dosa": 110, "Mysore Masala Dosa": 100,
        "Onion Dosa": 95, "Sambar Idli": 85, "Rava Idli": 75, "Mini Idli": 65, "Ghee Idli": 55,
        "Sambar Vada": 70, "Dahi Vada": 60, "Medu Vada": 85, "Masala Vada": 50,
        "Onion Uttapam": 65, "Tomato Uttapam": 60, "Mixed Veg Uttapam": 55, "Cheese Uttapam": 45,
        "Rava Upma": 80, "Vegetable Upma": 70, "Tomato Upma": 60, "Lemon Upma": 50,
        
        # Traditional items
        "Pongal": 95, "Ven Pongal": 85, "Khara Pongal": 75, "Sweet Pongal": 65, "Ghee Pongal": 55,
        
        # Rice dishes (lunch/dinner)
        "Sambar Rice": 140, "Rasam Rice": 120, "Curd Rice": 100, "Lemon Rice": 90, "Coconut Rice": 70,
        
        # Bread items
        "Poori": 85, "Chapati": 95, "Paratha": 75, "Aloo Paratha": 65, "Gobi Paratha": 55,
        
        # Beverages
        "Filter Coffee": 200, "South Indian Coffee": 150, "Masala Tea": 130, "Buttermilk": 110, "Fresh Lime": 90
    }
    
    # Outlet multipliers (different locations have different customer bases)
    outlet_multipliers = {
        "Madhapur": 1.3,      # Tech hub, higher demand
        "Jubilee Hills": 1.1,  # Premium area, moderate demand
        "Chennai Central": 1.2  # Business district, good demand
    }
    
    # Day of week patterns (1 = Monday, 7 = Sunday)
    day_multipliers = {
        0: 0.85,  # Monday - slower start
        1: 1.0,   # Tuesday - normal
        2: 1.05,  # Wednesday - mid-week pickup
        3: 1.1,   # Thursday - building up
        4: 1.15,  # Friday - week-end rush
        5: 1.3,   # Saturday - weekend high
        6: 1.25   # Sunday - family day
    }
    
    data = []
    
    for date in date_range:
        day_of_week = date.weekday()
        day_multiplier = day_multipliers.get(day_of_week, 1.0)
        
        for dish in SOUTH_INDIAN_DISHES:
            base_demand = dish_base_demand.get(dish, 80)  # Default base demand
            
            for outlet in OUTLETS:
                outlet_multiplier = outlet_multipliers.get(outlet, 1.0)
                
                # Calculate predicted demand with some randomness
                predicted_demand = base_demand * outlet_multiplier * day_multiplier
                
                # Add some realistic variance (±20%)
                variance = np.random.normal(0, 0.15)
                predicted_demand = predicted_demand * (1 + variance)
                
                # Ensure minimum demand and round to integer
                predicted_demand = max(int(predicted_demand), 10)
                
                data.append({
                    'date': date,
                    'dish': dish,
                    'outlet': outlet,
                    'predicted_demand': predicted_demand
                })
    
    df = pd.DataFrame(data)
    return df

# Additional utility functions for compatibility
def get_dishes():
    """Return list of available dishes"""
    return SOUTH_INDIAN_DISHES

def get_outlets():
    """Return list of available outlets"""
    return OUTLETS

if __name__ == "__main__":
    # Test data generation
    df = generate_demand_data()
    print(f"Generated {len(df)} records")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Dishes: {df['dish'].nunique()}")
    print(f"Outlets: {df['outlet'].nunique()}")
    print("\nSample data:")
    print(df.head()) 