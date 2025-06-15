# ⚙️ Streamlit Configuration - Context & Documentation

## 🎯 Purpose & Scope

This directory contains **Streamlit configuration files** that control the appearance, behavior, and deployment settings for the KKCG Analytics Dashboard.

---

## 📁 Directory Structure

```
.streamlit/
├── CONTEXT.md                    # This file - configuration documentation
├── config.toml                   # Main Streamlit configuration
└── secrets.toml                  # Secret environment variables (gitignored)
```

---

## 🔧 Configuration Files

### **1. Main Configuration (`config.toml`)**
- **Theme Settings**: Dark mode, colors, fonts
- **Server Configuration**: Port, headless mode, CORS
- **UI Behavior**: Sidebar state, file watcher, caching
- **Performance**: Memory limits, connection timeouts

### **2. Secrets Management (`secrets.toml`)**
- **API Keys**: Backend API base URL (optional)
- **Environment Variables**: Development vs production settings
- **Database Credentials**: Connection strings (if needed)
- **Security**: JWT secrets and authentication tokens

---

## 🎨 Theme Configuration

### **Dark Theme Settings**
```toml
[theme]
primaryColor = "#FF6B35"          # KKCG Orange for buttons and highlights
backgroundColor = "#0E1117"       # Dark background
secondaryBackgroundColor = "#262730"  # Sidebar and container background
textColor = "#FAFAFA"            # Primary text color
font = "sans serif"              # Clean, modern font
```

### **UI Customization**
- **Color Scheme**: Professional dark theme matching KKCG branding
- **Typography**: Clean sans-serif fonts for readability
- **Layout**: Wide mode enabled for dashboard layouts
- **Interactive Elements**: Orange accent color for consistency

---

## 🚀 Server Configuration

### **Development Settings**
```toml
[server]
headless = false                 # Show browser automatically
port = 8501                      # Default Streamlit port
address = "localhost"            # Local development
enableCORS = true               # Allow cross-origin requests
enableWebsocketCompression = true  # Performance optimization
```

### **Production Settings**
```toml
[server]
headless = true                  # Run without browser (for cloud deployment)
enableCORS = true               # Required for Streamlit Cloud
enableWebsocketCompression = true
runOnSave = false               # Disable auto-reload in production
fileWatcherType = "none"        # Disable file watching
```

---

## 🔐 Security & Secrets

### **Environment Variables** (`secrets.toml`)
```toml
# Backend API Configuration (optional - hardcoded in api_client.py)
API_BASE_URL = "https://kkcgbackend-production.up.railway.app"

# Development Settings
ENVIRONMENT = "production"
DEBUG_MODE = false

# Authentication (optional - using demo credentials)
JWT_SECRET = "your-jwt-secret-key"
```

### **Security Considerations**
- **No Database Secrets**: Database credentials managed by Railway backend
- **API URL**: Hardcoded in api_client.py for simplicity
- **Authentication**: JWT tokens handled by backend
- **CORS**: Enabled for Railway backend communication

---

## 📊 Performance Configuration

### **Caching Settings**
```toml
[global]
developmentMode = false          # Production optimizations
maxCachedMessageAge = 2         # Clear old messages after 2 seconds
showErrorDetails = false        # Hide error details in production
```

### **Resource Management**
- **Memory**: Streamlit Cloud default limits
- **Cache**: Session-based caching for API responses
- **Compression**: WebSocket compression enabled
- **File Watching**: Disabled in production for performance

---

## 🔗 Integration Points

### **Backend Connection**
- **API Client**: Configured in `utils/api_client.py`
- **Railway Backend**: https://kkcgbackend-production.up.railway.app
- **Authentication**: JWT tokens with 24-hour expiration
- **CORS**: Enabled for cross-origin requests

### **Streamlit Cloud Deployment**
- **Platform**: Streamlit Cloud hosting
- **Git Integration**: Auto-deploy from GitHub repository
- **Environment**: Production configuration automatically applied
- **Custom Domain**: Optional custom domain configuration

---

## 🎯 Configuration Best Practices

### **Development vs Production**
```toml
# Development - show errors and enable debugging
[global]
developmentMode = true
showErrorDetails = true

[server]
headless = false
runOnSave = true

# Production - optimize for performance and security
[global]
developmentMode = false
showErrorDetails = false

[server]
headless = true
runOnSave = false
```

### **Theme Consistency**
- **Brand Colors**: Use KKCG orange (#FF6B35) consistently
- **Dark Mode**: Optimized for professional analytics interface
- **Accessibility**: High contrast for readability
- **Mobile**: Responsive design considerations

---

## 🔄 Current Status

### **Active Configuration**
- ✅ Dark theme optimized for analytics
- ✅ KKCG brand colors (#FF6B35)
- ✅ CORS enabled for Railway backend
- ✅ Production performance settings
- ✅ Security headers configured
- ✅ Mobile-responsive layout

### **Deployment Status**
- ✅ Streamlit Cloud deployment ready
- ✅ GitHub integration configured
- ✅ Auto-deployment on git push
- ✅ Environment variables properly set
- ✅ Backend integration working

---

## 🔗 Related Documentation

- **Main Project**: `../PROJECT_CONTEXT.md`
- **Pages Configuration**: `../pages/CONTEXT.md`
- **Backend Integration**: `../utils/CONTEXT.md`
- **Deployment Guide**: `../STREAMLIT_CLOUD_READY.md`
- **System Management**: `../SYSTEM_MANAGEMENT_CONTEXT.md`

---

## 🛠️ Configuration Guidelines

### **Updating Configuration**
1. **Test Locally**: Always test configuration changes locally first
2. **Commit Changes**: Push configuration updates to repository
3. **Monitor Deployment**: Watch Streamlit Cloud deployment logs
4. **Verify Functionality**: Test all pages and backend integration

### **Adding New Secrets**
1. **Local Development**: Add to `.streamlit/secrets.toml`
2. **Production**: Add via Streamlit Cloud dashboard
3. **Security**: Never commit secrets to repository
4. **Documentation**: Update this context file with new secrets

### **Theme Customization**
1. **Brand Consistency**: Maintain KKCG orange color scheme
2. **Dark Theme**: Ensure all components work with dark background
3. **Accessibility**: Maintain high contrast ratios
4. **Testing**: Test on multiple screen sizes and devices

---

## 📝 Maintenance Notes

### **Regular Updates**
- **Streamlit Version**: Keep Streamlit updated for security and features
- **Theme Compatibility**: Verify theme works with new Streamlit versions
- **Performance**: Monitor page load times and optimize as needed
- **Security**: Review and update security settings regularly

### **Troubleshooting**
- **Backend Connection**: Check CORS settings if API calls fail
- **Theme Issues**: Verify color codes and theme compatibility
- **Performance**: Monitor memory usage and caching effectiveness
- **Deployment**: Check Streamlit Cloud logs for configuration errors

---

*Last Updated: June 2025 - Context reflects current Streamlit Cloud deployment configuration* 