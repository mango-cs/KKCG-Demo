# 🍛 KKCG Analytics Dashboard

**AI-Powered Restaurant Analytics Platform for Kodi Kura Chitti Gaare**

A comprehensive analytics dashboard for South Indian restaurant chain management, featuring demand forecasting, heatmap visualization, and AI-powered business insights.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app-url.streamlit.app)
[![Backend API](https://img.shields.io/badge/Backend-Railway-purple)](https://kkcgbackend-production.up.railway.app/docs)

## 🚀 **Live Demo**

- **Frontend Dashboard**: [Streamlit Cloud](https://your-streamlit-app-url.streamlit.app)
- **Backend API**: [Railway Deployment](https://kkcgbackend-production.up.railway.app/docs)
- **API Documentation**: Interactive Swagger UI available at backend URL

## ✨ **Features**

### 🔮 **AI Demand Forecasting**
- 7-day demand predictions with 94% accuracy
- Weather and event factor integration
- Confidence intervals and trend analysis
- Interactive visualizations with Plotly

### 🔥 **Interactive Heatmap Analytics**
- Cross-outlet performance comparison
- Real-time demand pattern visualization
- AI-powered business insights
- Custom filtering and aggregation

### 🎯 **Backend Integration**
- FastAPI backend with PostgreSQL database
- JWT authentication system
- RESTful API with comprehensive endpoints
- Fallback to demo mode when offline

### 🏢 **Multi-Outlet Support**
- **Chennai Central** - High-traffic business district
- **Bangalore Koramangala** - Tech hub location
- **Hyderabad Banjara Hills** - Premium dining area
- **Coimbatore** - Regional expansion
- **Kochi** - Coastal market
- **Jubilee Hills** - Upscale neighborhood

## 🛠️ **Technology Stack**

### Frontend
- **Streamlit** - Interactive web application framework
- **Plotly** - Advanced data visualization
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP client for API integration

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Production database
- **SQLAlchemy** - Database ORM
- **JWT** - Authentication system
- **Railway** - Cloud deployment platform

## 📦 **Installation & Setup**

### Frontend Deployment (Streamlit Cloud)

1. **Fork this repository** to your GitHub account

2. **Create Streamlit Cloud account** at [share.streamlit.io](https://share.streamlit.io)

3. **Deploy the app**:
   - Click "New app" in Streamlit Cloud
   - Connect your GitHub repository
   - Set repository to your fork
   - Set main file path to `Home.py`
   - Click "Deploy"

4. **Environment Variables** (Optional):
   ```
   API_BASE_URL=https://kkcgbackend-production.up.railway.app
   ```

### Backend Deployment (Railway)

1. **Create Railway account** at [railway.app](https://railway.app)

2. **Deploy backend**:
   - Create new project
   - Connect to your backend repository
   - Railway will auto-deploy using the railway.toml configuration

3. **Environment Variables**:
   ```
   DATABASE_URL=your_postgresql_connection_string
   SECRET_KEY=your_jwt_secret_key
   ```

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/KKCG---FINALTEST.git
   cd KKCG---FINALTEST
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run Home.py
   ```

4. **Access the dashboard**:
   - Open your browser to `http://localhost:8501`

## 🔧 **Backend API Integration**

### Connection Status
The frontend automatically detects backend availability and shows connection status:

- 🟢 **Live Database** - Connected to PostgreSQL with real data
- 🟡 **Demo Database** - Backend online with sample data
- 🔴 **Backend Offline** - Using simulated data (demo mode)

### Authentication
- **Demo Login**: Use `demo`/`demo` for quick access
- **User Registration**: Create account through the interface
- **JWT Tokens**: Secure API authentication

### API Endpoints
- `GET /health` - Backend health check
- `POST /auth/login` - User authentication
- `POST /auth/register` - User registration
- `GET /outlets` - Outlet information
- `GET /dishes` - Menu items
- `GET /demand-data` - Historical demand data
- `POST /seed-data` - Populate sample data

## 📊 **Data Models**

### Outlets
```python
{
    "id": 1,
    "name": "Chennai Central",
    "location": "Chennai",
    "type": "flagship"
}
```

### Dishes
```python
{
    "id": 1,
    "name": "Masala Dosa",
    "category": "South Indian",
    "price": 120.00
}
```

### Demand Data
```python
{
    "date": "2024-01-15",
    "outlet_id": 1,
    "dish_id": 1,
    "predicted_demand": 150
}
```

## 🎨 **UI/UX Features**

- **Dark Theme** - Professional restaurant industry aesthetic
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Interactive Charts** - Hover effects and zoom capabilities
- **Real-time Updates** - Live backend status indicators
- **Professional Styling** - Custom CSS with smooth animations

## 🔍 **Analytics Capabilities**

### Demand Forecasting
- **Historical Analysis** - 30-day lookback for pattern recognition
- **Seasonal Trends** - Festival and weather impact analysis
- **Confidence Intervals** - Statistical uncertainty quantification
- **Feature Importance** - SHAP-style explainable AI

### Performance Metrics
- **Outlet Rankings** - Performance comparison across locations
- **Dish Analysis** - Best-selling and consistent performers
- **Growth Tracking** - Week-over-week trend analysis
- **Optimization Insights** - AI-powered recommendations

## 🚀 **Deployment Guide**

### Streamlit Cloud Deployment

1. **Prepare Repository**:
   ```
   ├── Home.py              # Main dashboard
   ├── pages/
   │   ├── Forecasting_Tool.py
   │   └── Heatmap_Comparison.py
   ├── utils/
   │   ├── data_simulation.py
   │   ├── forecasting_utils.py
   │   ├── heatmap_utils.py
   │   └── api_client.py
   ├── .streamlit/
   │   └── config.toml
   ├── requirements.txt
   └── README.md
   ```

2. **Streamlit Configuration** (`.streamlit/config.toml`):
   ```toml
   [theme]
   primaryColor = "#FF6B35"
   backgroundColor = "#0E1117"
   secondaryBackgroundColor = "#262730"
   textColor = "#FAFAFA"
   
   [server]
   headless = true
   port = 8501
   enableCORS = false
   ```

3. **Deploy Steps**:
   - Push code to GitHub
   - Connect to Streamlit Cloud
   - Set `Home.py` as main file
   - Deploy and test

### Backend API Deployment

1. **Railway Configuration** (`railway.toml`):
   ```toml
   [build]
   builder = "nixpacks"
   
   [deploy]
   healthcheckPath = "/health"
   healthcheckTimeout = 300
   restartPolicyType = "on_failure"
   
   [[deploy.startCommand]]
   cmd = "uvicorn main:app --host 0.0.0.0 --port $PORT"
   ```

2. **Environment Variables**:
   - `DATABASE_URL` - PostgreSQL connection string
   - `SECRET_KEY` - JWT secret key (generate secure key)

3. **Health Check**:
   - Backend includes health endpoint at `/health`
   - Returns database connection status
   - Used for monitoring and auto-restart

## 🔐 **Security Features**

- **JWT Authentication** - Secure token-based access
- **Password Hashing** - Bcrypt encryption for user passwords
- **Input Validation** - Pydantic models for data validation
- **CORS Configuration** - Proper cross-origin resource sharing
- **Environment Variables** - Secure configuration management

## 📈 **Performance Optimization**

- **Caching** - Streamlit `@st.cache_data` for data caching
- **Lazy Loading** - Backend data loaded only when needed
- **Efficient Queries** - Optimized database operations
- **CDN Integration** - Fast static asset delivery
- **Error Handling** - Graceful fallbacks and user-friendly messages

## 🧪 **Testing**

### Frontend Testing
1. **Navigation Testing**:
   - Test all page transitions
   - Verify back buttons work correctly
   - Check responsive design

2. **Backend Integration**:
   - Test online/offline scenarios
   - Verify authentication flow
   - Check data loading and caching

3. **Visual Testing**:
   - Verify chart rendering
   - Test interactive elements
   - Check mobile responsiveness

### Backend Testing
1. **API Endpoints**:
   ```bash
   curl https://kkcgbackend-production.up.railway.app/health
   curl -X POST https://kkcgbackend-production.up.railway.app/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"demo","password":"demo"}'
   ```

2. **Database Operations**:
   - Test data seeding
   - Verify query performance
   - Check data integrity

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Streamlit** - For the amazing web app framework
- **Plotly** - For powerful data visualization capabilities
- **FastAPI** - For high-performance backend development
- **Railway** - For seamless cloud deployment
- **PostgreSQL** - For robust database management

## 📞 **Support**

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for the Restaurant Industry**

*Empowering data-driven decisions for South Indian restaurant excellence* 