# 🚀 KKCG Analytics Backend - Production Repository

## 🎯 Purpose
Production-ready FastAPI backend for KKCG Analytics Dashboard, deployed on Railway with PostgreSQL integration.

## 🌐 Live Deployment
- **URL**: https://kkcgbackend-production.up.railway.app
- **Docs**: https://kkcgbackend-production.up.railway.app/docs
- **Status**: ✅ Active

## 📁 Structure
```
KKCGBACKEND/
├── main.py                   # Production FastAPI app
├── requirements.txt          # Dependencies
├── railway.toml             # Railway config
├── Procfile                 # Process config
└── backend_final/           # Legacy backup
```

## 🔧 Tech Stack
- FastAPI 0.104.1
- Railway PostgreSQL
- JWT Authentication
- SQLAlchemy ORM

## 📊 Data Model
- 5 South Indian restaurant outlets
- 10 authentic menu items
- 350+ demand prediction records

## 🔐 Security
- JWT tokens (24h expiration)
- Demo credentials: demo/demo
- CORS for Streamlit Cloud

## 🚀 Deployment
Auto-deploy on git push to main branch via Railway platform.

*Last Updated: June 2025* 