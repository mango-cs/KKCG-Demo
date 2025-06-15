#!/bin/bash

# Restaurant Demand Forecasting System - Startup Script
# This script starts the complete AI-powered demand forecasting system

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}"
    echo "🍛 Restaurant Demand Forecasting System"
    echo "========================================"
    echo -e "${NC}"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_status "Docker is running ✓"
}

# Check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
    print_status "Docker Compose is available ✓"
}

# Create environment file if it doesn't exist
create_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating default environment configuration..."
        cat > .env << EOF
# Database Configuration
POSTGRES_DB=restaurant_forecasting
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres123@postgres:5432/restaurant_forecasting

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://redis:6379

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=your-super-secret-key-change-in-production-$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# ML Configuration
MLFLOW_TRACKING_URI=http://mlflow:5000

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Application Settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
TIMEZONE=Asia/Kolkata

# Data Simulation
SIMULATION_START_DATE=2024-01-01
SIMULATION_DAYS=90
NUM_OUTLETS=5
NUM_DISHES=40
EOF
        print_status "Created .env file with default configuration"
    else
        print_status "Using existing .env file ✓"
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p data/{raw,processed,models,features,mlflow}
    mkdir -p monitoring/grafana/{dashboards,datasources}
    mkdir -p ml_pipeline/{models,feature_store,airflow_dags}
    print_status "Directories created ✓"
}

# Build and start services
start_services() {
    print_status "Building and starting services..."
    
    # Build images
    print_status "Building Docker images..."
    docker-compose build --no-cache
    
    # Start infrastructure services first
    print_status "Starting infrastructure services (PostgreSQL, Redis)..."
    docker-compose up -d postgres redis
    
    # Wait for database to be ready
    print_status "Waiting for database to be ready..."
    sleep 10
    
    # Start MLflow
    print_status "Starting MLflow..."
    docker-compose up -d mlflow
    
    # Start backend services
    print_status "Starting backend services..."
    docker-compose up -d backend celery-worker celery-beat
    
    # Start frontend
    print_status "Starting frontend..."
    docker-compose up -d frontend
    
    # Start monitoring services
    print_status "Starting monitoring services..."
    docker-compose up -d prometheus grafana
    
    # Start Airflow services
    print_status "Starting Airflow services..."
    docker-compose up -d airflow-webserver airflow-scheduler
    
    print_status "All services started successfully ✓"
}

# Wait for services to be healthy
wait_for_services() {
    print_status "Waiting for services to be healthy..."
    
    services=("postgres" "redis" "backend" "frontend")
    for service in "${services[@]}"; do
        print_status "Checking $service..."
        timeout=60
        while [ $timeout -gt 0 ]; do
            if docker-compose ps | grep -q "$service.*Up"; then
                print_status "$service is healthy ✓"
                break
            fi
            sleep 2
            ((timeout--))
        done
        
        if [ $timeout -eq 0 ]; then
            print_warning "$service may not be fully ready yet"
        fi
    done
}

# Generate sample data
generate_sample_data() {
    print_status "Generating sample restaurant data..."
    
    # Wait a bit more for backend to be fully ready
    sleep 15
    
    # Run data generation script
    if docker-compose exec -T backend python ml_pipeline/data_simulation/generate_data.py; then
        print_status "Sample data generated successfully ✓"
    else
        print_warning "Sample data generation failed. You can run it manually later."
    fi
}

# Display access information
show_access_info() {
    echo ""
    print_header
    echo -e "${GREEN}🎉 System is ready! Access the application at:${NC}"
    echo ""
    echo -e "${BLUE}📊 Frontend Dashboard:${NC}     http://localhost:3000"
    echo -e "${BLUE}🔧 API Documentation:${NC}      http://localhost:8000/docs"
    echo -e "${BLUE}🤖 MLflow UI:${NC}              http://localhost:5000"
    echo -e "${BLUE}📈 Grafana Monitoring:${NC}     http://localhost:3001 (admin/admin)"
    echo -e "${BLUE}🔍 Prometheus Metrics:${NC}     http://localhost:9090"
    echo -e "${BLUE}⚡ Airflow DAGs:${NC}           http://localhost:8080 (admin/admin)"
    echo ""
    echo -e "${YELLOW}Default Login Credentials:${NC}"
    echo -e "  Username: admin"
    echo -e "  Password: admin123"
    echo ""
    echo -e "${GREEN}📋 Quick Commands:${NC}"
    echo -e "  View logs:           docker-compose logs -f [service-name]"
    echo -e "  Stop system:         docker-compose down"
    echo -e "  Restart service:     docker-compose restart [service-name]"
    echo -e "  Generate new data:   docker-compose exec backend python ml_pipeline/data_simulation/generate_data.py"
    echo ""
}

# Main execution
main() {
    print_header
    
    print_status "Starting Restaurant Demand Forecasting System..."
    
    # Pre-flight checks
    check_docker
    check_docker_compose
    
    # Setup
    create_env_file
    create_directories
    
    # Start system
    start_services
    wait_for_services
    
    # Generate data
    generate_sample_data
    
    # Show access info
    show_access_info
    
    print_status "🚀 System startup completed successfully!"
}

# Handle script arguments
case "${1:-}" in
    "stop")
        print_status "Stopping all services..."
        docker-compose down
        print_status "All services stopped ✓"
        ;;
    "restart")
        print_status "Restarting system..."
        docker-compose down
        sleep 5
        main
        ;;
    "logs")
        if [ -n "${2:-}" ]; then
            docker-compose logs -f "$2"
        else
            docker-compose logs -f
        fi
        ;;
    "status")
        docker-compose ps
        ;;
    "clean")
        print_warning "This will remove all containers, images, and data. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            docker-compose down -v --rmi all
            docker system prune -f
            print_status "System cleaned ✓"
        fi
        ;;
    "data")
        print_status "Generating fresh sample data..."
        docker-compose exec backend python ml_pipeline/data_simulation/generate_data.py
        ;;
    *)
        main
        ;;
esac 