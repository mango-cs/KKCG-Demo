# 🚀 KKCG Analytics Migration Guide

## Overview
This guide walks you through migrating your KKCG Analytics Backend from your old Railway account to a new Railway account and uploading the project to your new GitHub repository.

## 📋 Pre-Migration Checklist

### Current Setup
- **Current Backend**: https://kkcgbackend-production.up.railway.app
- **Current Repo**: https://github.com/DarkAvenger420/KKCGBACKEND.git
- **Target Repo**: https://github.com/mango-cs/KKCG-Demo.git
- **Database**: PostgreSQL with sample data

### What You'll Need
- [ ] New Railway account
- [ ] Access to mango-cs/KKCG-Demo repository
- [ ] Git installed locally
- [ ] Railway CLI installed (optional but recommended)

## 🔄 Step 1: Set Up New GitHub Repository

### 1.1 Clone Your Current Project Locally
```bash
git clone https://github.com/DarkAvenger420/KKCGBACKEND.git
cd KKCGBACKEND
```

### 1.2 Add New Remote Repository
```bash
# Add your new repo as origin
git remote remove origin
git remote add origin https://github.com/mango-cs/KKCG-Demo.git

# Verify the remote
git remote -v
```

### 1.3 Push to New Repository
```bash
# Push all branches to new repository
git push -u origin main

# Push any other branches if they exist
git push origin --all
```

## 🚂 Step 2: Create New Railway Project

### 2.1 Sign Up for New Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with your new account
3. Verify your email

### 2.2 Connect GitHub Repository
1. In Railway dashboard, click "New Project"
2. Choose "Deploy from GitHub repo"
3. Connect your GitHub account (mango-cs)
4. Select the `KKCG-Demo` repository
5. Choose the main branch

### 2.3 Configure Deployment
Railway should automatically detect your FastAPI app, but verify:
- **Build Command**: Automatic (Nixpacks)
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Dockerfile**: Not needed (Railway will use your `railway.toml`)

## 🗄️ Step 3: Set Up Database

### 3.1 Add PostgreSQL Service
1. In your Railway project, click "New Service"
2. Choose "PostgreSQL"
3. Railway will automatically create the database
4. Copy the connection details

### 3.2 Configure Environment Variables
Add these environment variables to your Railway service:
```
DATABASE_URL=postgresql://[automatically provided by Railway]
SECRET_KEY=[generate a new secret key]
```

To generate a new secret key:
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 3.3 Seed Database with Sample Data
Once your app is deployed, visit:
```
https://your-new-app.up.railway.app/seed-data
```

This will populate your database with the sample restaurant data.

## 🔧 Step 4: Update Configuration Files

### 4.1 Verify `railway.toml`
Your current configuration should work, but verify:
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

### 4.2 Verify `Procfile`
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 4.3 Update Dependencies (if needed)
Your current `requirements.txt` looks good:
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
PyJWT==2.8.0
```

## ✅ Step 5: Test Migration

### 5.1 Verify API Endpoints
Test these endpoints on your new deployment:
- `GET /health` - Should return healthy status
- `POST /auth/login` - Test with demo/demo credentials
- `GET /outlets` - Should return 5 restaurants
- `GET /dishes` - Should return 10 dishes
- `GET /demand-data` - Should return forecasting data

### 5.2 Test Frontend Integration
Update your Streamlit app (if you have it) to point to the new Railway URL:
```python
# Update the API base URL in your frontend
API_BASE_URL = "https://your-new-app.up.railway.app"
```

## 💰 Cost Estimation

### Railway Pricing (New Account)
- **Starter Plan**: $5 monthly credit (enough for small apps)
- **Usage-based pricing**: Only pay for what you use beyond the credit
- **Your app usage**: Likely to stay within free tier for development

### Expected Monthly Cost
- **Development/Testing**: $0 (covered by $5 credit)
- **Production with moderate traffic**: $0-10/month
- **High traffic**: Scales with usage

## 🔒 Security Considerations

### 5.1 Environment Variables
- Use Railway's environment variable management
- Never commit secrets to Git
- Generate new `SECRET_KEY` for production

### 5.2 Database Security
- Railway provides managed PostgreSQL with built-in security
- Database credentials are automatically managed
- Use SSL connections (enabled by default)

## 🚨 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check your requirements.txt format
# Ensure Python version compatibility
# Verify Railway logs for specific errors
```

#### Database Connection Issues
```bash
# Verify DATABASE_URL environment variable
# Check PostgreSQL service is running
# Test connection manually
```

#### Port Configuration
```bash
# Ensure your app binds to 0.0.0.0:$PORT
# Railway automatically provides PORT environment variable
```

### Getting Help
1. Railway Discord community
2. Railway documentation
3. GitHub issues in your repository

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.com/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL with Railway](https://docs.railway.com/databases/postgresql)

## 🎯 Next Steps After Migration

1. **Update DNS** (if using custom domain)
2. **Monitor performance** using Railway metrics
3. **Set up monitoring alerts**
4. **Configure backup strategy**
5. **Update documentation** with new URLs

---

**Migration Checklist:**
- [ ] Repository uploaded to mango-cs/KKCG-Demo
- [ ] New Railway project created
- [ ] PostgreSQL database configured
- [ ] Environment variables set
- [ ] Database seeded with sample data
- [ ] All API endpoints tested
- [ ] Frontend updated (if applicable)
- [ ] Documentation updated

**Estimated Migration Time**: 30-60 minutes

---

*This migration maintains all your current functionality while moving to your new accounts. Your app architecture and code remain unchanged.* 