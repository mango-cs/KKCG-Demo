# 🍛 KKCG System Batch Files

Easy one-click startup and shutdown scripts for the KKCG Analytics System.

## 📁 Available Scripts

### 🚀 **start_kkcg_system.bat** (Recommended)
**Full system startup with API integration**

**What it does:**
- ✅ Starts FastAPI backend server (port 8000)
- ✅ Starts KKCG Streamlit dashboard (port 8501)  
- ✅ Opens browser automatically
- ✅ Enables full forecasting tool with live API
- ✅ Includes all analytics tools

**When to use:** When you want the complete experience with working forecasting API

---

### ⚡ **start_kkcg_app_only.bat**
**Quick dashboard-only startup**

**What it does:**
- ✅ Starts KKCG Streamlit dashboard only (port 8501)
- ✅ Opens browser automatically  
- ✅ Forecasting tool uses sample data
- ✅ Heatmap analytics fully functional

**When to use:** When you just want to see the dashboard quickly

---

### 🛑 **stop_kkcg_system.bat**
**Complete system shutdown**

**What it does:**
- ✅ Stops all Streamlit processes
- ✅ Stops all FastAPI backend processes
- ✅ Terminates related Python processes
- ✅ Clean shutdown of all services

**When to use:** To cleanly stop all KKCG services

---

## 🎯 Quick Start Instructions

### Option 1: Full System (Recommended)
```
1. Double-click: start_kkcg_system.bat
2. Wait for services to start (30-60 seconds)
3. Browser opens automatically to http://localhost:8501
4. Navigate using sidebar: Home → Forecasting_Tool → Heatmap_Comparison
```

### Option 2: Dashboard Only (Faster)
```
1. Double-click: start_kkcg_app_only.bat  
2. Wait for startup (15-30 seconds)
3. Browser opens automatically to http://localhost:8501
4. Forecasting uses sample data, analytics fully functional
```

### Stopping the System
```
1. Double-click: stop_kkcg_system.bat
2. All services will be terminated cleanly
```

---

## 🌐 Access Points

When running the full system:

| Service | URL | Description |
|---------|-----|-------------|
| **Main Dashboard** | http://localhost:8501 | KKCG Analytics Interface |
| **API Backend** | http://localhost:8000 | FastAPI Server |
| **API Documentation** | http://localhost:8000/docs | Interactive API Docs |

---

## 🎨 Features Available

### 🏠 **Home Page**
- Beautiful dark mode landing page
- Navigation cards to tools
- Business benefits overview

### 🔮 **Forecasting Tool**
- ML-powered demand predictions
- Weather & event factor integration
- SHAP explanations
- Interactive charts with confidence intervals
- CSV/JSON export

### 🔥 **Heatmap Analytics**
- Interactive demand heatmaps
- Outlet performance comparisons  
- AI business insights & recommendations
- Trend analysis
- Professional reporting

---

## 🔧 Troubleshooting

### **Port Already in Use**
If you get port errors:
1. Run `stop_kkcg_system.bat` first
2. Wait 30 seconds
3. Try starting again

### **Python Not Found**
If you see Python errors:
1. Install Python 3.8+ from python.org
2. Make sure Python is in your PATH
3. Restart command prompt

### **Dependencies Missing**
The scripts automatically install requirements, but if issues persist:
```bash
cd kkcg_app
pip install -r requirements.txt

cd ../FORECASTER/backend  
pip install -r requirements.txt
```

### **Browser Doesn't Open**
Manually navigate to:
- **Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

---

## 💡 Pro Tips

1. **First Time Setup**: Use `start_kkcg_system.bat` to ensure all dependencies install
2. **Daily Use**: Use `start_kkcg_app_only.bat` for faster startup
3. **Clean Shutdown**: Always use `stop_kkcg_system.bat` instead of closing windows
4. **Multiple Sessions**: Don't run multiple instances on same ports
5. **Performance**: Close other applications for better performance

---

## 🎯 System Requirements

- **OS**: Windows 10/11
- **Python**: 3.8 or higher  
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 500MB free space
- **Browser**: Chrome, Firefox, or Edge

---

**🍛 Happy analyzing with KKCG Analytics!** ✨ 