-- Restaurant Demand Forecasting Database Initialization Script
-- This script initializes the PostgreSQL database with TimescaleDB extension

-- Enable TimescaleDB extension (if available)
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Enable other useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create schema for time series data
CREATE SCHEMA IF NOT EXISTS timeseries;

-- Function to create hypertables for time series data
CREATE OR REPLACE FUNCTION create_hypertables() RETURNS void AS $$
BEGIN
    -- Convert sales_data to hypertable (if TimescaleDB is available)
    BEGIN
        PERFORM create_hypertable('sales_data', 'datetime', if_not_exists => TRUE);
        RAISE NOTICE 'Created hypertable for sales_data';
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'TimescaleDB not available or hypertable already exists for sales_data';
    END;
    
    -- Convert forecasts to hypertable
    BEGIN
        PERFORM create_hypertable('forecasts', 'forecast_date', if_not_exists => TRUE);
        RAISE NOTICE 'Created hypertable for forecasts';
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'TimescaleDB not available or hypertable already exists for forecasts';
    END;
    
    -- Convert model_performance to hypertable
    BEGIN
        PERFORM create_hypertable('model_performance', 'evaluation_date', if_not_exists => TRUE);
        RAISE NOTICE 'Created hypertable for model_performance';
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'TimescaleDB not available or hypertable already exists for model_performance';
    END;
END;
$$ LANGUAGE plpgsql;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sales_data_composite ON sales_data (datetime DESC, dish_name, outlet_id);
CREATE INDEX IF NOT EXISTS idx_forecasts_composite ON forecasts (forecast_date DESC, dish_name, outlet_id, model_name);
CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts (is_active, created_at DESC) WHERE is_active = true;

-- Create materialized views for common aggregations
CREATE MATERIALIZED VIEW IF NOT EXISTS daily_sales_summary AS
SELECT 
    DATE(datetime) as date,
    dish_name,
    outlet_id,
    SUM(quantity_sold) as total_quantity,
    SUM(revenue) as total_revenue,
    SUM(profit) as total_profit,
    COUNT(*) as transaction_count,
    AVG(price) as avg_price
FROM sales_data
GROUP BY DATE(datetime), dish_name, outlet_id;

-- Index for the materialized view
CREATE UNIQUE INDEX IF NOT EXISTS idx_daily_sales_summary ON daily_sales_summary (date, dish_name, outlet_id);

-- Refresh materialized view function
CREATE OR REPLACE FUNCTION refresh_daily_sales_summary() RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;
END;
$$ LANGUAGE plpgsql;

-- Insert initial outlet data
INSERT INTO outlets (outlet_id, name, location, city, state, size, foot_traffic, seating_capacity, staff_count, is_active) VALUES
('outlet_1', 'Chennai Central', 'Central Railway Station, Chennai', 'Chennai', 'Tamil Nadu', 'large', 'high', 150, 25, true),
('outlet_2', 'Bangalore Koramangala', 'Koramangala 5th Block, Bangalore', 'Bangalore', 'Karnataka', 'medium', 'medium', 80, 15, true),
('outlet_3', 'Hyderabad Banjara Hills', 'Banjara Hills, Hyderabad', 'Hyderabad', 'Telangana', 'large', 'high', 120, 20, true),
('outlet_4', 'Coimbatore RS Puram', 'RS Puram, Coimbatore', 'Coimbatore', 'Tamil Nadu', 'small', 'low', 50, 10, true),
('outlet_5', 'Kochi Marine Drive', 'Marine Drive, Kochi', 'Kochi', 'Kerala', 'medium', 'medium', 70, 12, true)
ON CONFLICT (outlet_id) DO NOTHING;

-- Insert initial dish data
INSERT INTO dishes (name, category, base_price, base_cost, description, is_vegetarian, is_vegan, spice_level, calories, preparation_time) VALUES
-- Rice dishes
('Sambar Rice', 'rice', 80, 25, 'Steamed rice with sambar', true, true, 'Medium', 320, 15),
('Rasam Rice', 'rice', 75, 22, 'Steamed rice with rasam', true, true, 'Medium', 300, 15),
('Curd Rice', 'rice', 70, 20, 'Rice with yogurt and tempering', true, false, 'Mild', 280, 10),
('Coconut Rice', 'rice', 85, 28, 'Rice with coconut and spices', true, true, 'Mild', 350, 20),

-- Dosa varieties
('Plain Dosa', 'dosa', 60, 18, 'Crispy fermented crepe', true, true, 'Mild', 200, 10),
('Masala Dosa', 'dosa', 80, 25, 'Dosa with spiced potato filling', true, true, 'Medium', 300, 15),
('Onion Dosa', 'dosa', 70, 22, 'Dosa with onion topping', true, true, 'Mild', 220, 12),
('Ghee Dosa', 'dosa', 90, 30, 'Dosa cooked in ghee', true, false, 'Mild', 350, 15),
('Paper Dosa', 'dosa', 100, 35, 'Large thin crispy dosa', true, true, 'Mild', 250, 20),

-- Idli varieties
('Idli', 'idli', 40, 12, 'Steamed rice cakes', true, true, 'Mild', 150, 15),
('Button Idli', 'idli', 50, 15, 'Small round idlis', true, true, 'Mild', 120, 15),
('Rava Idli', 'idli', 55, 18, 'Semolina steamed cakes', true, false, 'Mild', 180, 20),

-- Vada varieties
('Medu Vada', 'vada', 45, 15, 'Deep fried lentil donuts', true, true, 'Medium', 180, 15),
('Masala Vada', 'vada', 50, 18, 'Spiced lentil fritters', true, true, 'Hot', 200, 20),
('Dahi Vada', 'vada', 60, 20, 'Vada in yogurt sauce', true, false, 'Mild', 220, 25),

-- Sambar and Rasam
('Sambar', 'sambar_rasam', 30, 10, 'Lentil curry with vegetables', true, true, 'Medium', 100, 30),
('Rasam', 'sambar_rasam', 25, 8, 'Tangy tomato soup', true, true, 'Hot', 80, 25),
('Tomato Rasam', 'sambar_rasam', 30, 10, 'Tomato based rasam', true, true, 'Medium', 90, 25),
('Pepper Rasam', 'sambar_rasam', 35, 12, 'Spicy pepper rasam', true, true, 'Hot', 85, 20),

-- Snacks
('Bajji', 'snacks', 40, 12, 'Vegetable fritters', true, true, 'Medium', 160, 15),
('Bonda', 'snacks', 35, 10, 'Spiced potato balls', true, true, 'Medium', 140, 15),
('Murukku', 'snacks', 25, 8, 'Crispy spiral snacks', true, true, 'Mild', 120, 30),
('Mixture', 'snacks', 30, 10, 'Crunchy snack mix', true, true, 'Medium', 150, 45),

-- Sweets
('Payasam', 'sweets', 60, 20, 'Sweet rice pudding', true, false, 'Mild', 250, 45),
('Halwa', 'sweets', 70, 25, 'Sweet semolina dessert', true, false, 'Mild', 300, 30),
('Laddu', 'sweets', 50, 18, 'Sweet gram flour balls', true, false, 'Mild', 220, 60),
('Mysore Pak', 'sweets', 80, 30, 'Rich sweet with ghee', true, false, 'Mild', 350, 45),

-- Beverages
('Filter Coffee', 'beverages', 30, 8, 'Traditional South Indian coffee', true, false, 'Mild', 50, 5),
('Tea', 'beverages', 20, 5, 'Spiced Indian tea', true, false, 'Mild', 40, 5),
('Buttermilk', 'beverages', 25, 7, 'Spiced yogurt drink', true, false, 'Mild', 60, 5),
('Lassi', 'beverages', 40, 12, 'Sweet yogurt drink', true, false, 'Mild', 150, 5),

-- Curries
('Kootu', 'curries', 50, 15, 'Vegetable and lentil curry', true, true, 'Medium', 120, 25),
('Poriyal', 'curries', 45, 12, 'Dry vegetable curry', true, true, 'Medium', 100, 20),
('Aviyal', 'curries', 55, 18, 'Mixed vegetable curry', true, true, 'Medium', 140, 30),
('Keerai', 'curries', 40, 10, 'Spinach curry', true, true, 'Medium', 80, 20),

-- Breads
('Parotta', 'breads', 25, 8, 'Layered flatbread', true, false, 'Mild', 200, 20),
('Chapati', 'breads', 15, 5, 'Whole wheat flatbread', true, true, 'Mild', 120, 15),
('Appam', 'breads', 35, 12, 'Fermented rice pancake', true, true, 'Mild', 150, 15),
('Uttapam', 'breads', 65, 20, 'Thick pancake with toppings', true, true, 'Medium', 250, 15)
ON CONFLICT (name) DO NOTHING;

-- Insert initial events/festivals
INSERT INTO events (event_name, event_type, start_date, end_date, description, expected_impact, is_national, is_regional) VALUES
('Pongal', 'festival', '2024-01-15', '2024-01-15', 'Tamil harvest festival', 1.5, false, true),
('Republic Day', 'holiday', '2024-01-26', '2024-01-26', 'National holiday', 1.3, true, false),
('Holi', 'festival', '2024-03-08', '2024-03-08', 'Festival of colors', 1.4, true, false),
('Tamil New Year', 'festival', '2024-04-14', '2024-04-14', 'Tamil New Year celebration', 1.6, false, true),
('Independence Day', 'holiday', '2024-08-15', '2024-08-15', 'National holiday', 1.3, true, false),
('Ganesh Chaturthi', 'festival', '2024-09-07', '2024-09-07', 'Lord Ganesha festival', 1.4, true, false),
('Diwali', 'festival', '2024-10-31', '2024-10-31', 'Festival of lights', 1.7, true, false),
('Christmas', 'holiday', '2024-12-25', '2024-12-25', 'Christmas celebration', 1.2, true, false)
ON CONFLICT (event_name) DO NOTHING;

-- Create default admin user (password: admin123)
INSERT INTO users (username, email, hashed_password, full_name, role, is_active, is_verified) VALUES
('admin', 'admin@restaurant.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LegK5/VwYGb2bPpuW', 'Administrator', 'admin', true, true),
('manager', 'manager@restaurant.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LegK5/VwYGb2bPpuW', 'Restaurant Manager', 'manager', true, true),
('analyst', 'analyst@restaurant.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LegK5/VwYGb2bPpuW', 'Data Analyst', 'analyst', true, true)
ON CONFLICT (username) DO NOTHING;

-- Create function to calculate time-based features
CREATE OR REPLACE FUNCTION extract_time_features(input_datetime TIMESTAMP)
RETURNS TABLE (
    hour_of_day INTEGER,
    day_of_week INTEGER,
    day_of_month INTEGER,
    month_of_year INTEGER,
    is_weekend BOOLEAN,
    is_lunch_time BOOLEAN,
    is_dinner_time BOOLEAN,
    is_business_hours BOOLEAN
) AS $$
BEGIN
    RETURN QUERY SELECT
        EXTRACT(HOUR FROM input_datetime)::INTEGER,
        EXTRACT(DOW FROM input_datetime)::INTEGER,
        EXTRACT(DAY FROM input_datetime)::INTEGER,
        EXTRACT(MONTH FROM input_datetime)::INTEGER,
        EXTRACT(DOW FROM input_datetime) IN (0, 6),
        EXTRACT(HOUR FROM input_datetime) BETWEEN 12 AND 14,
        EXTRACT(HOUR FROM input_datetime) BETWEEN 19 AND 21,
        EXTRACT(HOUR FROM input_datetime) BETWEEN 6 AND 23;
END;
$$ LANGUAGE plpgsql;

-- Create aggregation function for demand metrics
CREATE OR REPLACE FUNCTION calculate_demand_metrics(
    p_dish_name TEXT,
    p_outlet_id TEXT,
    p_start_date DATE,
    p_end_date DATE
)
RETURNS TABLE (
    avg_daily_demand NUMERIC,
    max_daily_demand NUMERIC,
    min_daily_demand NUMERIC,
    total_demand NUMERIC,
    demand_volatility NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    WITH daily_demand AS (
        SELECT DATE(datetime) as date, SUM(quantity_sold) as daily_qty
        FROM sales_data
        WHERE dish_name = p_dish_name 
          AND outlet_id = p_outlet_id
          AND DATE(datetime) BETWEEN p_start_date AND p_end_date
        GROUP BY DATE(datetime)
    )
    SELECT 
        AVG(daily_qty)::NUMERIC,
        MAX(daily_qty)::NUMERIC,
        MIN(daily_qty)::NUMERIC,
        SUM(daily_qty)::NUMERIC,
        STDDEV(daily_qty)::NUMERIC
    FROM daily_demand;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to update revenue and profit automatically
CREATE OR REPLACE FUNCTION update_sales_calculations()
RETURNS TRIGGER AS $$
BEGIN
    NEW.revenue = NEW.price * NEW.quantity_sold;
    NEW.profit = NEW.revenue - (NEW.cost * NEW.quantity_sold);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_sales_calculations
    BEFORE INSERT OR UPDATE ON sales_data
    FOR EACH ROW
    EXECUTE FUNCTION update_sales_calculations();

-- Create function to check inventory alerts
CREATE OR REPLACE FUNCTION check_inventory_alerts()
RETURNS void AS $$
DECLARE
    inventory_record RECORD;
BEGIN
    FOR inventory_record IN 
        SELECT * FROM inventory WHERE current_stock <= reorder_point
    LOOP
        INSERT INTO alerts (
            alert_type, severity, outlet_id, message, description,
            current_value, threshold_value, recommended_action
        ) VALUES (
            'inventory_low',
            CASE 
                WHEN inventory_record.current_stock <= inventory_record.minimum_stock THEN 'critical'
                WHEN inventory_record.current_stock <= inventory_record.reorder_point * 0.5 THEN 'high'
                ELSE 'medium'
            END,
            inventory_record.outlet_id,
            format('Low inventory: %s at %s', inventory_record.ingredient_name, inventory_record.outlet_id),
            format('Current stock: %s %s, Minimum required: %s %s', 
                   inventory_record.current_stock, inventory_record.unit,
                   inventory_record.minimum_stock, inventory_record.unit),
            inventory_record.current_stock,
            inventory_record.reorder_point,
            format('Reorder %s %s immediately', 
                   (inventory_record.maximum_stock - inventory_record.current_stock), 
                   inventory_record.unit)
        )
        ON CONFLICT DO NOTHING;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Call the function to create hypertables (if TimescaleDB is available)
SELECT create_hypertables();

-- Create indexes after all tables are created
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sales_data_datetime_desc ON sales_data (datetime DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_forecasts_date_desc ON forecasts (forecast_date DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_model_performance_date ON model_performance (evaluation_date DESC);

-- Set up row-level security (optional)
-- ALTER TABLE sales_data ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE forecasts ENABLE ROW LEVEL SECURITY;

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Display initialization status
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Database initialization completed!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Created tables: %', (SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public');
    RAISE NOTICE 'Created outlets: %', (SELECT count(*) FROM outlets);
    RAISE NOTICE 'Created dishes: %', (SELECT count(*) FROM dishes);
    RAISE NOTICE 'Created events: %', (SELECT count(*) FROM events);
    RAISE NOTICE 'Created users: %', (SELECT count(*) FROM users);
    RAISE NOTICE '========================================';
END $$; 