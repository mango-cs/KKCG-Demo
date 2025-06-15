"""
Restaurant Demand Forecasting - Data Simulation
Generates realistic sales data for 40 South Indian dishes across 5 outlets for 90 days
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import os
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from app.core.config import settings
from app.core.database import SessionLocal, init_db
from app.db.models import SalesData, Dish, Outlet, Event

class RestaurantDataSimulator:
    """Simulates realistic restaurant sales data with patterns and seasonality"""
    
    def __init__(self):
        self.start_date = datetime.strptime(settings.SIMULATION_START_DATE, "%Y-%m-%d")
        self.days = settings.SIMULATION_DAYS
        self.outlets = list(settings.OUTLETS.keys())
        
        # South Indian dishes with categories and base popularity
        self.dishes = {
            # Rice dishes (High volume, especially lunch)
            "Sambar Rice": {"category": "rice", "base_demand": 25, "peak_hours": [12, 13, 19, 20], "price": 80, "cost": 25},
            "Rasam Rice": {"category": "rice", "base_demand": 20, "peak_hours": [12, 13, 19, 20], "price": 75, "cost": 22},
            "Curd Rice": {"category": "rice", "base_demand": 15, "peak_hours": [13, 14, 20, 21], "price": 70, "cost": 20},
            "Coconut Rice": {"category": "rice", "base_demand": 12, "peak_hours": [12, 13], "price": 85, "cost": 28},
            
            # Dosa varieties (Popular breakfast and dinner)
            "Plain Dosa": {"category": "dosa", "base_demand": 30, "peak_hours": [7, 8, 9, 19, 20], "price": 60, "cost": 18},
            "Masala Dosa": {"category": "dosa", "base_demand": 35, "peak_hours": [7, 8, 9, 19, 20], "price": 80, "cost": 25},
            "Onion Dosa": {"category": "dosa", "base_demand": 20, "peak_hours": [7, 8, 19, 20], "price": 70, "cost": 22},
            "Ghee Dosa": {"category": "dosa", "base_demand": 15, "peak_hours": [8, 9, 20], "price": 90, "cost": 30},
            "Paper Dosa": {"category": "dosa", "base_demand": 18, "peak_hours": [8, 9, 20], "price": 100, "cost": 35},
            
            # Idli varieties (Breakfast favorite)
            "Idli": {"category": "idli", "base_demand": 40, "peak_hours": [7, 8, 9], "price": 40, "cost": 12},
            "Button Idli": {"category": "idli", "base_demand": 25, "peak_hours": [7, 8, 9], "price": 50, "cost": 15},
            "Rava Idli": {"category": "idli", "base_demand": 20, "peak_hours": [8, 9], "price": 55, "cost": 18},
            
            # Vada varieties (Breakfast and evening snack)
            "Medu Vada": {"category": "vada", "base_demand": 30, "peak_hours": [7, 8, 16, 17], "price": 45, "cost": 15},
            "Masala Vada": {"category": "vada", "base_demand": 15, "peak_hours": [8, 16, 17], "price": 50, "cost": 18},
            "Dahi Vada": {"category": "vada", "base_demand": 12, "peak_hours": [13, 14, 17], "price": 60, "cost": 20},
            
            # Sambar and Rasam (Side dishes)
            "Sambar": {"category": "sides", "base_demand": 45, "peak_hours": [7, 8, 12, 13, 19, 20], "price": 30, "cost": 10},
            "Rasam": {"category": "sides", "base_demand": 35, "peak_hours": [12, 13, 19, 20], "price": 25, "cost": 8},
            "Tomato Rasam": {"category": "sides", "base_demand": 25, "peak_hours": [12, 13, 19, 20], "price": 30, "cost": 10},
            "Pepper Rasam": {"category": "sides", "base_demand": 20, "peak_hours": [13, 20], "price": 35, "cost": 12},
            
            # Snacks (Evening time)
            "Bajji": {"category": "snacks", "base_demand": 20, "peak_hours": [16, 17, 18], "price": 40, "cost": 12},
            "Bonda": {"category": "snacks", "base_demand": 18, "peak_hours": [16, 17, 18], "price": 35, "cost": 10},
            "Murukku": {"category": "snacks", "base_demand": 15, "peak_hours": [16, 17], "price": 25, "cost": 8},
            "Mixture": {"category": "snacks", "base_demand": 12, "peak_hours": [16, 17], "price": 30, "cost": 10},
            
            # Sweets (Special occasions and weekends)
            "Payasam": {"category": "sweets", "base_demand": 8, "peak_hours": [14, 20, 21], "price": 60, "cost": 20},
            "Halwa": {"category": "sweets", "base_demand": 10, "peak_hours": [14, 20, 21], "price": 70, "cost": 25},
            "Laddu": {"category": "sweets", "base_demand": 12, "peak_hours": [14, 20], "price": 50, "cost": 18},
            "Mysore Pak": {"category": "sweets", "base_demand": 6, "peak_hours": [14, 21], "price": 80, "cost": 30},
            
            # Beverages (All day but peaks with meals)
            "Filter Coffee": {"category": "beverages", "base_demand": 50, "peak_hours": [7, 8, 16, 17, 20], "price": 30, "cost": 8},
            "Tea": {"category": "beverages", "base_demand": 40, "peak_hours": [7, 8, 16, 17], "price": 20, "cost": 5},
            "Buttermilk": {"category": "beverages", "base_demand": 25, "peak_hours": [13, 14, 20], "price": 25, "cost": 7},
            "Lassi": {"category": "beverages", "base_demand": 15, "peak_hours": [14, 17, 20], "price": 40, "cost": 12},
            
            # Curries (Lunch and dinner)
            "Kootu": {"category": "curries", "base_demand": 20, "peak_hours": [12, 13, 19, 20], "price": 50, "cost": 15},
            "Poriyal": {"category": "curries", "base_demand": 18, "peak_hours": [12, 13, 19, 20], "price": 45, "cost": 12},
            "Aviyal": {"category": "curries", "base_demand": 15, "peak_hours": [12, 13, 19], "price": 55, "cost": 18},
            "Keerai": {"category": "curries", "base_demand": 12, "peak_hours": [12, 13], "price": 40, "cost": 10},
            
            # Breads (Dinner mainly)
            "Parotta": {"category": "breads", "base_demand": 25, "peak_hours": [19, 20, 21], "price": 25, "cost": 8},
            "Chapati": {"category": "breads", "base_demand": 20, "peak_hours": [19, 20], "price": 15, "cost": 5},
            "Appam": {"category": "breads", "base_demand": 18, "peak_hours": [8, 19, 20], "price": 35, "cost": 12},
            "Uttapam": {"category": "breads", "base_demand": 22, "peak_hours": [8, 9, 19, 20], "price": 65, "cost": 20},
        }
        
        # Outlet characteristics
        self.outlet_multipliers = {
            "outlet_1": 1.3,  # Chennai Central - High traffic
            "outlet_2": 1.0,  # Bangalore Koramangala - Medium
            "outlet_3": 1.2,  # Hyderabad Banjara Hills - High
            "outlet_4": 0.7,  # Coimbatore RS Puram - Low
            "outlet_5": 0.9   # Kochi Marine Drive - Medium
        }
        
        # Weather patterns
        self.weather_patterns = {
            "sunny": 1.1,
            "cloudy": 1.0,
            "rainy": 0.7,
            "hot": 1.2
        }
        
        # Festival/Event impacts
        self.festivals = {
            "2024-01-15": {"name": "Pongal", "impact": 1.6},
            "2024-01-26": {"name": "Republic Day", "impact": 1.3},
            "2024-03-08": {"name": "Holi", "impact": 1.4},
            "2024-04-14": {"name": "Tamil New Year", "impact": 1.7},
            "2024-08-15": {"name": "Independence Day", "impact": 1.3},
            "2024-09-07": {"name": "Ganesh Chaturthi", "impact": 1.5},
            "2024-10-31": {"name": "Diwali", "impact": 1.8},
            "2024-12-25": {"name": "Christmas", "impact": 1.2}
        }
    
    def get_hour_multiplier(self, hour, dish_name):
        """Get demand multiplier based on hour and dish type"""
        dish_info = self.dishes[dish_name]
        peak_hours = dish_info["peak_hours"]
        
        if hour in peak_hours:
            return 1.8  # Peak hour boost
        elif hour in [h+1 for h in peak_hours] or hour in [h-1 for h in peak_hours]:
            return 1.3  # Near peak
        elif 6 <= hour <= 23:  # Business hours
            return 1.0
        else:
            return 0.1  # Off hours
    
    def get_day_multiplier(self, date):
        """Get demand multiplier based on day of week"""
        day_of_week = date.weekday()
        
        if day_of_week == 6:  # Sunday
            return 1.4
        elif day_of_week == 5:  # Saturday
            return 1.2
        elif day_of_week in [0, 1, 2, 3, 4]:  # Weekdays
            return 1.0
        else:
            return 1.0
    
    def get_weather(self, date):
        """Simulate weather based on month and randomness"""
        month = date.month
        
        # Monsoon months (June-September)
        if month in [6, 7, 8, 9]:
            return random.choices(
                ["rainy", "cloudy", "sunny"],
                weights=[0.6, 0.3, 0.1]
            )[0]
        # Summer months (March-May)
        elif month in [3, 4, 5]:
            return random.choices(
                ["hot", "sunny", "cloudy"],
                weights=[0.5, 0.4, 0.1]
            )[0]
        # Winter months
        else:
            return random.choices(
                ["sunny", "cloudy", "rainy"],
                weights=[0.6, 0.3, 0.1]
            )[0]
    
    def get_event_impact(self, date):
        """Get event impact for a specific date"""
        date_str = date.strftime("%Y-%m-%d")
        if date_str in self.festivals:
            return self.festivals[date_str]["impact"], self.festivals[date_str]["name"]
        return 1.0, None
    
    def generate_promotions(self, date, dish_name):
        """Randomly generate promotions"""
        # Weekend promotions more likely
        if date.weekday() in [5, 6]:
            if random.random() < 0.15:  # 15% chance on weekends
                return True, random.uniform(0.8, 0.9)  # 10-20% discount
        else:
            if random.random() < 0.05:  # 5% chance on weekdays
                return True, random.uniform(0.85, 0.95)  # 5-15% discount
        
        return False, 1.0
    
    def calculate_demand(self, date, hour, dish_name, outlet_id):
        """Calculate demand for a specific dish at a specific time"""
        dish_info = self.dishes[dish_name]
        base_demand = dish_info["base_demand"]
        
        # Apply various multipliers
        hour_mult = self.get_hour_multiplier(hour, dish_name)
        day_mult = self.get_day_multiplier(date)
        outlet_mult = self.outlet_multipliers[outlet_id]
        
        # Weather impact
        weather = self.get_weather(date)
        weather_mult = self.weather_patterns[weather]
        
        # Event impact
        event_mult, event_name = self.get_event_impact(date)
        
        # Promotion impact
        has_promotion, promotion_mult = self.generate_promotions(date, dish_name)
        
        # Calculate base quantity
        quantity = base_demand * hour_mult * day_mult * outlet_mult * weather_mult * event_mult
        
        # Add promotion boost (more demand due to lower price)
        if has_promotion:
            quantity *= 1.3  # 30% more demand due to promotion
        
        # Add random noise
        noise = random.uniform(0.7, 1.3)
        quantity *= noise
        
        # Ensure minimum of 0
        quantity = max(0, int(round(quantity)))
        
        # Calculate price (with promotion discount)
        price = dish_info["price"] * promotion_mult
        cost = dish_info["cost"]
        
        return {
            "quantity": quantity,
            "price": price,
            "cost": cost,
            "weather": weather,
            "event": event_name,
            "promotion_flag": has_promotion
        }
    
    def generate_sales_data(self):
        """Generate complete sales dataset"""
        sales_data = []
        
        print(f"Generating sales data from {self.start_date} for {self.days} days...")
        print(f"Dishes: {len(self.dishes)}")
        print(f"Outlets: {len(self.outlets)}")
        
        for day in range(self.days):
            current_date = self.start_date + timedelta(days=day)
            print(f"Generating day {day + 1}/{self.days}: {current_date.strftime('%Y-%m-%d')}")
            
            for hour in range(6, 24):  # Business hours 6 AM to 11 PM
                for outlet_id in self.outlets:
                    for dish_name in self.dishes:
                        
                        # Calculate demand
                        demand_data = self.calculate_demand(current_date, hour, dish_name, outlet_id)
                        
                        # Only add if there's demand
                        if demand_data["quantity"] > 0:
                            record = {
                                "datetime": current_date.replace(hour=hour),
                                "dish_name": dish_name,
                                "outlet_id": outlet_id,
                                "quantity_sold": demand_data["quantity"],
                                "price": round(demand_data["price"], 2),
                                "cost": round(demand_data["cost"], 2),
                                "weather": demand_data["weather"],
                                "event": demand_data["event"],
                                "promotion_flag": demand_data["promotion_flag"]
                            }
                            sales_data.append(record)
        
        print(f"Generated {len(sales_data)} sales records")
        return sales_data
    
    def save_to_database(self, sales_data):
        """Save generated data to PostgreSQL database"""
        print("Connecting to database...")
        
        # Initialize database
        init_db()
        db = SessionLocal()
        
        try:
            print("Clearing existing sales data...")
            db.query(SalesData).delete()
            db.commit()
            
            print("Inserting new sales data...")
            batch_size = 1000
            
            for i in range(0, len(sales_data), batch_size):
                batch = sales_data[i:i + batch_size]
                
                for record in batch:
                    sales_record = SalesData(**record)
                    db.add(sales_record)
                
                db.commit()
                print(f"Inserted batch {i//batch_size + 1}/{(len(sales_data) + batch_size - 1)//batch_size}")
            
            print(f"✅ Successfully inserted {len(sales_data)} sales records")
            
            # Generate summary statistics
            total_revenue = sum(r["price"] * r["quantity_sold"] for r in sales_data)
            total_quantity = sum(r["quantity_sold"] for r in sales_data)
            
            print(f"\n📊 Data Summary:")
            print(f"Total Records: {len(sales_data):,}")
            print(f"Total Quantity Sold: {total_quantity:,}")
            print(f"Total Revenue: ₹{total_revenue:,.2f}")
            print(f"Average Order Value: ₹{total_revenue/len(sales_data):.2f}")
            
        except Exception as e:
            print(f"❌ Error saving to database: {e}")
            db.rollback()
            raise
        finally:
            db.close()
    
    def save_to_csv(self, sales_data, filename="sales_data.csv"):
        """Save data to CSV file for backup"""
        df = pd.DataFrame(sales_data)
        
        # Create data directory if it doesn't exist
        data_dir = Path(__file__).parent.parent.parent / "data" / "raw"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = data_dir / filename
        df.to_csv(filepath, index=False)
        print(f"💾 Data saved to {filepath}")
        
        return filepath

def main():
    """Main function to generate and save restaurant sales data"""
    print("🍛 Restaurant Demand Forecasting - Data Generation")
    print("=" * 60)
    
    simulator = RestaurantDataSimulator()
    
    try:
        # Generate sales data
        sales_data = simulator.generate_sales_data()
        
        # Save to CSV
        csv_path = simulator.save_to_csv(sales_data)
        
        # Save to database
        simulator.save_to_database(sales_data)
        
        print("\n✅ Data generation completed successfully!")
        print(f"📁 CSV file: {csv_path}")
        print("💾 Database: Updated with fresh data")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Data generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 