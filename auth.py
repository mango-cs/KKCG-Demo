import streamlit as st
import hashlib
import sqlite3
from datetime import datetime, timedelta
import uuid

class UserAuth:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Initialize user database"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                company_name TEXT,
                plan TEXT DEFAULT 'starter',
                created_at TEXT,
                is_active BOOLEAN DEFAULT 1,
                trial_end TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_restaurants (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                restaurant_name TEXT,
                location TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password with salt"""
        return hashlib.sha256(str.encode(password)).hexdigest()
    
    def create_user(self, email, password, company_name, plan="starter"):
        """Create new user account"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        user_id = str(uuid.uuid4())
        password_hash = self.hash_password(password)
        created_at = datetime.now().isoformat()
        trial_end = (datetime.now() + timedelta(days=14)).isoformat()
        
        try:
            cursor.execute('''
                INSERT INTO users (id, email, password_hash, company_name, plan, created_at, trial_end)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, email, password_hash, company_name, plan, created_at, trial_end))
            
            conn.commit()
            conn.close()
            return True, user_id
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Email already exists"
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, company_name, plan, is_active 
            FROM users 
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[3]:  # is_active
            return True, {
                'id': result[0],
                'email': email,
                'company_name': result[1],
                'plan': result[2]
            }
        return False, None
    
    def check_subscription_status(self, user_id):
        """Check if user subscription is active"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT plan, trial_end, is_active 
            FROM users 
            WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            trial_end = datetime.fromisoformat(result[1])
            is_trial_active = datetime.now() < trial_end
            return {
                'plan': result[0],
                'trial_active': is_trial_active,
                'is_active': result[2],
                'trial_days_left': max(0, (trial_end - datetime.now()).days)
            }
        return None

# Authentication UI components
def show_login_page():
    """Display login/signup interface"""
    st.markdown("""
    <div style="max-width: 400px; margin: 2rem auto; padding: 2rem; background: #2a2a3e; border-radius: 20px;">
        <h2 style="text-align: center; color: #FF6B35; margin-bottom: 2rem;">🍛 KKCG Analytics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    auth = UserAuth()
    
    with tab1:
        st.subheader("Login to Your Dashboard")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                success, user_data = auth.authenticate_user(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = user_data
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
    
    with tab2:
        st.subheader("Start Your Free Trial")
        
        with st.form("signup_form"):
            company = st.text_input("Company Name", placeholder="Your Restaurant Chain")
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            plan = st.selectbox("Choose Plan", ["starter", "professional", "enterprise"])
            
            submit = st.form_submit_button("🎉 Start Free Trial", use_container_width=True)
            
            if submit:
                success, result = auth.create_user(email, password, company, plan)
                if success:
                    st.success("✅ Account created! Please login to continue.")
                else:
                    st.error(f"❌ Error: {result}")

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
        return False
    
    return True

def show_user_info():
    """Display user info and subscription status"""
    if 'user' in st.session_state:
        user = st.session_state.user
        auth = UserAuth()
        status = auth.check_subscription_status(user['id'])
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**👋 Welcome, {user['company_name']}**")
        
        with col2:
            plan_color = {"starter": "🟢", "professional": "🟡", "enterprise": "🟣"}
            st.markdown(f"{plan_color.get(user['plan'], '⚪')} {user['plan'].title()} Plan")
        
        with col3:
            if status and status['trial_active']:
                st.markdown(f"🆓 Trial: {status['trial_days_left']} days left")
            else:
                st.markdown("💳 Active Subscription")
        
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.clear()
            st.rerun() 