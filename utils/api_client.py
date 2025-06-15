import requests
import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import os

class KKCGAPIClient:
    """API client for KKCG Analytics Backend"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"
    
    def login(self, username: str, password: str) -> Dict:
        """Login to get access token"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.set_token(data["access_token"])
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": response.json().get("detail", "Login failed")}
        
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def register(self, username: str, email: str, password: str) -> Dict:
        """Register new user"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={"username": username, "email": email, "password": password}
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.json().get("detail", "Registration failed")}
        
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_outlets(self) -> List[Dict]:
        """Get all outlets"""
        try:
            response = requests.get(
                f"{self.base_url}/outlets",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Failed to fetch outlets: {response.json().get('detail', 'Unknown error')}")
                return []
        
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
            return []
    
    def get_dishes(self) -> List[Dict]:
        """Get all dishes"""
        try:
            response = requests.get(
                f"{self.base_url}/dishes",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Failed to fetch dishes: {response.json().get('detail', 'Unknown error')}")
                return []
        
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
            return []
    
    def get_demand_data(self, 
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None,
                       outlet_id: Optional[int] = None,
                       dish_id: Optional[int] = None) -> pd.DataFrame:
        """Get demand data as DataFrame"""
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
            
            response = requests.get(
                f"{self.base_url}/demand-data",
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    df['date'] = pd.to_datetime(df['date'])
                    return df
                else:
                    return pd.DataFrame()
            else:
                st.error(f"Failed to fetch demand data: {response.json().get('detail', 'Unknown error')}")
                return pd.DataFrame()
        
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
            return pd.DataFrame()
    
    def get_analytics_summary(self) -> Dict:
        """Get analytics summary"""
        try:
            response = requests.get(
                f"{self.base_url}/analytics/summary",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Failed to fetch analytics: {response.json().get('detail', 'Unknown error')}")
                return {}
        
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
            return {}
    
    def seed_database(self) -> Dict:
        """Seed database with sample data"""
        try:
            response = requests.post(
                f"{self.base_url}/seed-data",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {"success": True, "message": response.json()["message"]}
            else:
                return {"success": False, "error": response.json().get("detail", "Seeding failed")}
        
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def health_check(self) -> bool:
        """Check if backend is accessible"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False

def get_api_client() -> KKCGAPIClient:
    """Get API client instance"""
    if 'api_client' not in st.session_state:
        st.session_state.api_client = KKCGAPIClient()
    
    return st.session_state.api_client

def check_authentication():
    """Check if user is authenticated"""
    return 'access_token' in st.session_state and st.session_state.access_token is not None

def login_required(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not check_authentication():
            st.error("🔒 Please login to access this feature")
            show_login_form()
            return None
        return func(*args, **kwargs)
    return wrapper

def show_login_form():
    """Show login/register form"""
    st.markdown("### 🔐 Authentication Required")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if username and password:
                    client = get_api_client()
                    result = client.login(username, password)
                    
                    if result["success"]:
                        st.session_state.access_token = result["data"]["access_token"]
                        st.session_state.username = username
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['error']}")
                else:
                    st.error("Please enter both username and password")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            email = st.text_input("Email")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register = st.form_submit_button("Register")
            
            if register:
                if new_username and email and new_password and confirm_password:
                    if new_password == confirm_password:
                        client = get_api_client()
                        result = client.register(new_username, email, new_password)
                        
                        if result["success"]:
                            st.success("✅ Registration successful! Please login.")
                        else:
                            st.error(f"❌ {result['error']}")
                    else:
                        st.error("Passwords don't match")
                else:
                    st.error("Please fill all fields")

def show_backend_status():
    """Show backend connection status"""
    client = get_api_client()
    
    if client.health_check():
        st.success("🟢 Backend Connected")
        return True
    else:
        st.error("🔴 Backend Offline - Using Demo Mode")
        return False 