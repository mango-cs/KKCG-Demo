# 🍛 KKCG Analytics System - Project Context

## 🎯 Project Overview

**KKCG Analytics Dashboard** is a comprehensive restaurant analytics system providing demand forecasting, performance analysis, and business intelligence for the South Indian restaurant chain "Kodi Kura Chitti Gaare" (KKCG).

The system combines a **Streamlit frontend** with a **Railway-hosted FastAPI backend** and **PostgreSQL database** to deliver real-time analytics and AI-powered business insights.

---

## 🏗️ System Architecture

### **Frontend: Streamlit Cloud Dashboard**
- **Platform**: Streamlit Cloud (https://streamlit.io)
- **Repository**: KKCG---FINALTEST
- **Framework**: Streamlit with Plotly visualizations
- **Theme**: Professional dark theme with KKCG branding
- **Authentication**: JWT-based with demo credentials

### **Backend: Railway API Server**
- **Platform**: Railway.app (https://railway.app)
- **Repository**: KKCGBACKEND
- **URL**: https://kkcgbackend-production.up.railway.app
- **Framework**: FastAPI with SQLAlchemy ORM
- **Database**: Railway-managed PostgreSQL

### **Integration Architecture**
```
Streamlit Cloud ←→ Railway FastAPI ←→ PostgreSQL Database
      ↑                    ↑                   ↑
   Frontend UI         REST API           Data Storage
```

---

## 📊 Business Domain

### **Restaurant Chain: Kodi Kura Chitti Gaare**
- **Cuisine**: Authentic South Indian dishes
- **Locations**: 5 outlets across South India
  - Chennai Central (Tamil Nadu)
  - Jubilee Hills (Hyderabad, Telangana)
  - Koramangala (Bangalore, Karnataka)
  - Kochi Marine Drive (Kerala)
  - Coimbatore RS Puram (Tamil Nadu)

### **Menu Portfolio**: 10 signature dishes
- Masala Dosa, Idli Sambar, Chicken Biryani
- Uttapam, Rasam Rice, Vada Sambar
- Paneer Butter Masala, Filter Coffee
- Coconut Chutney, Hyderabadi Biryani

### **Analytics Scope**
- **Demand Forecasting**: 7-day predictions with confidence intervals
- **Performance Analysis**: Outlet and dish performance rankings
- **Trend Analysis**: Historical patterns and seasonal variations
- **Business Intelligence**: AI-powered insights and recommendations

---

## 🛠️ Core Features

### **1. Interactive Dashboard (Home.py)**
- Real-time backend connection status
- User authentication and session management
- Database seeding and management tools
- System performance metrics
- Backend API integration status

### **2. Demand Forecasting Tool (pages/Forecasting_Tool.py)**
- 7-day demand predictions with confidence intervals
- Weather and event factor analysis
- Trend analysis with historical data
- Export capabilities for forecasted data
- AI-powered business recommendations

### **3. Heatmap Analytics (pages/Heatmap_Comparison.py)**
- Interactive demand heatmaps with dark theme optimization
- Outlet and dish performance rankings
- Real-time trend analysis and comparisons
- AI-powered business insights
- Performance dashboards with rankings

### **4. Backend API System**
- RESTful API with comprehensive documentation
- JWT authentication with demo access
- Database seeding with realistic sample data
- Health monitoring and status reporting
- CORS configuration for frontend integration

---

## 📁 Repository Structure

```
KKCG---FINALTEST/
├── PROJECT_CONTEXT.md              # This file - main project overview
├── DOCUMENTATION_INDEX.md          # Complete documentation index
├── SYSTEM_MANAGEMENT_CONTEXT.md    # System management and batch files
├── Home.py                         # Main dashboard application
├── pages/                          # Streamlit pages
│   ├── CONTEXT.md                  # Pages documentation (NEW)
│   ├── Forecasting_Tool.py         # Demand forecasting interface
│   └── Heatmap_Comparison.py       # Interactive analytics
├── utils/                          # Utility modules
│   ├── CONTEXT.md                  # Utilities documentation
│   ├── api_client.py               # Backend API integration
│   ├── forecasting_utils.py        # Forecasting algorithms
│   ├── heatmap_utils.py            # Visualization functions
│   └── insights.py                 # Business intelligence
├── backend/                        # Local development backend
│   ├── CONTEXT.md                  # Local backend documentation (NEW)
│   └── main.py                     # FastAPI development server
├── backend_final/                  # Production backend reference
│   ├── CONTEXT.md                  # Production backend documentation (NEW)
│   └── main.py                     # Production FastAPI application
├── .streamlit/                     # Streamlit configuration
│   ├── CONTEXT.md                  # Configuration documentation (NEW)
│   └── config.toml                 # Theme and server settings
├── requirements.txt                # Python dependencies
└── README.md                       # Basic project information
```

---

## 🔐 Security & Authentication

### **Authentication System**
- **Method**: JWT tokens with 24-hour expiration
- **Demo Access**: Username: `demo`, Password: `demo`
- **Registration**: Email/username/password signup available
- **Session**: Streamlit session state management

### **Security Features**
- **HTTPS**: Enforced by both Streamlit Cloud and Railway
- **CORS**: Configured for secure cross-origin requests
- **Input Validation**: Pydantic models validate all API requests
- **Error Sanitization**: No sensitive data exposed in error messages

---

## 🌐 Deployment Status

### **Frontend Deployment**
- ✅ **Platform**: Streamlit Cloud
- ✅ **Status**: Active and serving traffic
- ✅ **Theme**: Dark theme optimized for analytics
- ✅ **Integration**: Connected to Railway backend
- ✅ **Authentication**: Working with demo credentials

### **Backend Deployment**
- ✅ **Platform**: Railway.app
- ✅ **URL**: https://kkcgbackend-production.up.railway.app
- ✅ **Database**: Railway PostgreSQL connected
- ✅ **API Docs**: Auto-generated documentation available
- ✅ **Health Check**: Responding with status "healthy"

### **Integration Status**
- ✅ **API Connectivity**: Frontend successfully connecting to backend
- ✅ **Data Flow**: Real-time data from PostgreSQL to Streamlit
- ✅ **Authentication**: JWT tokens working across systems
- ✅ **Error Handling**: Graceful error handling and user feedback

---

## 📊 Data Model & Sample Data

### **Database Schema**
- **Users**: Authentication and user management
- **Outlets**: Restaurant location information  
- **Dishes**: Menu item catalog with pricing
- **DemandData**: Historical and predicted demand records

### **Sample Dataset**
- **Records**: 350+ demand predictions (5 outlets × 10 dishes × 7 days)
- **Time Range**: 7-day rolling predictions
- **Data Quality**: Realistic business patterns with seasonal variations
- **Seeding**: Automated sample data generation via API endpoint

---

## 🔄 Recent Updates & Improvements

### **Production Readiness (June 2025)**
- ✅ **Backend-Only Mode**: Removed all fallback mechanisms
- ✅ **Railway Integration**: Full PostgreSQL integration
- ✅ **Import Fixes**: Resolved utility function import errors
- ✅ **Color Optimization**: Improved heatmap colors for dark theme
- ✅ **Layout Fixes**: Removed floating UI elements
- ✅ **Context Documentation**: Comprehensive context files added

### **Performance Optimizations**
- **Caching**: Streamlit data and resource caching implemented
- **Connection Pooling**: Database connection optimization
- **Error Recovery**: Graceful handling of backend failures
- **UI Responsiveness**: Mobile-friendly responsive design

---

## 🔗 Integration Points

### **Frontend ↔ Backend Communication**
- **Protocol**: HTTP REST API with JSON payloads
- **Authentication**: JWT Bearer tokens in Authorization headers
- **Error Handling**: Comprehensive error responses with user feedback
- **Rate Limiting**: Built-in protection against API abuse

### **Data Pipeline**
```
User Input → Streamlit UI → API Client → Railway FastAPI → PostgreSQL → Response
```

### **Real-Time Features**
- **Backend Status**: Live connection monitoring
- **Data Refresh**: Real-time data updates and refresh capabilities
- **Health Monitoring**: Continuous backend health checking
- **Session Management**: Persistent authentication across pages

---

## 🎯 Business Value

### **For Restaurant Management**
- **Demand Forecasting**: Predict demand 7 days ahead with confidence intervals
- **Inventory Optimization**: Reduce waste with accurate demand predictions
- **Performance Analysis**: Identify top-performing outlets and dishes
- **Trend Insights**: Understand seasonal patterns and customer preferences

### **For Operations Teams**
- **Real-Time Dashboards**: Monitor performance across all outlets
- **Data Export**: CSV exports for external analysis
- **AI Recommendations**: Actionable business insights
- **Mobile Access**: Responsive design for mobile management

---

## 🔗 Related Documentation

### **Component Documentation**
- **Pages**: `pages/CONTEXT.md` - Streamlit pages and user interface
- **Utilities**: `utils/CONTEXT.md` - Backend integration and analytics
- **Backend Local**: `backend/CONTEXT.md` - Local development setup
- **Backend Production**: `backend_final/CONTEXT.md` - Production deployment
- **Configuration**: `.streamlit/CONTEXT.md` - Streamlit settings

### **System Documentation**
- **Documentation Index**: `DOCUMENTATION_INDEX.md` - Complete documentation map
- **System Management**: `SYSTEM_MANAGEMENT_CONTEXT.md` - Batch files and automation
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md` - Deployment instructions
- **Streamlit Cloud**: `STREAMLIT_CLOUD_READY.md` - Cloud deployment guide

---

## 🛠️ Development Guidelines

### **For Frontend Development**
1. **Setup**: Clone repository and install requirements
2. **Backend**: Ensure backend is running (local or Railway)
3. **Testing**: Test with demo credentials (demo/demo)
4. **Styling**: Maintain KKCG orange theme (#FF6B35)
5. **Documentation**: Update relevant CONTEXT.md files

### **For Backend Development**
1. **Local Setup**: Use `backend/` directory for development
2. **Database**: PostgreSQL or SQLite fallback
3. **Testing**: Use `/docs` endpoint for API testing
4. **Production**: Deploy via `backend_final/` directory
5. **Documentation**: Update backend CONTEXT.md files

---

## 📈 Future Roadmap

### **Short-Term Enhancements**
- **Advanced Authentication**: OAuth integration for production
- **Real-Time Data**: WebSocket integration for live updates
- **Advanced Analytics**: More sophisticated ML models
- **Mobile App**: Native mobile application development

### **Long-Term Vision**
- **Multi-Chain Support**: Support for multiple restaurant chains
- **AI Assistant**: Conversational AI for business insights
- **Predictive Maintenance**: Equipment and supply chain optimization
- **Integration APIs**: Third-party POS and inventory system integration

---

## 📞 Support & Maintenance

### **Technical Support**
- **Frontend Issues**: Check Streamlit Cloud logs and CONTEXT.md files
- **Backend Issues**: Monitor Railway logs and health endpoints
- **Integration Issues**: Verify API connectivity and authentication
- **Documentation**: Comprehensive context files in each directory

### **Maintenance Schedule**
- **Daily**: Health check monitoring
- **Weekly**: Log review and performance analysis
- **Monthly**: Dependency updates and security patches
- **Quarterly**: Performance optimization and feature planning

---

*Last Updated: June 2025 - Context reflects current production deployment state with comprehensive documentation* 