import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'dark_theme' not in st.session_state:
        st.session_state.dark_theme = True
    if 'animation_enabled' not in st.session_state:
        st.session_state.animation_enabled = True

def apply_dark_theme():
    """
    Apply enhanced dark theme with neumorphism and professional styling
    """
    
    # Dark theme CSS with neumorphism
    dark_theme_css = """
    <style>
    /* Import Inter and Poppins fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styles with neumorphism */
    .stApp {
        background: linear-gradient(135deg, #1A1A1A 0%, #0E1117 100%);
        color: #F5F5F5;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Main container with subtle gradient */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        background: linear-gradient(135deg, #1A1A1A 0%, #0E1117 100%);
        border-radius: 0;
        max-width: 1200px;
    }
    
    /* Enhanced Headers with gradients and shadows */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        color: #FAFAFA;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
        background: linear-gradient(135deg, #FF6B35 0%, #FFD23F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        position: relative;
    }
    
    h1::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FF6B35, transparent);
        border-radius: 2px;
    }
    
    h2 {
        color: #FF6B35;
        font-size: 2rem;
        margin-top: 2.5rem;
        margin-bottom: 1.25rem;
        font-weight: 600;
        position: relative;
        padding-left: 1rem;
    }
    
    h2::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 60%;
        background: linear-gradient(135deg, #FF6B35, #E55A2B);
        border-radius: 2px;
    }
    
    h3 {
        color: #E0E0E0;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    h4 {
        color: #CCCCCC;
        font-size: 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    
    /* Enhanced paragraph styling */
    p {
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
        color: #CCCCCC;
        margin-bottom: 1.2rem;
        text-align: justify;
    }
    
    /* Code and pre styling */
    code {
        color: #FFD23F;
        background: rgba(255, 107, 53, 0.15);
        padding: 3px 8px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 0.9em;
        border: 1px solid rgba(255, 107, 53, 0.2);
    }
    
    pre {
        background: linear-gradient(145deg, #1e1e1e, #141414);
        border: 1px solid #333;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        overflow-x: auto;
        box-shadow: 
            inset 5px 5px 10px #0a0a0a,
            inset -5px -5px 10px #2a2a2a;
    }
    
    /* Enhanced text emphasis */
    strong, b {
        color: #FF6B35;
        font-weight: 600;
    }
    
    em, i {
        color: #FFD23F;
        font-style: italic;
    }
    
    /* Lists styling */
    ul, ol {
        color: #CCCCCC;
        padding-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    li {
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    
    li::marker {
        color: #FF6B35;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1A1A1A;
        border-right: 1px solid #333;
    }
    
    .css-1d391kg .css-1d391kg {
        background-color: #1A1A1A;
    }
    
    /* Sidebar content */
    .css-1d391kg h2, .css-1d391kg h3 {
        color: #FF6B35;
        font-weight: 600;
    }
    
    /* Metric cards */
    .css-1r6slb0 {
        background-color: #1A1A1A;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Metric values */
    .css-1xarl3l {
        color: #FF6B35;
        font-weight: 600;
        font-size: 1.5rem;
    }
    
    /* Metric labels */
    .css-12w0qpk {
        color: #CCCCCC;
        font-weight: 400;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #FF6B35;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #E55A2B;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #1A1A1A;
        border: 1px solid #333;
        border-radius: 6px;
        color: #FAFAFA;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #FF6B35;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #333;
    }
    
    .stSlider > div > div > div > div {
        background-color: #FF6B35;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        background-color: #1A1A1A;
        border: 1px solid #333;
        border-radius: 6px;
        color: #FAFAFA;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B35;
        box-shadow: 0 0 0 1px #FF6B35;
    }
    
    /* Enhanced Tabs with neumorphism */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: linear-gradient(135deg, #1A1A1A 0%, #0E1117 100%);
        padding: 6px;
        border-radius: 12px;
        box-shadow: 
            inset 5px 5px 10px #0a0a0a,
            inset -5px -5px 10px #2a2a2a;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, #1e1e1e, #141414);
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        color: #CCCCCC;
        font-weight: 500;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            3px 3px 6px #0a0a0a,
            -3px -3px 6px #2a2a2a;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 
            5px 5px 15px #0a0a0a,
            -5px -5px 15px #2a2a2a,
            0 0 20px rgba(255, 107, 53, 0.2);
        color: #FAFAFA;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B35 0%, #E55A2B 100%);
        color: white;
        border-color: #FF6B35;
        transform: translateY(-3px);
        box-shadow: 
            8px 8px 20px #0a0a0a,
            -8px -8px 20px #2a2a2a,
            0 0 30px rgba(255, 107, 53, 0.4);
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .stTabs [aria-selected="true"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stTabs [aria-selected="true"]:hover::before {
        left: 100%;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1A1A1A;
        border: 1px solid #333;
        border-radius: 6px;
        color: #FAFAFA;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        background-color: #1A1A1A;
        border: 1px solid #333;
        border-top: none;
        border-radius: 0 0 6px 6px;
    }
    
    /* Enhanced KPI Cards with neumorphism */
    .kpi-card {
        background: linear-gradient(145deg, #1e1e1e, #141414);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            20px 20px 60px #0a0a0a,
            -20px -20px 60px #2a2a2a,
            inset 0 0 0 1px rgba(255, 107, 53, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 53, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            25px 25px 80px #0a0a0a,
            -25px -25px 80px #2a2a2a,
            inset 0 0 0 2px rgba(255, 107, 53, 0.2);
    }
    
    .kpi-card:hover::before {
        left: 100%;
    }
    
    /* Custom metric card (legacy) */
    .metric-card {
        background: linear-gradient(145deg, #1e1e1e, #141414);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 
            15px 15px 30px #0a0a0a,
            -15px -15px 30px #2a2a2a;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            20px 20px 40px #0a0a0a,
            -20px -20px 40px #2a2a2a,
            0 0 20px rgba(255, 107, 53, 0.3);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #FF6B35;
        margin: 0.5rem 0;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #CCCCCC;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: #4CAF50;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    /* Enhanced Insight cards */
    .insight-card {
        background: linear-gradient(145deg, #1e1e1e, #141414);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            10px 10px 20px #0a0a0a,
            -10px -10px 20px #2a2a2a;
        position: relative;
        transition: all 0.3s ease;
        border-left: 4px solid #FF6B35;
    }
    
    .insight-card:hover {
        transform: translateX(5px);
        box-shadow: 
            15px 15px 30px #0a0a0a,
            -15px -15px 30px #2a2a2a,
            0 0 15px rgba(255, 107, 53, 0.2);
    }
    
    .insight-card h4 {
        color: #FF6B35;
        margin-bottom: 0.75rem;
        font-size: 1.2rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
    }
    
    .insight-card p {
        color: #E0E0E0;
        line-height: 1.6;
        margin: 0;
        font-size: 0.95rem;
    }
    
    /* Business alert cards */
    .business-alert {
        background: linear-gradient(145deg, #1e1e1e, #141414);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            10px 10px 20px #0a0a0a,
            -10px -10px 20px #2a2a2a;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .business-alert.success {
        border-left: 4px solid #4CAF50;
    }
    
    .business-alert.warning {
        border-left: 4px solid #FFA726;
    }
    
    .business-alert.info {
        border-left: 4px solid #2196F3;
    }
    
    .business-alert.critical {
        border-left: 4px solid #F44336;
    }
    
    /* Warning/Alert boxes */
    .alert-box {
        background-color: #2A1810;
        border: 1px solid #FF6B35;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #FAFAFA;
    }
    
    .alert-box.success {
        background-color: #1A2A1A;
        border-color: #4CAF50;
    }
    
    .alert-box.warning {
        background-color: #2A2A1A;
        border-color: #FFA726;
    }
    
    /* Enhanced data table styling */
    .stDataFrame {
        background: linear-gradient(145deg, #1e1e1e, #141414);
        border: 1px solid #333;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 
            10px 10px 20px #0a0a0a,
            -10px -10px 20px #2a2a2a;
    }
    
    .stDataFrame table {
        background: transparent;
        color: #FAFAFA;
        border-collapse: separate;
        border-spacing: 0;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #FF6B35 0%, #E55A2B 100%);
        color: white;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        padding: 12px 16px;
        border: none;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .stDataFrame td {
        border-color: #333;
        padding: 10px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease;
    }
    
    .stDataFrame tr:hover td {
        background-color: rgba(255, 107, 53, 0.1);
        transform: scale(1.01);
    }
    
    .stDataFrame tr:last-child td {
        border-bottom: none;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #FF6B35;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1A1A1A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #FF6B35;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #E55A2B;
    }
    
    /* Plotly chart container */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    </style>
    """
    
    st.markdown(dark_theme_css, unsafe_allow_html=True)

def create_kpi_card(title, value, delta=None, icon="📊", card_type="primary"):
    """
    Create an enhanced KPI card with neumorphism styling
    
    Args:
        title: KPI title
        value: KPI value
        delta: Optional delta value
        icon: Icon for the card
        card_type: Type of card ("primary", "success", "warning", "info")
    """
    
    delta_html = ""
    if delta is not None:
        delta_color = "#4CAF50" if isinstance(delta, str) and "↑" in delta else "#F44336"
        delta_html = f'<div class="kpi-delta" style="color: {delta_color}; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</div>'
    
    # Color schemes for different card types
    color_schemes = {
        "primary": "#FF6B35",
        "success": "#4CAF50", 
        "warning": "#FFA726",
        "info": "#2196F3"
    }
    
    accent_color = color_schemes.get(card_type, "#FF6B35")
    
    kpi_html = f"""
    <div class="kpi-card fade-in-up">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 0.9rem; color: #B0B0B0; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">{title}</div>
        <div style="font-size: 2.2rem; font-weight: 700; color: {accent_color}; margin: 0.75rem 0; font-family: 'Poppins', sans-serif;">{value}</div>
        {delta_html}
    </div>
    """
    
    st.markdown(kpi_html, unsafe_allow_html=True)

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """
    Create a custom metric card with dark theme styling (legacy function)
    
    Args:
        title: Metric title
        value: Metric value
        delta: Optional delta value
        delta_color: Color for delta ("normal", "inverse", "off")
    """
    
    delta_html = ""
    if delta is not None:
        delta_class = "metric-delta"
        if delta_color == "inverse":
            delta_class += " inverse"
        delta_html = f'<div class="{delta_class}">{delta}</div>'
    
    metric_html = f"""
    <div class="metric-card fade-in-up">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    
    st.markdown(metric_html, unsafe_allow_html=True)

def create_insight_card(title, content):
    """
    Create an insight card with dark theme styling
    
    Args:
        title: Card title
        content: Card content
    """
    
    insight_html = f"""
    <div class="insight-card fade-in-up">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """
    
    st.markdown(insight_html, unsafe_allow_html=True)

def create_business_alert(content, alert_type="info", icon=None):
    """
    Create an enhanced business alert with neumorphism styling
    
    Args:
        content: Alert content
        alert_type: Type of alert ("info", "success", "warning", "critical")
        icon: Optional icon for the alert
    """
    
    # Default icons for different alert types
    default_icons = {
        "success": "✅",
        "warning": "⚠️", 
        "info": "💡",
        "critical": "🚨"
    }
    
    display_icon = icon or default_icons.get(alert_type, "💡")
    
    alert_html = f"""
    <div class="business-alert {alert_type} fade-in-up">
        <div style="display: flex; align-items: flex-start; gap: 1rem;">
            <div style="font-size: 1.5rem; flex-shrink: 0;">{display_icon}</div>
            <div style="flex: 1;">{content}</div>
        </div>
    </div>
    """
    
    st.markdown(alert_html, unsafe_allow_html=True)

def create_alert_box(content, alert_type="info"):
    """
    Create an alert box with styling (legacy function)
    
    Args:
        content: Alert content
        alert_type: Type of alert ("info", "success", "warning")
    """
    
    alert_html = f"""
    <div class="alert-box {alert_type}">
        {content}
    </div>
    """
    
    st.markdown(alert_html, unsafe_allow_html=True)

def set_page_config():
    """
    Set Streamlit page configuration with dark theme
    """
    
    st.set_page_config(
        page_title="📊 Kodi Kura Chitti Gaare - Demand Heatmap",
        page_icon="🍛",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.example.com/help',
            'Report a bug': 'https://www.example.com/bug',
            'About': """
            # Kodi Kura Chitti Gaare - Demand Heatmap Dashboard
            
            This dashboard provides insights into demand patterns across our South Indian restaurant outlets.
            
            **Features:**
            - Interactive demand heatmaps
            - Business insights and analytics
            - Outlet performance comparison
            - Dish popularity analysis
            
            Built with ❤️ using Streamlit and Plotly
            """
        }
    )

def add_footer():
    """
    Add a custom footer to the app
    """
    
    footer_html = """
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #1A1A1A;
        border-top: 1px solid #333;
        padding: 0.5rem;
        text-align: center;
        color: #CCCCCC;
        font-size: 0.8rem;
        z-index: 999;
    ">
        📊 Kodi Kura Chitti Gaare - Demand Analytics Dashboard | Built with Streamlit & Plotly
    </div>
    """
    
    st.markdown(footer_html, unsafe_allow_html=True)

def create_theme_toggle():
    """
    Create a theme toggle in the sidebar
    """
    
    with st.sidebar:
        st.markdown("---")
        st.subheader("🎨 Theme Settings")
        
        # Theme toggle
        theme_option = st.radio(
            "Select Theme",
            options=["🌙 Dark", "☀️ Light"],
            index=0 if st.session_state.get('dark_theme', True) else 1,
            help="Switch between dark and light themes"
        )
        
        st.session_state.dark_theme = theme_option == "🌙 Dark"
        
        # Animation toggle
        st.session_state.animation_enabled = st.checkbox(
            "🎭 Enable Animations",
            value=st.session_state.get('animation_enabled', True),
            help="Toggle smooth animations and transitions"
        )

def create_section_header(title, subtitle=None, icon="📊"):
    """
    Create a styled section header
    
    Args:
        title: Main title
        subtitle: Optional subtitle
        icon: Icon for the section
    """
    
    subtitle_html = f'<p style="color: #B0B0B0; font-size: 1rem; margin-top: 0.5rem; font-weight: 400;">{subtitle}</p>' if subtitle else ""
    
    header_html = f"""
    <div style="margin: 2rem 0 1.5rem 0; text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h2 style="color: #FF6B35; font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 2rem; margin: 0;">{title}</h2>
        {subtitle_html}
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

def create_loading_spinner(text="Loading..."):
    """
    Create a custom loading spinner
    
    Args:
        text: Loading text to display
    """
    
    spinner_html = f"""
    <div style="text-align: center; padding: 2rem;">
        <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #333; border-radius: 50%; border-top-color: #FF6B35; animation: spin 1s ease-in-out infinite;"></div>
        <p style="color: #B0B0B0; margin-top: 1rem;">{text}</p>
    </div>
    """ + """
    <style>
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """
    
    return st.markdown(spinner_html, unsafe_allow_html=True)

def apply_custom_theme_toggle():
    """
    Apply theme based on session state
    """
    
    if st.session_state.get('dark_theme', True):
        apply_dark_theme()
    else:
        # Light theme could be implemented here
        apply_dark_theme()  # For now, always use dark theme 