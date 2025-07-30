# 🚂 KKCG Analytics Backend - Railway Deployment

## 📋 Overview
This directory contains the **production-ready FastAPI backend** optimized for Railway deployment. It includes the complete KKCG Analytics API with all endpoints and PostgreSQL integration.

## 🗂️ Files Structure
```
railway_backend/
├── main.py           # Complete FastAPI application (543 lines)
├── requirements.txt  # Python dependencies
├── Procfile         # Railway process configuration  
├── railway.toml     # Railway deployment settings
├── runtime.txt      # Python version specification
└── README.md        # This file
```

## 🚀 Quick Railway Deployment

### Method 1: Deploy This Directory Directly
1. **Create New Railway Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `mango-cs/KKCG-Demo` repository
   - **Important**: Set root directory to `railway_backend/`

2. **Add PostgreSQL Database**
   - Click "New Service" → "PostgreSQL"
   - Railway automatically provides `DATABASE_URL`

3. **Set Environment Variables**
   ```
   DATABASE_URL=postgresql://[auto-provided-by-railway]
   SECRET_KEY=[generate-new-secret]
   ```

4. **Deploy!**
   - Railway will auto-detect FastAPI and deploy
   - Visit `/health` endpoint to verify deployment

### Method 2: Copy Files to Repository Root
1. Copy all files from this directory to your repository root
2. Deploy from root directory via Railway

## 🔧 Configuration Details

### FastAPI Application (`main.py`)
- **Complete Implementation**: 543 lines with all endpoints
- **Database**: PostgreSQL with SQLite fallback
- **Authentication**: JWT tokens (demo credentials: demo/demo)
- **Features**:
  - 5 South Indian restaurant outlets
  - 10 authentic menu items  
  - Demand forecasting APIs
  - Data seeding endpoint (`/seed-data`)
  - Analytics dashboard APIs

### Dependencies (`requirements.txt`)
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
PyJWT==2.8.0
```

### Railway Configuration (`railway.toml`)
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

## 🔐 API Endpoints

### Health & Status
- `GET /` - API status and version
- `GET /health` - Health check with database status

### Authentication  
- `POST /auth/login` - User login (demo: demo/demo)
- `POST /auth/register` - User registration

### Data Endpoints
- `GET /outlets` - Restaurant locations
- `GET /dishes` - Menu items  
- `GET /demand-data` - Demand forecasting data
- `GET /analytics/summary` - Dashboard analytics

### Database Management
- `POST /seed-data` - Populate database with sample data

## 💰 Railway Pricing
- **Free Tier**: $5 monthly credit (covers most small apps)
- **Usage-Based**: Pay only for what you use beyond credit
- **Expected Cost**: $0-5/month for typical usage

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app.up.railway.app/health
```

### 2. Authentication Test
```bash
curl -X POST https://your-app.up.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo"}'
```

### 3. Data Endpoints
```bash
curl https://your-app.up.railway.app/outlets
curl https://your-app.up.railway.app/dishes
curl https://your-app.up.railway.app/demand-data
```

### 4. Seed Database
```bash
curl -X POST https://your-app.up.railway.app/seed-data
```

## 📚 API Documentation
Once deployed, visit:
- **Swagger UI**: `https://your-app.up.railway.app/docs`
- **ReDoc**: `https://your-app.up.railway.app/redoc`

## 🔄 Frontend Integration
Update your Streamlit frontend to point to the new Railway URL:
```python
API_BASE_URL = "https://your-new-app.up.railway.app"
```

## 🚨 Troubleshooting

### Common Issues
1. **Build Failures**: Check Railway logs for Python version/dependency issues
2. **Database Connection**: Verify `DATABASE_URL` environment variable
3. **Port Issues**: Ensure app binds to `0.0.0.0:$PORT`

### Environment Variables
Generate a new secret key:
```python
import secrets
print(secrets.token_urlsafe(32))
```

## 📞 Support
- **Railway Documentation**: [docs.railway.com](https://docs.railway.com)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Project Issues**: Use GitHub issues in this repository

---

**This backend contains your complete KKCG Analytics API and is ready for production deployment on Railway! 🚀** 