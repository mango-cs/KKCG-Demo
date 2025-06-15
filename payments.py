import streamlit as st
import stripe
import sqlite3
from datetime import datetime, timedelta
import os

# Set your Stripe keys
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_stripe_secret_key")

class PaymentManager:
    def __init__(self):
        self.pricing = {
            "starter": {
                "setup_fee": 299,
                "monthly_fee": 49,
                "features": [
                    "Up to 3 restaurant outlets",
                    "Basic demand forecasting", 
                    "Standard analytics",
                    "Email support"
                ]
            },
            "professional": {
                "setup_fee": 799,
                "monthly_fee": 149,
                "features": [
                    "Up to 10 restaurant outlets",
                    "Advanced AI forecasting",
                    "Custom dishes/menus", 
                    "Priority support",
                    "API access"
                ]
            },
            "enterprise": {
                "setup_fee": 1999,
                "monthly_fee": 399,
                "features": [
                    "Unlimited outlets",
                    "White-label solution",
                    "Custom integrations",
                    "Dedicated support",
                    "Custom analytics"
                ]
            }
        }
    
    def create_stripe_checkout_session(self, plan, user_email, setup_only=False):
        """Create Stripe checkout session"""
        try:
            plan_info = self.pricing[plan]
            
            line_items = []
            
            if setup_only:
                # One-time setup fee only
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'KKCG Analytics - {plan.title()} Setup',
                            'description': f'One-time setup fee for {plan.title()} plan'
                        },
                        'unit_amount': plan_info['setup_fee'] * 100,  # Stripe uses cents
                    },
                    'quantity': 1,
                })
            else:
                # Both setup fee and monthly subscription
                line_items.extend([
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'KKCG Analytics - {plan.title()} Setup',
                            },
                            'unit_amount': plan_info['setup_fee'] * 100,
                        },
                        'quantity': 1,
                    },
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'KKCG Analytics - {plan.title()} Monthly',
                            },
                            'unit_amount': plan_info['monthly_fee'] * 100,
                            'recurring': {
                                'interval': 'month',
                            },
                        },
                        'quantity': 1,
                    }
                ])
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='subscription' if not setup_only else 'payment',
                success_url='https://your-app.streamlit.app/?success=true',
                cancel_url='https://your-app.streamlit.app/?canceled=true',
                customer_email=user_email,
                metadata={
                    'plan': plan,
                    'user_email': user_email
                }
            )
            
            return checkout_session.url
        except Exception as e:
            st.error(f"Payment setup error: {e}")
            return None
    
    def update_user_subscription(self, user_id, plan, stripe_customer_id=None):
        """Update user subscription in database"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET plan = ?, is_active = 1, stripe_customer_id = ?
            WHERE id = ?
        ''', (plan, stripe_customer_id, user_id))
        
        conn.commit()
        conn.close()
    
    def show_pricing_page(self):
        """Display pricing plans"""
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h1 style="color: #FF6B35; font-size: 3rem;">💰 Choose Your Plan</h1>
            <p style="color: #E8F4FD; font-size: 1.2rem;">Start your restaurant analytics journey today</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="large")
        
        for i, (plan, details) in enumerate(self.pricing.items()):
            col = [col1, col2, col3][i]
            
            with col:
                # Plan highlight for professional
                highlight = plan == "professional"
                border_color = "#FF6B35" if highlight else "rgba(255,255,255,0.1)"
                
                st.markdown(f"""
                <div style="
                    background: #2a2a3e; 
                    border-radius: 20px; 
                    padding: 2rem; 
                    border: 2px solid {border_color};
                    height: 500px;
                    position: relative;
                ">
                    {f'<div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #FF6B35; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">🔥 POPULAR</div>' if highlight else ''}
                    
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <h2 style="color: #FF6B35; margin: 0; text-transform: capitalize;">{plan}</h2>
                        <div style="margin: 1rem 0;">
                            <span style="color: #E8F4FD; font-size: 2rem; font-weight: bold;">${details['setup_fee']}</span>
                            <span style="color: #BDC3C7; font-size: 0.9rem;"> setup</span>
                        </div>
                        <div>
                            <span style="color: #E8F4FD; font-size: 1.5rem; font-weight: bold;">${details['monthly_fee']}</span>
                            <span style="color: #BDC3C7; font-size: 0.9rem;">/month</span>
                        </div>
                    </div>
                    
                    <div style="text-align: left;">
                """, unsafe_allow_html=True)
                
                for feature in details['features']:
                    st.markdown(f"✅ {feature}")
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                if st.button(f"🚀 Choose {plan.title()}", key=f"select_{plan}", use_container_width=True):
                    if 'user' in st.session_state:
                        user = st.session_state.user
                        checkout_url = self.create_stripe_checkout_session(
                            plan, user['email']
                        )
                        if checkout_url:
                            st.markdown(f"[💳 **Complete Payment →**]({checkout_url})")
                    else:
                        st.error("Please login first to select a plan")

def show_billing_page():
    """Display billing and subscription management"""
    st.header("💳 Billing & Subscription")
    
    if 'user' in st.session_state:
        user = st.session_state.user
        
        # Current plan info
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Current Plan")
            plan_colors = {"starter": "🟢", "professional": "🟡", "enterprise": "🟣"}
            st.markdown(f"{plan_colors.get(user['plan'], '⚪')} **{user['plan'].title()} Plan**")
            
            pm = PaymentManager()
            current_plan = pm.pricing[user['plan']]
            st.metric("Setup Fee", f"${current_plan['setup_fee']}")
            st.metric("Monthly Fee", f"${current_plan['monthly_fee']}")
        
        with col2:
            st.subheader("Usage Statistics")
            st.metric("Restaurants Added", "3", "▲ 1 this month")
            st.metric("Forecasts Generated", "127", "▲ 23 this month") 
            st.metric("Data Exports", "15", "▲ 5 this month")
        
        # Upgrade/downgrade options
        st.subheader("🔄 Change Plan")
        pm = PaymentManager()
        pm.show_pricing_page()
        
    else:
        st.error("Please login to view billing information")

# Usage in main app
def handle_payment_success():
    """Handle successful payment callback"""
    query_params = st.query_params
    
    if "success" in query_params:
        st.success("🎉 **Payment Successful!** Your subscription is now active.")
        st.balloons()
        
        # Update user subscription status
        if 'user' in st.session_state:
            user = st.session_state.user
            pm = PaymentManager()
            pm.update_user_subscription(user['id'], user['plan'])
    
    elif "canceled" in query_params:
        st.warning("💔 Payment was canceled. You can try again anytime.")
        st.info("Your trial period is still active. Complete payment to continue after trial.") 