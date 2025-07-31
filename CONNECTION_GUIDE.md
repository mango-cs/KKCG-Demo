# 🔗 Frontend-Backend Connection Guide

## ✅ Backend Status: DEPLOYED AND ACTIVE

**Backend URL**: `https://web-production-929f.up.railway.app`  
**Status**: 🟢 ACTIVE  
**Database**: ✅ Connected  
**Region**: Asia Southeast (Singapore)

## 🔧 Frontend Configuration Updated

### ✅ API Client Configuration
The frontend has been updated to connect to your deployed Railway backend:

**File**: `utils/api_client.py`
```python
# Updated configuration
self.base_url = "https://web-production-929f.up.railway.app"
```

### ✅ All Backend Endpoints Working
- ✅ `GET /health` - Backend health check
- ✅ `GET /outlets` - Restaurant locations (5 outlets)
- ✅ `GET /dishes` - Menu items (10 dishes)
- ✅ `GET /demand-data` - Forecasting data
- ✅ `GET /analytics/summary` - Dashboard analytics
- ✅ `POST /auth/login` - Authentication (demo/demo)
- ✅ `POST /seed-data` - Database population

## 🚀 Deploy Frontend to Streamlit Cloud

### Step 1: Go to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account (mango-cs)

### Step 2: Deploy Your App
1. Click **"New app"**
2. **Repository**: `mango-cs/KKCG-Demo`
3. **Branch**: `main`
4. **Main file path**: `Home.py`
5. **App URL**: Choose your preferred URL (e.g., `kkcg-analytics`)

### Step 3: Advanced Settings (Optional)
```toml
# Add these if needed for environment variables
[secrets]
API_BASE_URL = "https://web-production-929f.up.railway.app"
```

### Step 4: Deploy!
Click **"Deploy!"** and wait for deployment to complete.

## 🧪 Testing the Connection

### Test Backend Directly
```bash
# Health check
curl https://web-production-929f.up.railway.app/health

# API documentation
open https://web-production-929f.up.railway.app/docs

# Test authentication
curl -X POST https://web-production-929f.up.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo"}'
```

### Test Frontend Integration
Once your Streamlit app is deployed:
1. **Login**: Use credentials `demo` / `demo`
2. **Check Backend Status**: Should show "✅ Connected"
3. **View Data**: Navigate to pages to see restaurant analytics
4. **Seed Database**: Use the seed data button if needed

## 🔄 How the Connection Works

```
Streamlit Cloud Frontend → Railway Backend → PostgreSQL Database
     (Your App)              (FastAPI)         (Managed DB)
```

### Authentication Flow
1. User enters `demo` / `demo` credentials
2. Frontend sends request to `/auth/login`
3. Backend validates and returns JWT token
4. Frontend stores token and includes in subsequent requests
5. Backend validates token for protected endpoints

### Data Flow
1. Frontend requests data from specific endpoints
2. Backend processes request and queries PostgreSQL
3. Backend returns JSON data to frontend
4. Frontend displays data in interactive charts and tables

## 📊 Expected Results

### ✅ Backend Response Examples

**Health Check**:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-31T01:34:27.765896",
  "database": "connected",
  "version": "1.0.0"
}
```

**Outlets Data**:
```json
[
  {"id": 1, "name": "Chennai Central", "location": "Chennai, Tamil Nadu"},
  {"id": 2, "name": "Jubilee Hills", "location": "Hyderabad, Telangana"},
  {"id": 3, "name": "Koramangala", "location": "Bangalore, Karnataka"},
  ...
]
```

**Dishes Data**:
```json
[
  {"id": 1, "name": "Masala Dosa", "category": "Main Course", "price": 120.0},
  {"id": 2, "name": "Idli Sambar", "category": "Breakfast", "price": 80.0},
  {"id": 3, "name": "Chicken Biryani", "category": "Main Course", "price": 250.0},
  ...
]
```

## 🎯 Success Indicators

### ✅ Frontend Connected Successfully
- Backend status shows "✅ Connected"
- Login with demo/demo works
- Restaurant data loads in dashboards
- Charts and analytics display properly
- No connection error messages

### ✅ Backend Working Properly
- Health endpoint returns "healthy" status
- Database shows "connected" status
- All API endpoints respond correctly
- Authentication returns valid JWT tokens

## 🚨 Troubleshooting

### Issue: Frontend Can't Connect
**Check**: Backend status at https://web-production-929f.up.railway.app/health
**Solution**: Verify Railway deployment is active

### Issue: Authentication Fails
**Check**: Try demo/demo credentials directly via API
**Solution**: Ensure backend /auth/login endpoint is working

### Issue: No Data Loading
**Check**: Backend endpoints individually
**Solution**: Use /seed-data endpoint to populate database

### Issue: CORS Errors
**Solution**: Backend already configured for CORS with Streamlit Cloud

## 💰 Cost Summary

### ✅ Hosting Costs
- **Backend (Railway)**: $0-5/month (covered by $5 credit)
- **Frontend (Streamlit Cloud)**: Free tier available
- **Database**: Included with Railway backend
- **Total Expected**: $0-5/month

## 🏆 Next Steps

1. ✅ **Backend**: Already deployed and working
2. 🚀 **Frontend**: Deploy to Streamlit Cloud using this guide
3. 🧪 **Test**: Verify connection using demo/demo credentials
4. 📊 **Use**: Start analyzing restaurant data!

## 📞 Support

### Backend Issues
- **Railway Dashboard**: Check deployment status
- **API Docs**: https://web-production-929f.up.railway.app/docs
- **Health Check**: https://web-production-929f.up.railway.app/health

### Frontend Issues
- **Streamlit Cloud**: Check app logs in Streamlit dashboard
- **Repository**: https://github.com/mango-cs/KKCG-Demo

---

**Your KKCG Analytics system is ready for production use! 🚀** 