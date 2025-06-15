# 📊 Streamlit Pages - Context & Documentation

## 🎯 Purpose & Scope

This directory contains the **Streamlit pages** for the KKCG Analytics Dashboard, providing interactive analytics tools for restaurant demand forecasting and performance analysis.

---

## 📁 Directory Structure

```
pages/
├── CONTEXT.md                    # This file - pages documentation
├── Forecasting_Tool.py          # AI-powered demand forecasting interface
├── Heatmap_Comparison.py         # Interactive heatmap analytics
└── __pycache__/                  # Python cache files
```

---

## 🔧 Core Components

### **1. Forecasting Tool (`Forecasting_Tool.py`)**
- **Purpose**: Interactive demand forecasting with AI insights
- **Features**: 
  - 7-day demand predictions with confidence intervals
  - Weather and event factor analysis
  - Trend analysis and business recommendations
  - Export capabilities for forecasted data
- **Backend Integration**: Live Railway API integration
- **Authentication**: Required for full functionality

### **2. Heatmap Comparison (`Heatmap_Comparison.py`)**
- **Purpose**: Visual analytics and performance comparison
- **Features**:
  - Interactive demand heatmaps with dark theme optimization
  - Outlet and dish performance rankings
  - Real-time trend analysis
  - AI-powered business insights and recommendations
- **Visualization**: Plotly-based with custom styling
- **Color Scheme**: Plasma colormap optimized for dark themes

---

## 🔗 Dependencies & Integration

### **Backend Connection**
- **API Client**: `utils.api_client` for Railway backend communication
- **Authentication**: JWT-based auth with demo/demo credentials
- **Data Flow**: Live PostgreSQL → Railway API → Streamlit pages

### **Utility Modules**
- **Forecasting**: `utils.forecasting_utils` for prediction algorithms
- **Heatmaps**: `utils.heatmap_utils` for visualization functions
- **API Client**: `utils.api_client` for backend communication

### **Required Libraries**
```python
streamlit>=1.28.0
plotly>=5.15.0
pandas>=2.0.0
requests>=2.31.0
```

---

## 🎨 UI/UX Design Standards

### **Visual Theme**
- **Primary Color**: `#FF6B35` (KKCG Orange)
- **Background**: Dark theme with gradients
- **Cards**: Rounded corners with hover effects
- **Typography**: Professional with clear hierarchy

### **Navigation**
- **Home Button**: Available on all pages
- **Backend Status**: Real-time connection indicator
- **Responsive Design**: Works on desktop and mobile

### **User Experience**
- **Loading States**: Spinners for backend operations
- **Error Handling**: User-friendly error messages
- **Data Validation**: Input validation with helpful feedback
- **Export Options**: CSV download capabilities

---

## 📊 Data Architecture

### **Data Flow**
1. **Authentication**: Login with demo credentials or registration
2. **Backend Query**: API calls to Railway-hosted backend
3. **Data Processing**: Pandas-based analysis and transformation
4. **Visualization**: Plotly charts with custom styling
5. **User Interaction**: Filters, controls, and export options

### **Data Sources**
- **Primary**: Railway PostgreSQL database via FastAPI
- **Structure**: Outlets, dishes, demand predictions, timestamps
- **Updates**: Real-time data seeding and refresh capabilities

---

## 🔐 Security & Authentication

### **Authentication Model**
- **JWT Tokens**: Secure backend communication
- **Demo Access**: `demo/demo` for testing
- **Session Management**: Streamlit session state
- **Error Handling**: Graceful auth failures

### **Data Security**
- **API Validation**: Backend request validation
- **CORS Configuration**: Properly configured for Streamlit Cloud
- **Environment Variables**: Secure credential management

---

## 🚀 Development Guidelines

### **Adding New Pages**
1. Create new `.py` file in `pages/` directory
2. Follow naming convention: `Page_Name.py`
3. Import required utilities and API client
4. Implement consistent UI/UX patterns
5. Add backend integration and error handling
6. Update this context file with new page documentation

### **Code Standards**
- **Imports**: Organize imports with utils first, then external libraries
- **Functions**: Use descriptive docstrings
- **Error Handling**: Comprehensive try/catch blocks
- **Caching**: Use `@st.cache_data` for performance
- **Styling**: Consistent CSS and HTML usage

### **Testing Requirements**
- **Backend Connection**: Test with live Railway backend
- **Authentication**: Verify login/logout functionality  
- **Data Loading**: Test with seeded and empty databases
- **UI Responsiveness**: Check mobile and desktop layouts
- **Error Scenarios**: Test offline and error conditions

---

## 📈 Performance Optimization

### **Caching Strategy**
- **Data Caching**: `@st.cache_data` for backend responses
- **Resource Caching**: `@st.cache_resource` for API clients
- **Session State**: Efficient state management

### **Loading Optimization**
- **Lazy Loading**: Load data only when needed
- **Progress Indicators**: User feedback during operations
- **Error Recovery**: Graceful handling of timeouts

---

## 🔄 Current Status

### **Production Ready**
- ✅ Backend integration with Railway API
- ✅ Authentication and security implemented
- ✅ Dark theme optimization
- ✅ Mobile responsive design
- ✅ Export functionality
- ✅ Real-time data updates

### **Recent Updates**
- **Color Scheme**: Updated heatmap to Plasma colormap for better dark theme contrast
- **Layout Fixes**: Removed floating UI elements in filter controls
- **Import Fixes**: Resolved module import errors for utility functions
- **Backend Integration**: Full Railway PostgreSQL integration

---

## 🔗 Related Documentation

- **Main Project**: `../PROJECT_CONTEXT.md`
- **API Client**: `../utils/CONTEXT.md`
- **Backend System**: `../backend/CONTEXT.md`
- **Deployment**: `../STREAMLIT_CLOUD_READY.md`
- **System Management**: `../SYSTEM_MANAGEMENT_CONTEXT.md`

---

## 📝 Maintenance Notes

### **Regular Updates Required**
- **Dependencies**: Keep Streamlit and Plotly updated
- **Backend Compatibility**: Ensure API compatibility
- **Security Patches**: Regular security updates
- **Performance Monitoring**: Monitor loading times and user experience

### **Known Limitations**
- **Demo Data**: Limited to sample dataset without real-time restaurant data
- **Authentication**: Simple demo auth system (not production-grade)
- **Offline Mode**: Requires backend connection for functionality

---

*Last Updated: June 2025 - Context reflects current production deployment state* 