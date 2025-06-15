# ⚡ KKCG Backend - Local Development Context

## 🎯 Purpose & Scope

This directory contains the **local development version** of the KKCG Analytics Backend API, providing FastAPI-based REST endpoints for restaurant demand analytics and forecasting.

---

## 📁 Directory Structure

```
backend/
├── CONTEXT.md                    # This file - backend documentation
├── main.py                       # FastAPI application with SQLAlchemy ORM
├── requirements.txt              # Python dependencies for local development
├── runtime.txt                   # Python version specification
├── railway.toml                  # Railway deployment configuration
├── docker-compose.yml            # Docker containerization setup
├── Dockerfile.backup             # Docker container configuration backup
├── README.md                     # Basic setup and deployment instructions
└── env_template.txt              # Environment variables template
```

---

## 🔧 Core Components

### **1. FastAPI Application (`main.py`)**
- **Framework**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL with SQLite fallback
- **Authentication**: JWT-based with demo credentials
- **Features**:
  - User registration and authentication
  - Outlet and dish management
  - Demand data CRUD operations
  - Analytics endpoints with aggregations
  - Database seeding with sample data
  - CORS enabled for Streamlit Cloud integration

### **2. Database Models**
- **User**: Authentication and user management
- **Outlet**: Restaurant location information
- **Dish**: Menu item catalog
- **DemandData**: Historical and predicted demand records

### **3. API Endpoints**
- **Health**: `/health` - Backend status and database connectivity
- **Authentication**: `/auth/login`, `/auth/register` - User management
- **Data**: `/outlets`, `/dishes`, `/demand-data` - CRUD operations
- **Analytics**: `/analytics/summary` - Aggregated insights
- **Utilities**: `/seed-data` - Database initialization

---

## 🔗 Dependencies & Configuration

### **Core Dependencies** (`requirements.txt`)
```python
fastapi==0.104.1      # Web framework
uvicorn==0.24.0       # ASGI server
sqlalchemy==2.0.23    # ORM and database toolkit
psycopg2-binary==2.9.9 # PostgreSQL adapter
pydantic==2.5.0       # Data validation
PyJWT==2.8.0          # JWT authentication
```

### **Environment Configuration**
```bash
DATABASE_URL=postgresql://user:password@localhost/kkcg  # PostgreSQL connection
SECRET_KEY=your-secret-key-here                         # JWT signing key
ENVIRONMENT=development                                   # Development/production mode
PORT=8000                                               # Server port
```

### **Database Configuration**
- **Primary**: PostgreSQL for production
- **Fallback**: SQLite for local development
- **Connection**: SQLAlchemy with connection pooling
- **Migration**: Automatic table creation on startup

---

## 🚀 Local Development Setup

### **Prerequisites**
```bash
python>=3.9
postgresql (optional - SQLite fallback available)
pip package manager
```

### **Installation Steps**
1. **Environment Setup**:
   ```bash
   cd backend/
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Configuration**:
   ```bash
   # Copy environment template
   cp env_template.txt .env
   
   # Edit .env with your database URL
   # For SQLite (easier): Leave DATABASE_URL empty
   # For PostgreSQL: Set DATABASE_URL=postgresql://user:password@localhost/kkcg
   ```

3. **Run Development Server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access API Documentation**:
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health

---

## 🐳 Docker Development

### **Using Docker Compose**
```bash
# Build and start containers
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### **Container Configuration**
- **FastAPI App**: Port 8000
- **PostgreSQL**: Port 5432 (if using database container)
- **Volumes**: Code mounted for live reload

---

## 🔄 Data Management

### **Sample Data Seeding**
```python
# Automatic seeding via API
POST /seed-data

# Generates sample data:
# - 5 outlets (Chennai, Hyderabad, Bangalore, Kochi, Coimbatore)
# - 10 South Indian dishes
# - 7 days of demand predictions (350 records total)
```

### **Data Structure**
```json
{
  "outlets": [
    {"id": 1, "name": "Chennai Central", "location": "Chennai, Tamil Nadu"},
    {"id": 2, "name": "Jubilee Hills", "location": "Hyderabad, Telangana"}
  ],
  "dishes": [
    {"id": 1, "name": "Masala Dosa", "category": "Main Course", "price": 120.0},
    {"id": 2, "name": "Idli Sambar", "category": "Breakfast", "price": 80.0}
  ],
  "demand_data": [
    {"outlet_name": "Chennai Central", "dish_name": "Masala Dosa", 
     "predicted_demand": 150, "weather_factor": 1.1}
  ]
}
```

---

## 🔐 Security & Authentication

### **Authentication Flow**
1. **Registration**: Create user with email/username/password
2. **Login**: Validate credentials, return JWT token
3. **Authorization**: Include token in Authorization header
4. **Demo Access**: Use `demo/demo` for testing

### **Security Features**
- **Password Hashing**: SHA256 encryption
- **JWT Tokens**: 24-hour expiration
- **CORS Configuration**: Enabled for Streamlit Cloud domains
- **Input Validation**: Pydantic models for request validation

---

## 📊 API Response Formats

### **Standard Response Structure**
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
}
```

### **Error Response Structure**
```json
{
  "detail": "Descriptive error message",
  "status_code": 400
}
```

### **Health Check Response**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-15T15:30:00.000000",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## 🔄 Current Status

### **Development Ready**
- ✅ FastAPI application with SQLAlchemy ORM
- ✅ PostgreSQL and SQLite database support
- ✅ JWT authentication system
- ✅ CORS configuration for frontend integration
- ✅ Sample data generation
- ✅ Docker containerization
- ✅ Comprehensive API documentation

### **Testing Status**
- ✅ Health endpoint functional
- ✅ Authentication endpoints working
- ✅ CRUD operations tested
- ✅ Database seeding operational
- ✅ CORS headers properly configured

---

## 🔗 Integration Points

### **Frontend Connection**
- **Streamlit App**: Connects via `utils.api_client`
- **Base URL**: http://localhost:8000 (local development)
- **Authentication**: JWT tokens with session management
- **Data Flow**: Streamlit → FastAPI → PostgreSQL/SQLite

### **Production Deployment**
- **Target**: Railway platform (see `../backend_final/CONTEXT.md`)
- **Database**: Railway PostgreSQL
- **Monitoring**: Health checks and logging
- **Scaling**: Automatic scaling on Railway

---

## 🔗 Related Documentation

- **Production Backend**: `../backend_final/CONTEXT.md`
- **Frontend Integration**: `../utils/CONTEXT.md`
- **Main Project**: `../PROJECT_CONTEXT.md`
- **Deployment Guide**: `../DEPLOYMENT_GUIDE.md`
- **System Management**: `../SYSTEM_MANAGEMENT_CONTEXT.md`

---

## 🛠️ Development Guidelines

### **Adding New Endpoints**
1. Define Pydantic models for request/response
2. Create database models if needed
3. Implement endpoint in main.py
4. Add authentication if required
5. Update API documentation
6. Test with frontend integration

### **Database Changes**
1. Modify SQLAlchemy models
2. Update sample data generation
3. Test with both PostgreSQL and SQLite
4. Ensure compatibility with production database

### **Testing Checklist**
- ✅ Endpoint functionality
- ✅ Authentication requirements
- ✅ Database operations
- ✅ Error handling
- ✅ CORS headers
- ✅ Frontend integration

---

## 📝 Maintenance Notes

### **Regular Updates**
- **Dependencies**: Keep FastAPI and SQLAlchemy updated
- **Security**: Regular security patches
- **Database**: Monitor connection pool performance
- **Logs**: Review application logs for errors

### **Known Limitations**
- **Demo Auth**: Simple authentication system (not production-grade)
- **Data Validation**: Basic input validation
- **Error Handling**: Could be more comprehensive
- **Testing**: Manual testing (no automated test suite)

---

*Last Updated: June 2025 - Context reflects current local development setup* 