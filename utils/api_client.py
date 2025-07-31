# KKCG Analytics API Client
import requests
import streamlit as st
from typing import Dict, List, Optional
import json
from datetime import datetime
import pandas as pd

class KKCGAPIClient:
    """API client for KKCG Analytics backend"""
    
    def __init__(self, base_url: str = None):
        # Use deployed Railway backend by default
        self.base_url = base_url or "https://web-production-929f.up.railway.app"
        
        # Ensure base_url doesn't end with slash
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
            
        self.session = requests.Session()
        self.session.timeout = 30  # 30 second timeout
        
        # Test backend connection on initialization
        self._validate_backend()
    
    def _validate_backend(self):
        """Validate that backend is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    st.session_state.backend_status = "✅ Connected"
                    st.session_state.backend_url = self.base_url
                    return True
        except Exception as e:
            st.session_state.backend_status = f"❌ Connection failed: {str(e)}"
            st.session_state.backend_url = self.base_url
        return False
    
    def get_connection_status(self):
        """Get backend connection status"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                db_status = data.get('database', 'unknown')
                
                if db_status == "connected":
                    return {
                        "status": "🟢 Live PostgreSQL Database",
                        "message": "Connected to production database",
                        "color": "green"
                    }
                else:
                    return {
                        "status": "🟡 Backend Online (Demo Data)",
                        "message": "Backend running with sample data",
                        "color": "orange"
                    }
            else:
                st.error(f"❌ Backend Error: HTTP {response.status_code}")
                st.stop()
        except Exception as e:
            st.error(f"❌ **Backend Connection Lost**: {str(e)}")
            st.error(f"🔗 Check: {self.base_url}/health")
            st.stop()
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def login(self, username: str, password: str) -> Dict:
        """Login to get access token"""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.set_token(data["access_token"])
                return {"success": True, "data": data}
            else:
                error_detail = response.json().get("detail", "Login failed")
                return {"success": False, "error": error_detail}
        
        except requests.exceptions.Timeout:
            st.error("❌ **Request Timeout**: Backend is slow to respond")
            return {"success": False, "error": "Request timeout - backend may be overloaded"}
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **Connection Error**: {str(e)}")
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def register(self, username: str, email: str, password: str) -> Dict:
        """Register new user"""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/register",
                json={"username": username, "email": email, "password": password},
                timeout=30
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                error_detail = response.json().get("detail", "Registration failed")
                return {"success": False, "error": error_detail}
        
        except requests.exceptions.Timeout:
            st.error("❌ **Request Timeout**: Registration is taking too long")
            return {"success": False, "error": "Request timeout during registration"}
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **Connection Error**: {str(e)}")
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_outlets(self) -> List[Dict]:
        """Get all outlets - BACKEND REQUIRED"""
        try:
            response = self.session.get(f"{self.base_url}/outlets", timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"❌ **API Error**: Failed to fetch outlets (HTTP {response.status_code})")
                st.stop()
        
        except requests.exceptions.Timeout:
            st.error("❌ **Timeout**: Outlet data request timed out")
            st.stop()
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **Connection Error**: {str(e)}")
            st.stop()
    
    def get_dishes(self) -> List[Dict]:
        """Get all dishes - BACKEND REQUIRED"""
        try:
            response = self.session.get(f"{self.base_url}/dishes", timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"❌ **API Error**: Failed to fetch dishes (HTTP {response.status_code})")
                st.stop()
        
        except requests.exceptions.Timeout:
            st.error("❌ **Timeout**: Dish data request timed out")
            st.stop()
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **Connection Error**: {str(e)}")
            st.stop()
    
    def get_demand_data(self, 
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None,
                       outlet_id: Optional[int] = None,
                       dish_id: Optional[int] = None) -> pd.DataFrame:
        """Get demand data as DataFrame - BACKEND REQUIRED"""
        try:
            params = {}
            if start_date:
                params["start_date"] = start_date.isoformat()
            if end_date:
                params["end_date"] = end_date.isoformat()
            if outlet_id:
                params["outlet_id"] = outlet_id
            if dish_id:
                params["dish_id"] = dish_id
            
            response = self.session.get(
                f"{self.base_url}/demand-data",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    df['date'] = pd.to_datetime(df['date'])
                    # Ensure column compatibility
                    if 'outlet_name' in df.columns:
                        df['outlet'] = df['outlet_name']
                    if 'dish_name' in df.columns:
                        df['dish'] = df['dish_name']
                    return df
                else:
                    st.warning("⚠️ **No Data**: Backend returned empty dataset")
                    return pd.DataFrame()
            else:
                st.error(f"❌ **API Error**: Failed to fetch demand data (HTTP {response.status_code})")
                st.stop()
        
        except requests.exceptions.Timeout:
            st.error("❌ **Timeout**: Demand data request timed out")
            st.stop()
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **Connection Error**: {str(e)}")
            st.stop()
    
    def get_analytics_summary(self) -> Dict:
        """Get analytics summary - BACKEND REQUIRED"""
        try:
            response = self.session.get(f"{self.base_url}/analytics/summary", timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"❌ **API Error**: Failed to fetch analytics (HTTP {response.status_code})")
                st.stop()
        
        except requests.exceptions.Timeout:
            st.error("❌ **Timeout**: Analytics request timed out")
            st.stop()
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **Connection Error**: {str(e)}")
            st.stop()
    
    def seed_database(self) -> Dict:
        """Seed database with sample data"""
        try:
            response = self.session.post(f"{self.base_url}/seed-data", timeout=60)
            
            if response.status_code == 200:
                return {"success": True, "message": response.json()["message"]}
            else:
                error_detail = response.json().get("detail", "Seeding failed")
                return {"success": False, "error": error_detail}
        
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout - seeding takes time, please wait"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def health_check(self) -> bool:
        """Check if backend is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            return response.status_code == 200
        except:
            return False

# Global API client instance
@st.cache_resource
def get_api_client() -> KKCGAPIClient:
    """Get cached API client instance"""
    return KKCGAPIClient()

def check_authentication():
    """Check if user is authenticated"""
    return 'access_token' in st.session_state and st.session_state.access_token is not None

def login_required(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not check_authentication():
            st.warning("🔐 **Authentication Required**")
            st.info("Please login to access this feature")
            show_login_form()
            return None
        return func(*args, **kwargs)
    return wrapper

def show_backend_status():
    """Show backend connection status"""
    client = get_api_client()
    status_info = client.get_connection_status()
    
    # Create status indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if status_info["color"] == "green":
            st.success(f"**{status_info['status']}** - {status_info['message']}")
        elif status_info["color"] == "orange":
            st.warning(f"**{status_info['status']}** - {status_info['message']}")
        else:
            st.info(f"**{status_info['status']}** - {status_info['message']}")

def show_login_form():
    """Show login/register form"""
    st.markdown("### 🔐 User Authentication")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            st.markdown("**Login to access all features**")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Login", use_container_width=True)
            with col2:
                demo_login = st.form_submit_button("Demo Login", use_container_width=True)
            
            if submit and username and password:
                client = get_api_client()
                with st.spinner("Logging in..."):
                    result = client.login(username, password)
                
                if result["success"]:
                    st.session_state.access_token = result["data"]["access_token"]
                    st.session_state.username = username
                    st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")
            
            elif demo_login:
                client = get_api_client()
                with st.spinner("Logging in with demo account..."):
                    result = client.login("demo", "demo")
                
                if result["success"]:
                    st.session_state.access_token = result["data"]["access_token"]
                    st.session_state.username = "demo"
                    st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success("✅ Demo login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ Demo login failed: {result['error']}")
            
            elif submit and (not username or not password):
                st.error("Please enter both username and password")
    
    with tab2:
        with st.form("register_form"):
            st.markdown("**Create a new account**")
            new_username = st.text_input("Choose Username", placeholder="Enter desired username")
            email = st.text_input("Email", placeholder="Enter your email")
            new_password = st.text_input("Choose Password", type="password", placeholder="Enter password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            register = st.form_submit_button("Register", use_container_width=True)
            
            if register:
                if new_username and email and new_password and confirm_password:
                    if new_password == confirm_password:
                        client = get_api_client()
                        with st.spinner("Creating account..."):
                            result = client.register(new_username, email, new_password)
                        
                        if result["success"]:
                            st.success("✅ Registration successful! Please login.")
                        else:
                            st.error(f"❌ {result['error']}")
                    else:
                        st.error("Passwords don't match")
                else:
                    st.error("Please fill all fields")

def logout():
    """Logout user"""
    if 'access_token' in st.session_state:
        del st.session_state.access_token
    if 'username' in st.session_state:
        del st.session_state.username
    if 'login_time' in st.session_state:
        del st.session_state.login_time
    st.success("✅ Logged out successfully")
    st.rerun() 