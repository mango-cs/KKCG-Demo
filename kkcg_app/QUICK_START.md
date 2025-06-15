# 🚀 KKCG Analytics Dashboard - Quick Start Guide

Get your AI-powered restaurant analytics dashboard running in 3 minutes!

## ⚡ Quick Setup

### Option 1: Using the Launcher Script (Recommended)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the launcher (includes all checks)
python run_app.py
```

### Option 2: Direct Streamlit Command
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch directly
streamlit run Home.py
```

## 🌐 Access Your Dashboard

Once launched, your dashboard will be available at:
**http://localhost:8501**

## 🎯 First Steps

### 1. Home Page
- **Beautiful Landing**: View the main dashboard with tool navigation
- **Choose Your Tool**: Click either "Forecasting" or "Heatmap Analytics"

### 2. Try the Forecasting Tool 🔮
1. Click **"🔮 Launch Forecasting Tool"**
2. In the sidebar, select:
   - **Dish**: "Masala Dosa" (popular choice)
   - **Outlet**: "Chennai Central" (high traffic)
   - **Date Range**: Default 7-day forecast
   - **Weather**: "Rainy" (optional)
   - **Event**: "Festival" (optional)
3. Click **"🚀 Generate Forecast"**
4. View interactive charts and explanations!

### 3. Try the Heatmap Analytics 🔥
1. Click **"🔥 Launch Heatmap Analytics"** from home
2. Explore the **main heatmap** showing all dishes vs outlets
3. Use the **tabs** at the bottom:
   - **📈 Trends**: See demand over time
   - **🏢 Outlet Comparison**: Compare performance
   - **🍽️ Dish Analysis**: Top performers
   - **💡 Business Insights**: AI recommendations

## 🎨 Features to Explore

### Forecasting Tool Features
- **Interactive Charts**: Hover over data points for details
- **SHAP Explanations**: See why predictions were made
- **Confidence Intervals**: Understand prediction uncertainty
- **Export Options**: Download forecasts as CSV or JSON

### Heatmap Analytics Features
- **Color Scales**: Try different visualization modes
- **Filter Options**: Customize dish and outlet selections
- **Smart Alerts**: Get AI-powered business recommendations
- **Export Reports**: Download insights and data

## 🛠️ Customization Tips

### Change Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#Your_Color_Here"  # Default: #FF6B35 (saffron)
```

### Add Your Data
Replace the sample data in `utils/data_simulation.py`:
- Update `SOUTH_INDIAN_DISHES` list with your menu
- Modify `OUTLETS` list with your locations
- Connect to your API in `pages/Forecasting_Tool.py`

### Modify Styling
Update the CSS in each page file to match your brand:
- Colors, fonts, and spacing
- Logo and branding elements
- Layout and component styling

## 📱 Mobile Usage

The dashboard is fully responsive! Access it from:
- **Desktop**: Full feature experience
- **Tablet**: Optimized layout with touch controls  
- **Mobile**: Compact view with collapsible sidebar

## 🔧 Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install -r requirements.txt --upgrade
```

**Port Already in Use:**
```bash
streamlit run Home.py --server.port 8502
```

**Permission Errors:**
```bash
python -m streamlit run Home.py
```

**Module Not Found:**
Make sure you're in the `kkcg_app` directory:
```bash
ls -la  # Should see Home.py, pages/, utils/
```

### Performance Tips
- **Data Caching**: App uses `@st.cache_data` for speed
- **Browser Cache**: Refresh page if styling seems off
- **Memory Usage**: Restart app if it becomes slow

## 🎯 Business Use Cases

### Daily Operations
- **Morning Planning**: Generate today's demand forecast
- **Inventory Decisions**: Check which dishes need more prep
- **Staffing**: Plan workforce based on predicted busy periods

### Weekly Analysis  
- **Performance Review**: Use heatmap to see week's patterns
- **Menu Optimization**: Identify underperforming dishes
- **Outlet Comparison**: See which locations are performing best

### Strategic Planning
- **Trend Analysis**: Understand demand patterns over time
- **Growth Opportunities**: Find dishes to expand to other outlets
- **Risk Management**: Monitor consistency across locations

## 🔌 API Integration

To connect your real data:

1. **Update API endpoint** in `pages/Forecasting_Tool.py`:
   ```python
   API_BASE_URL = "http://your-api-server:8000"
   ```

2. **Replace sample data** in `utils/data_simulation.py` with API calls

3. **Add authentication** if needed for your data sources

## 🚀 Ready to Launch!

Your KKCG Analytics Dashboard is now ready to help optimize your restaurant operations with AI-powered insights!

### Need Help?
- Check the full **README.md** for detailed documentation
- Use browser developer tools to debug any issues
- Modify the code to fit your specific business needs

---

**🍛 Happy Analytics!**  
*Built with ❤️ for data-driven restaurant success* 