import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# South Indian dish names for authenticity
SOUTH_INDIAN_DISHES = [
    "Masala Dosa", "Plain Dosa", "Rava Dosa", "Ghee Roast", "Set Dosa",
    "Idli", "Vada", "Sambar Vada", "Ragi Mudde", "Bisi Bele Bath",
    "Puliyogare", "Curd Rice", "Coconut Rice", "Tomato Rice", "Lemon Rice",
    "Paneer Biryani", "Veg Biryani", "Chicken Biryani", "Mutton Biryani", "Fish Curry",
    "Rasam", "Sambar", "Dal Tadka", "Palak Dal", "Chole",
    "Aloo Gobi", "Bhindi Masala", "Paneer Butter Masala", "Kadai Paneer", "Palak Paneer",
    "Chapati", "Naan", "Butter Naan", "Garlic Naan", "Paratha",
    "Uttapam", "Rava Uttapam", "Onion Uttapam", "Tomato Uttapam", "Mixed Veg Uttapam"
]

OUTLETS = ["Madhapur", "Jubilee Hills", "Chennai Central"]

def generate_demand_data():
    """
    Generate demand forecasts for 40 dishes × 3 outlets × 7 days
    Returns a Pandas DataFrame with columns: dish, outlet, predicted_demand, date
    """
    np.random.seed(42)  # For reproducible results
    random.seed(42)
    
    # Generate date range for 7 days starting from today
    start_date = datetime.now().date()
    dates = [start_date + timedelta(days=i) for i in range(7)]
    
    data = []
    
    # Generate data for each combination
    for dish in SOUTH_INDIAN_DISHES:
        for outlet in OUTLETS:
            # Create outlet-specific demand patterns
            base_demand = random.randint(100, 300)
            
            # Add outlet-specific modifiers
            if outlet == "Jubilee Hills":
                # Premium location - higher demand
                modifier = 1.2
            elif outlet == "Chennai Central":
                # Busy location - variable demand
                modifier = 1.1
            else:  # Madhapur
                # Regular demand
                modifier = 1.0
            
            # Add dish-specific popularity
            if dish in ["Masala Dosa", "Chicken Biryani", "Paneer Biryani", "Idli"]:
                dish_modifier = 1.3  # Popular dishes
            elif dish in ["Ragi Mudde", "Fish Curry", "Mutton Biryani"]:
                dish_modifier = 0.8  # Less popular
            else:
                dish_modifier = 1.0
            
            for date in dates:
                # Add daily variation
                daily_variation = np.random.uniform(0.8, 1.2)
                
                # Weekend boost (Saturday/Sunday)
                weekend_boost = 1.2 if date.weekday() >= 5 else 1.0
                
                final_demand = int(base_demand * modifier * dish_modifier * daily_variation * weekend_boost)
                
                # Ensure minimum demand of 80 and maximum of 400
                final_demand = max(80, min(400, final_demand))
                
                data.append({
                    'dish': dish,
                    'outlet': outlet,
                    'predicted_demand': final_demand,
                    'date': date
                })
    
    df = pd.DataFrame(data)
    return df

def get_sample_data():
    """
    Convenience function to get sample data
    """
    return generate_demand_data()

if __name__ == "__main__":
    # Test the data generation
    df = generate_demand_data()
    print(f"Generated {len(df)} records")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Dishes: {df['dish'].nunique()}")
    print(f"Outlets: {df['outlet'].nunique()}")
    print("\nSample data:")
    print(df.head(10)) 