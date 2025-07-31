import streamlit as st
from typing import Dict, Any

# Translation dictionaries for all application text
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # ==== GENERAL NAVIGATION & COMMON ====
    "english": {
        # Navigation
        "home": "Home",
        "forecasting_tool": "AI Forecasting",
        "heatmap_analytics": "Heatmap Analytics", 
        "settings": "Settings",
        "logout": "Logout",
        "login": "Login",
        "register": "Register",
        
        # Common buttons and actions
        "refresh_data": "Refresh Data",
        "export_data": "Export Data",
        "download_csv": "Download CSV",
        "generate_report": "Generate Report",
        "seed_database": "Seed Database",
        "test_connection": "Test Connection",
        "go_to_home": "Go to Home Page",
        "back_to_home": "Back to Home",
        "launch": "Launch",
        
        # Status and authentication
        "welcome_back": "Welcome back",
        "logged_in_as": "Logged in as",
        "session_started": "Session Started",
        "access_denied": "Access Denied",
        "authentication_required": "Authentication Required",
        "connection_verified": "Connection verified",
        "connection_failed": "Connection failed",
        
        # ==== HOME PAGE ====
        "app_title": "KKCG Analytics Dashboard",
        "app_subtitle": "AI-Powered Restaurant Analytics for Kodi Kura Chitti Gaare",
        "app_description": "Live Backend Integration • Real-time Data • Professional Analytics",
        
        # Metrics
        "total_demand": "Total Demand",
        "average_per_day": "Average per Day", 
        "peak_demand": "Peak Demand",
        "menu_items": "Menu Items",
        "steady_growth": "Steady growth",
        "new_record": "New record",
        "active_dishes": "Active dishes",
        "vs_last_week": "vs last week",
        
        # Dashboard sections
        "live_performance_dashboard": "Live Performance Dashboard",
        "realtime_demand_analytics": "Real-time Demand Analytics",
        "analytics_tools": "Analytics Tools",
        "platform_benefits": "Platform Benefits",
        "quick_actions": "Quick Actions",
        
        # Tool descriptions
        "ai_demand_forecasting": "AI Demand Forecasting",
        "interactive_heatmap_analytics": "Interactive Heatmap Analytics",
        "forecasting_description": "Advanced machine learning forecasting engine with real backend data. Features seasonal analysis, confidence intervals, and AI-powered insights for optimal inventory planning.",
        "heatmap_description": "Dynamic heatmap visualization with live backend data integration. Real-time performance analysis across dishes and outlets with AI-generated business insights.",
        
        # Benefits
        "boost_revenue": "Boost Revenue",
        "reduce_waste": "Reduce Waste", 
        "save_time": "Save Time",
        "cost_control": "Cost Control",
        "future_ready": "Future Ready",
        "data_driven": "Data Driven",
        "competitive_edge": "Competitive Edge",
        "easy_to_use": "Easy to Use",
        
        "boost_revenue_desc": "Increase sales by 15-25% with optimized inventory and demand forecasting",
        "reduce_waste_desc": "Cut food waste by 30% through accurate demand predictions and smart planning",
        "save_time_desc": "Automate 80% of planning tasks with AI-powered insights and recommendations",
        "cost_control_desc": "Lower operational costs by 20% with efficient resource allocation",
        "future_ready_desc": "Stay ahead with 7-day forecasts and seasonal trend analysis",
        "data_driven_desc": "Make confident decisions backed by real-time analytics and insights",
        "competitive_edge_desc": "Outperform competitors with advanced ML-powered business intelligence",
        "easy_to_use_desc": "User-friendly interface that requires no technical expertise to operate",
        
        # ==== FORECASTING TOOL ====
        "ai_demand_forecasting_title": "AI Demand Forecasting",
        "forecasting_subtitle": "Advanced Machine Learning Predictions with Live Backend Integration",
        "forecasting_controls": "Forecasting Controls",
        "select_dish": "Select Dish",
        "select_outlet": "Select Outlet",
        "forecast_horizon": "Forecast Horizon",
        "all_dishes": "All Dishes",
        "all_outlets": "All Outlets",
        "days": "days",
        
        "performance_metrics": "Performance Metrics",
        "average_daily": "Average Daily",
        "growth_trend": "Growth Trend",
        "forecast_visualization": "AI-Powered Forecast Visualization",
        "demand_breakdown": "Demand Breakdown",
        "ai_insights_analysis": "AI Insights & Analysis",
        
        "forecast_confidence": "Forecast Confidence",
        "trend_analysis": "Trend Analysis", 
        "recommendations": "Recommendations",
        "high_confidence": "High Confidence",
        "confidence_desc": "Current predictions show High Confidence based on historical patterns and trend analysis.",
        "trend_desc": "Demand shows steady growth with seasonal variations. Peak periods align with festival seasons and weekends.",
        "recommendations_desc": "Consider increasing inventory for high-demand items and optimizing staff scheduling based on predicted peaks.",
        
        "average_daily_forecast": "Average Daily Forecast for Next",
        "forecast_report_generated": "Forecast report generated successfully!",
        "no_data_for_report": "No data for report generation",
        "refreshing_from_backend": "Refreshing from backend...",
        
        # ==== HEATMAP ANALYTICS ====
        "interactive_heatmap_analytics_title": "Interactive Heatmap Analytics",
        "heatmap_subtitle": "Real-time Performance Visualization & AI-Powered Business Insights",
        "analysis_controls": "Analysis Controls",
        "date_range": "Date Range",
        "metric_to_analyze": "Metric to Analyze",
        "aggregation_method": "Aggregation Method",
        
        "live_data_overview": "Live Data Overview",
        "total_records": "Total Records",
        "unique_dishes": "Unique Dishes",
        "active_outlets": "Active Outlets",
        "interactive_demand_heatmap": "Interactive Demand Heatmap",
        "performance_analysis": "Performance Analysis",
        
        "top_performing_outlets": "Top Performing Outlets",
        "top_performing_dishes": "Top Performing Dishes",
        "key_insights": "Key Insights",
        "total_demand_volume": "Total Demand Volume",
        "average_daily_demand": "Average Daily Demand",
        "peak_single_demand": "Peak Single Demand",
        "analysis_period": "Analysis Period",
        
        "across_all_outlets": "Across all outlets and dishes",
        "per_dish_per_day": "Per dish per day average",
        "highest_recorded": "Highest recorded demand",
        "data_coverage_span": "Data coverage span",
        
        "ai_business_recommendations": "AI-Powered Business Recommendations",
        "inventory_optimization": "Inventory Optimization",
        "outlet_performance": "Outlet Performance",
        "demand_patterns": "Demand Patterns",
        "staff_optimization": "Staff Optimization",
        
        "export_heatmap_data": "Export Heatmap Data",
        "generate_analytics_report": "Generate Analytics Report",
        "analytics_report_generated": "Analytics report generated successfully!",
        
        # ==== SETTINGS PAGE ====
        "system_settings": "System Settings",
        "settings_subtitle": "Backend Configuration • API Management • System Controls",
        "backend_connection_status": "Backend Connection Status",
        "user_management": "User Management",
        "database_management": "Database Management",
        "api_configuration": "API Configuration",
        "available_api_endpoints": "Available API Endpoints",
        "system_information": "System Information",
        "application_information": "Application Information",
        
        "backend_information": "Backend Information",
        "security_features": "Security Features",
        "backend_architecture": "Backend Architecture",
        "frontend_stack": "Frontend Stack",
        "performance": "Performance",
        
        "production_grade_infrastructure": "Production-grade infrastructure",
        "modern_web_application": "Modern web application",
        "optimized_for_speed": "Optimized for speed",
        
        # ==== ERROR MESSAGES & STATUS ====
        "no_data_available": "No data available",
        "loading_data": "Loading live data from backend...",
        "data_loading_error": "Data loading error",
        "backend_connection_lost": "Backend connection lost",
        "request_timeout": "Request Timeout",
        "connection_error": "Connection Error",
        "no_metrics_available": "No metrics available - Data needed for analysis",
        "no_data_matches_selection": "No data matches current selection",
        "chart_requires_data": "Chart requires data - Visualization will appear after adding data",
        "insights_will_appear": "Insights will appear when data is available",
        
        # ==== LANGUAGE SELECTOR ====
        "language": "Language",
        "select_language": "Select Language",
        "english_lang": "English",
        "telugu_lang": "తెలుగు",
        "hindi_lang": "हिंदी",
    },
    
    # ==== TELUGU TRANSLATIONS ====
    "telugu": {
        # Navigation
        "home": "హోమ్",
        "forecasting_tool": "AI అంచనా",
        "heatmap_analytics": "హీట్‌మ్యాప్ విశ్లేషణ",
        "settings": "సెట్టింగులు",
        "logout": "లాగ్ అవుట్",
        "login": "లాగిన్",
        "register": "రిజిస్టర్",
        
        # Common buttons and actions
        "refresh_data": "డేటా రిఫ్రెష్",
        "export_data": "డేటా ఎక్స్‌పోర్ట్",
        "download_csv": "CSV డౌన్‌లోడ్",
        "generate_report": "రిపోర్ట్ రూపొందించు",
        "seed_database": "డేటాబేస్ సీడ్",
        "test_connection": "కనెక్షన్ టెస్ట్",
        "go_to_home": "హోమ్ పేజీకి వెళ్లు",
        "back_to_home": "హోమ్‌కు తిరిగి",
        "launch": "ప్రారంభించు",
        
        # Status and authentication
        "welcome_back": "తిరిగి స్వాగతం",
        "logged_in_as": "లాగిన్ అయినవారు",
        "session_started": "సెషన్ ప్రారంభం",
        "access_denied": "యాక్సెస్ నిరాకరించబడింది",
        "authentication_required": "ప్రమాణీకరణ అవసరం",
        "connection_verified": "కనెక్షన్ ధృవీకరించబడింది",
        "connection_failed": "కనెక్షన్ విఫలమైంది",
        
        # ==== HOME PAGE ====
        "app_title": "KKCG అనలిటిక్స్ డ్యాష్‌బోర్డ్",
        "app_subtitle": "కోడి కూర చిట్టి గారే కోసం AI-శక్తితో కూడిన రెస్టారెంట్ అనలిటిక్స్",
        "app_description": "లైవ్ బ్యాకెండ్ ఇంటిగ్రేషన్ • రియల్-టైమ్ డేటా • ప్రోఫెషనల్ అనలిటిక్స్",
        
        # Metrics
        "total_demand": "మొత్తం డిమాండ్",
        "average_per_day": "రోజుకు సగటు",
        "peak_demand": "పీక్ డిమాండ్",
        "menu_items": "మెనూ వస్తువులు",
        "steady_growth": "స్థిరమైన వృద్ధి",
        "new_record": "కొత్త రికార్డు",
        "active_dishes": "క్రియాశీల వంటకాలు",
        "vs_last_week": "గత వారంతో పోల్చితే",
        
        # Dashboard sections
        "live_performance_dashboard": "లైవ్ పెర్ఫార్మెన్స్ డ్యాష్‌బోర్డ్",
        "realtime_demand_analytics": "రియల్-టైమ్ డిమాండ్ అనలిటిక్స్",
        "analytics_tools": "అనలిటిక్స్ టూల్స్",
        "platform_benefits": "ప్లాట్‌ఫారమ్ ప్రయోజనాలు",
        "quick_actions": "త్వరిత చర్యలు",
        
        # Tool descriptions
        "ai_demand_forecasting": "AI డిమాండ్ అంచనా",
        "interactive_heatmap_analytics": "ఇంటరాక్టివ్ హీట్‌మ్యాప్ అనలిటిక్స్",
        "forecasting_description": "రియల్ బ్యాకెండ్ డేటాతో అధునాతన మెషిన్ లెర్నింగ్ అంచనా ఇంజిన్. సీజనల్ విశ్లేషణ, కాన్ఫిడెన్స్ ఇంటర్వెల్స్, మరియు ఆప్టిమల్ ఇన్వెంటరీ ప్లానింగ్ కోసం AI-శక్తితో కూడిన అంతర్దృష్టులు.",
        "heatmap_description": "లైవ్ బ్యాకెండ్ డేటా ఇంటిగ్రేషన్‌తో డైనమిక్ హీట్‌మ్యాప్ విజువలైజేషన్. AI-జనరేట్ చేసిన వ్యాపార అంతర్దృష్టులతో వంటకాలు మరియు అవుట్‌లెట్లలో రియల్-టైమ్ పెర్ఫార్మెన్స్ విశ్లేషణ.",
        
        # Benefits
        "boost_revenue": "ఆదాయం పెంచు",
        "reduce_waste": "వ్యర్థాలను తగ్గించు",
        "save_time": "సమయం ఆదా చేయి",
        "cost_control": "ఖర్చు నియంత్రణ",
        "future_ready": "భవిష్యత్తుకు సిద్ధం",
        "data_driven": "డేటా ఆధారిత",
        "competitive_edge": "పోటీ ప్రయోజనం",
        "easy_to_use": "ఉపయోగించడానికి సులభం",
        
        "boost_revenue_desc": "ఆప్టిమైజ్డ్ ఇన్వెంటరీ మరియు డిమాండ్ అంచనాతో అమ్మకాలను 15-25% పెంచండి",
        "reduce_waste_desc": "ఖచ్చితమైన డిమాండ్ అంచనాలు మరియు స్మార్ట్ ప్లానింగ్ ద్వారా ఆహార వ్యర్థాలను 30% తగ్గించండి",
        "save_time_desc": "AI-శక్తితో కూడిన అంతర్దృష్టులు మరియు సిఫార్సులతో 80% ప్లానింగ్ పనులను ఆటోమేట్ చేయండి",
        "cost_control_desc": "సమర్థవంతమైన వనరుల కేటాయింపుతో ఆపరేషనల్ ఖర్చులను 20% తగ్గించండి",
        "future_ready_desc": "7-రోజుల అంచనాలు మరియు సీజనల్ ట్రెండ్ విశ్లేషణతో ముందుండండి",
        "data_driven_desc": "రియల్-టైమ్ అనలిటిక్స్ మరియు అంతర్దృష్టుల మద్దతుతో నమ్మకంగా నిర్ణయాలు తీసుకోండి",
        "competitive_edge_desc": "అధునాతన ML-శక్తితో కూడిన వ్యాపార మేధస్సుతో పోటీదారులను మించిపోండి",
        "easy_to_use_desc": "ఎలాంటి సాంకేతిక నైపుణ్యం అవసరం లేని వినియోగదారు-స్నేహ ఇంటర్‌ఫేస్",
        
        # ==== FORECASTING TOOL ====
        "ai_demand_forecasting_title": "AI డిమాండ్ అంచనా",
        "forecasting_subtitle": "లైవ్ బ్యాకెండ్ ఇంటిగ్రేషన్‌తో అధునాతన మెషిన్ లెర్నింగ్ అంచనాలు",
        "forecasting_controls": "అంచనా నియంత్రణలు",
        "select_dish": "వంటకం ఎంచుకోండి",
        "select_outlet": "అవుట్‌లెట్ ఎంచుకోండి",
        "forecast_horizon": "అంచనా హోరిజన్",
        "all_dishes": "అన్ని వంటకాలు",
        "all_outlets": "అన్ని అవుట్‌లెట్లు",
        "days": "రోజులు",
        
        "performance_metrics": "పెర్ఫార్మెన్స్ మెట్రిక్స్",
        "average_daily": "రోజువారీ సగటు",
        "growth_trend": "వృద్ధి ట్రెండ్",
        "forecast_visualization": "AI-శక్తితో కూడిన అంచనా విజువలైజేషన్",
        "demand_breakdown": "డిమాండ్ విభజన",
        "ai_insights_analysis": "AI అంతర్దృష్టులు & విశ్లేషణ",
        
        "forecast_confidence": "అంచనా విశ్వాసం",
        "trend_analysis": "ట్రెండ్ విశ్లేషణ",
        "recommendations": "సిఫార్సులు",
        "high_confidence": "అధిక విశ్వాసం",
        "confidence_desc": "చారిత్రక నమూనాలు మరియు ట్రెండ్ విశ్లేషణ ఆధారంగా ప్రస్తుత అంచనాలు అధిక విశ్వాసాన్ని చూపుతున్నాయి.",
        "trend_desc": "డిమాండ్ సీజనల్ వైవిధ్యాలతో స్థిరమైన వృద్ధిని చూపుతుంది. పీక్ పీరియడ్స్ పండుగ సీజన్లు మరియు వారాంతాలతో సమలేఖనం చేస్తాయి.",
        "recommendations_desc": "అధిక-డిమాండ్ వస్తువుల కోసం ఇన్వెంటరీని పెంచడం మరియు అంచనా వేసిన పీక్స్ ఆధారంగా స్టాఫ్ షెడ్యూలింగ్‌ను ఆప్టిమైజ్ చేయడాన్ని పరిగణించండి.",
        
        "average_daily_forecast": "తదుపరి రోజులకు రోజువారీ సగటు అంచనా",
        "forecast_report_generated": "అంచనా రిపోర్ట్ విజయవంతంగా రూపొందించబడింది!",
        "no_data_for_report": "రిపోర్ట్ రూపొందింపు కోసం డేటా లేదు",
        "refreshing_from_backend": "బ్యాకెండ్ నుండి రిఫ్రెష్ చేస్తోంది...",
        
        # ==== HEATMAP ANALYTICS ====
        "interactive_heatmap_analytics_title": "ఇంటరాక్టివ్ హీట్‌మ్యాప్ అనలిటిక్స్",
        "heatmap_subtitle": "రియల్-టైమ్ పెర్ఫార్మెన్స్ విజువలైజేషన్ & AI-శక్తితో కూడిన వ్యాపార అంతర్దృష్టులు",
        "analysis_controls": "విశ్లేషణ నియంత్రణలు",
        "date_range": "తేదీ పరిధి",
        "metric_to_analyze": "విశ్లేషించవలసిన మెట్రిక్",
        "aggregation_method": "సమీకరణ పద్ధతి",
        
        "live_data_overview": "లైవ్ డేటా అవలోకనం",
        "total_records": "మొత్తం రికార్డులు",
        "unique_dishes": "ప్రత్యేక వంటకాలు",
        "active_outlets": "క్రియాశీల అవుట్‌లెట్లు",
        "interactive_demand_heatmap": "ఇంటరాక్టివ్ డిమాండ్ హీట్‌మ్యాప్",
        "performance_analysis": "పెర్ఫార్మెన్స్ విశ్లేషణ",
        
        "top_performing_outlets": "అగ్రస్థాన అవుట్‌లెట్లు",
        "top_performing_dishes": "అగ్రస్థాన వంటకాలు",
        "key_insights": "ముఖ్య అంతర్దృష్టులు",
        "total_demand_volume": "మొత్తం డిమాండ్ వాల్యూమ్",
        "average_daily_demand": "రోజువారీ సగటు డిమాండ్",
        "peak_single_demand": "పీక్ సింగిల్ డిమాండ్",
        "analysis_period": "విశ్లేషణ కాలం",
        
        "across_all_outlets": "అన్ని అవుట్‌లెట్లు మరియు వంటకాలలో",
        "per_dish_per_day": "వంటకానికి రోజుకు సగటు",
        "highest_recorded": "అత్యధిక రికార్డ్ చేసిన డిమాండ్",
        "data_coverage_span": "డేటా కవరేజ్ స్పాన్",
        
        "ai_business_recommendations": "AI-శక్తితో కూడిన వ్యాపార సిఫార్సులు",
        "inventory_optimization": "ఇన్వెంటరీ ఆప్టిమైజేషన్",
        "outlet_performance": "అవుట్‌లెట్ పెర్ఫార్మెన్స్",
        "demand_patterns": "డిమాండ్ నమూనాలు",
        "staff_optimization": "స్టాఫ్ ఆప్టిమైజేషన్",
        
        "export_heatmap_data": "హీట్‌మ్యాప్ డేటా ఎక్స్‌పోర్ట్",
        "generate_analytics_report": "అనలిటిక్స్ రిపోర్ట్ రూపొందించు",
        "analytics_report_generated": "అనలిటిక్స్ రిపోర్ట్ విజయవంతంగా రూపొందించబడింది!",
        
        # ==== SETTINGS PAGE ====
        "system_settings": "సిస్టమ్ సెట్టింగులు",
        "settings_subtitle": "బ్యాకెండ్ కాన్ఫిగరేషన్ • API మేనేజ్‌మెంట్ • సిస్టమ్ నియంత్రణలు",
        "backend_connection_status": "బ్యాకెండ్ కనెక్షన్ స్థితి",
        "user_management": "వినియోగదారు నిర్వహణ",
        "database_management": "డేటాబేస్ నిర్వహణ",
        "api_configuration": "API కాన్ఫిగరేషన్",
        "available_api_endpoints": "అందుబాటులో ఉన్న API ఎండ్‌పాయింట్లు",
        "system_information": "సిస్టమ్ సమాచారం",
        "application_information": "అప్లికేషన్ సమాచారం",
        
        "backend_information": "బ్యాకెండ్ సమాచారం",
        "security_features": "భద్రతా లక్షణాలు",
        "backend_architecture": "బ్యాకెండ్ ఆర్కిటెక్చర్",
        "frontend_stack": "ఫ్రంటెండ్ స్టాక్",
        "performance": "పెర్ఫార్మెన్స్",
        
        "production_grade_infrastructure": "ప్రొడక్షన్-గ్రేడ్ ఇన్‌ఫ్రాస్ట్రక్చర్",
        "modern_web_application": "ఆధునిక వెబ్ అప్లికేషన్",
        "optimized_for_speed": "గतి కోసం అనుకూలించబడింది",
        
        # ==== ERROR MESSAGES & STATUS ====
        "no_data_available": "డేటా అందుబాటులో లేదు",
        "loading_data": "బ్యాకెండ్ నుండి లైవ్ డేటా లోడ్ చేస్తోంది...",
        "data_loading_error": "డేటా లోడింగ్ లోపం",
        "backend_connection_lost": "బ్యాకెండ్ కనెక్షన్ కోల్పోయింది",
        "request_timeout": "అభ్యర్థన సమయ ముగింపు",
        "connection_error": "కనెక్షన్ లోపం",
        "no_metrics_available": "మెట్రిక్స్ అందుబాటులో లేవు - విశ్లేషణ కోసం డేటా అవసరం",
        "no_data_matches_selection": "ప్రస్తుత ఎంపికకు డేటా సరిపోలలేదు",
        "chart_requires_data": "చార్ట్‌కు డేటా అవసరం - డేటా జోడించిన తర్వాత విజువలైజేషన్ కనిపిస్తుంది",
        "insights_will_appear": "డేటా అందుబాటులో ఉన్నప్పుడు అంతర్దృష్టులు కనిపిస్తాయి",
        
        # ==== LANGUAGE SELECTOR ====
        "language": "భాష",
        "select_language": "భాష ఎంచుకోండి",
        "english_lang": "English",
        "telugu_lang": "తెలుగు",
        "hindi_lang": "हिंदी",
    },
    
    # ==== HINDI TRANSLATIONS ====
    "hindi": {
        # Navigation
        "home": "होम",
        "forecasting_tool": "AI पूर्वानुमान",
        "heatmap_analytics": "हीटमैप एनालिटिक्स",
        "settings": "सेटिंग्स",
        "logout": "लॉग आउट",
        "login": "लॉगिन",
        "register": "रजिस्टर",
        
        # Common buttons and actions
        "refresh_data": "डेटा रिफ्रेश",
        "export_data": "डेटा एक्सपोर्ट",
        "download_csv": "CSV डाउनलोड",
        "generate_report": "रिपोर्ट बनाएं",
        "seed_database": "डेटाबेस सीड",
        "test_connection": "कनेक्शन टेस्ट",
        "go_to_home": "होम पेज पर जाएं",
        "back_to_home": "होम पर वापस",
        "launch": "शुरू करें",
        
        # Status and authentication
        "welcome_back": "वापस स्वागत है",
        "logged_in_as": "लॉग इन के रूप में",
        "session_started": "सत्र शुरू",
        "access_denied": "पहुंच अस्वीकृत",
        "authentication_required": "प्रमाणीकरण आवश्यक",
        "connection_verified": "कनेक्शन सत्यापित",
        "connection_failed": "कनेक्शन असफल",
        
        # ==== HOME PAGE ====
        "app_title": "KKCG एनालिटिक्स डैशबोर्ड",
        "app_subtitle": "कोडी कूरा चित्ति गारे के लिए AI-संचालित रेस्टोरेंट एनालिटिक्स",
        "app_description": "लाइव बैकएंड इंटीग्रेशन • रियल-टाइम डेटा • प्रोफेशनल एनालिटिक्स",
        
        # Metrics
        "total_demand": "कुल मांग",
        "average_per_day": "प्रति दिन औसत",
        "peak_demand": "चरम मांग",
        "menu_items": "मेनू आइटम",
        "steady_growth": "स्थिर विकास",
        "new_record": "नया रिकॉर्ड",
        "active_dishes": "सक्रिय व्यंजन",
        "vs_last_week": "पिछले सप्ताह की तुलना में",
        
        # Dashboard sections
        "live_performance_dashboard": "लाइव प्रदर्शन डैशबोर्ड",
        "realtime_demand_analytics": "रियल-टाइम मांग एनालिटिक्स",
        "analytics_tools": "एनालिटिक्स टूल्स",
        "platform_benefits": "प्लेटफॉर्म लाभ",
        "quick_actions": "त्वरित कार्य",
        
        # Tool descriptions
        "ai_demand_forecasting": "AI मांग पूर्वानुमान",
        "interactive_heatmap_analytics": "इंटरैक्टिव हीटमैप एनालिटिक्स",
        "forecasting_description": "रियल बैकएंड डेटा के साथ उन्नत मशीन लर्निंग फोरकास्टिंग इंजन। सीज़नल विश्लेषण, कॉन्फिडेंस इंटरवल, और ऑप्टिमल इन्वेंटरी प्लानिंग के लिए AI-संचालित अंतर्दृष्टि।",
        "heatmap_description": "लाइव बैकएंड डेटा इंटीग्रेशन के साथ डायनामिक हीटमैप विज़ुअलाइज़ेशन। AI-जनरेटेड बिजनेस इनसाइट्स के साथ व्यंजनों और आउटलेट्स में रियल-टाइम प्रदर्शन विश्लेषण।",
        
        # Benefits
        "boost_revenue": "राजस्व बढ़ाएं",
        "reduce_waste": "अपशिष्ट कम करें",
        "save_time": "समय बचाएं",
        "cost_control": "लागत नियंत्रण",
        "future_ready": "भविष्य के लिए तैयार",
        "data_driven": "डेटा संचालित",
        "competitive_edge": "प्रतिस्पर्धी बढ़त",
        "easy_to_use": "उपयोग में आसान",
        
        "boost_revenue_desc": "ऑप्टिमाइज़्ड इन्वेंटरी और डिमांड फोरकास्टिंग के साथ बिक्री को 15-25% तक बढ़ाएं",
        "reduce_waste_desc": "सटीक मांग पूर्वानुमान और स्मार्ट प्लानिंग के माध्यम से भोजन की बर्बादी को 30% तक कम करें",
        "save_time_desc": "AI-संचालित अंतर्दृष्टि और सिफारिशों के साथ 80% प्लानिंग कार्यों को स्वचालित करें",
        "cost_control_desc": "कुशल संसाधन आवंटन के साथ परिचालन लागत को 20% तक कम करें",
        "future_ready_desc": "7-दिन के पूर्वानुमान और मौसमी प्रवृत्ति विश्लेषण के साथ आगे रहें",
        "data_driven_desc": "रियल-टाइम एनालिटिक्स और अंतर्दृष्टि द्वारा समर्थित आत्मविश्वास के साथ निर्णय लें",
        "competitive_edge_desc": "उन्नत ML-संचालित बिजनेस इंटेलिजेंस के साथ प्रतिस्पर्धियों से आगे निकलें",
        "easy_to_use_desc": "उपयोगकर्ता-अनुकूल इंटरफेस जिसके लिए किसी तकनीकी विशेषज्ञता की आवश्यकता नहीं",
        
        # ==== FORECASTING TOOL ====
        "ai_demand_forecasting_title": "AI मांग पूर्वानुमान",
        "forecasting_subtitle": "लाइव बैकएंड इंटीग्रेशन के साथ उन्नत मशीन लर्निंग पूर्वानुमान",
        "forecasting_controls": "पूर्वानुमान नियंत्रण",
        "select_dish": "व्यंजन चुनें",
        "select_outlet": "आउटलेट चुनें",
        "forecast_horizon": "पूर्वानुमान क्षितिज",
        "all_dishes": "सभी व्यंजन",
        "all_outlets": "सभी आउटलेट",
        "days": "दिन",
        
        "performance_metrics": "प्रदर्शन मेट्रिक्स",
        "average_daily": "दैनिक औसत",
        "growth_trend": "विकास प्रवृत्ति",
        "forecast_visualization": "AI-संचालित पूर्वानुमान विज़ुअलाइज़ेशन",
        "demand_breakdown": "मांग विभाजन",
        "ai_insights_analysis": "AI अंतर्दृष्टि और विश्लेषण",
        
        "forecast_confidence": "पूर्वानुमान विश्वास",
        "trend_analysis": "प्रवृत्ति विश्लेषण",
        "recommendations": "सिफारिशें",
        "high_confidence": "उच्च विश्वास",
        "confidence_desc": "ऐतिहासिक पैटर्न और प्रवृत्ति विश्लेषण के आधार पर वर्तमान पूर्वानुमान उच्च विश्वास दिखाते हैं।",
        "trend_desc": "मांग मौसमी विविधताओं के साथ स्थिर विकास दिखाती है। चरम अवधि त्योहारी सीज़न और सप्ताहांत के साथ संरेखित होती है।",
        "recommendations_desc": "उच्च-मांग वाली वस्तुओं के लिए इन्वेंटरी बढ़ाने और अनुमानित चरम के आधार पर स्टाफ शेड्यूलिंग को अनुकूलित करने पर विचार करें।",
        
        "average_daily_forecast": "अगले दिनों के लिए दैनिक औसत पूर्वानुमान",
        "forecast_report_generated": "पूर्वानुमान रिपोर्ट सफलतापूर्वक तैयार की गई!",
        "no_data_for_report": "रिपोर्ट तैयार करने के लिए कोई डेटा नहीं",
        "refreshing_from_backend": "बैकएंड से रिफ्रेश कर रहा है...",
        
        # ==== HEATMAP ANALYTICS ====
        "interactive_heatmap_analytics_title": "इंटरैक्टिव हीटमैप एनालिटिक्स",
        "heatmap_subtitle": "रियल-टाइम प्रदर्शन विज़ुअलाइज़ेशन और AI-संचालित बिजनेस इनसाइट्स",
        "analysis_controls": "विश्लेषण नियंत्रण",
        "date_range": "दिनांक सीमा",
        "metric_to_analyze": "विश्लेषण करने का मेट्रिक",
        "aggregation_method": "एकत्रीकरण विधि",
        
        "live_data_overview": "लाइव डेटा अवलोकन",
        "total_records": "कुल रिकॉर्ड",
        "unique_dishes": "अनोखे व्यंजन",
        "active_outlets": "सक्रिय आउटलेट",
        "interactive_demand_heatmap": "इंटरैक्टिव मांग हीटमैप",
        "performance_analysis": "प्रदर्शन विश्लेषण",
        
        "top_performing_outlets": "शीर्ष प्रदर्शन करने वाले आउटलेट",
        "top_performing_dishes": "शीर्ष प्रदर्शन करने वाले व्यंजन",
        "key_insights": "मुख्य अंतर्दृष्टि",
        "total_demand_volume": "कुल मांग मात्रा",
        "average_daily_demand": "दैनिक औसत मांग",
        "peak_single_demand": "चरम एकल मांग",
        "analysis_period": "विश्लेषण अवधि",
        
        "across_all_outlets": "सभी आउटलेट और व्यंजनों में",
        "per_dish_per_day": "प्रति व्यंजन प्रति दिन औसत",
        "highest_recorded": "सर्वोच्च रिकॉर्ड की गई मांग",
        "data_coverage_span": "डेटा कवरेज स्पैन",
        
        "ai_business_recommendations": "AI-संचालित व्यापार सिफारिशें",
        "inventory_optimization": "इन्वेंटरी अनुकूलन",
        "outlet_performance": "आउटलेट प्रदर्शन",
        "demand_patterns": "मांग पैटर्न",
        "staff_optimization": "स्टाफ अनुकूलन",
        
        "export_heatmap_data": "हीटमैप डेटा एक्सपोर्ट",
        "generate_analytics_report": "एनालिटिक्स रिपोर्ट बनाएं",
        "analytics_report_generated": "एनालिटिक्स रिपोर्ट सफलतापूर्वक तैयार की गई!",
        
        # ==== SETTINGS PAGE ====
        "system_settings": "सिस्टम सेटिंग्स",
        "settings_subtitle": "बैकएंड कॉन्फ़िगरेशन • API प्रबंधन • सिस्टम नियंत्रण",
        "backend_connection_status": "बैकएंड कनेक्शन स्थिति",
        "user_management": "उपयोगकर्ता प्रबंधन",
        "database_management": "डेटाबेस प्रबंधन",
        "api_configuration": "API कॉन्फ़िगरेशन",
        "available_api_endpoints": "उपलब्ध API एंडपॉइंट्स",
        "system_information": "सिस्टम जानकारी",
        "application_information": "एप्लिकेशन जानकारी",
        
        "backend_information": "बैकएंड जानकारी",
        "security_features": "सुरक्षा सुविधाएं",
        "backend_architecture": "बैकएंड आर्किटेक्चर",
        "frontend_stack": "फ्रंटएंड स्टैक",
        "performance": "प्रदर्शन",
        
        "production_grade_infrastructure": "प्रोडक्शन-ग्रेड इन्फ्रास्ट्रक्चर",
        "modern_web_application": "आधुनिक वेब एप्लिकेशन",
        "optimized_for_speed": "गति के लिए अनुकूलित",
        
        # ==== ERROR MESSAGES & STATUS ====
        "no_data_available": "कोई डेटा उपलब्ध नहीं",
        "loading_data": "बैकएंड से लाइव डेटा लोड कर रहा है...",
        "data_loading_error": "डेटा लोडिंग त्रुटि",
        "backend_connection_lost": "बैकएंड कनेक्शन खो गया",
        "request_timeout": "अनुरोध समय समाप्त",
        "connection_error": "कनेक्शन त्रुटि",
        "no_metrics_available": "कोई मेट्रिक्स उपलब्ध नहीं - विश्लेषण के लिए डेटा की आवश्यकता",
        "no_data_matches_selection": "वर्तमान चयन से कोई डेटा मेल नहीं खाता",
        "chart_requires_data": "चार्ट के लिए डेटा की आवश्यकता - डेटा जोड़ने के बाद विज़ुअलाइज़ेशन दिखाई देगा",
        "insights_will_appear": "डेटा उपलब्ध होने पर अंतर्दृष्टि दिखाई देगी",
        
        # ==== LANGUAGE SELECTOR ====
        "language": "भाषा",
        "select_language": "भाषा चुनें",
        "english_lang": "English",
        "telugu_lang": "తెలుగు",
        "hindi_lang": "हिंदी",
    }
}

def get_translation(key: str, language: str = None) -> str:
    """
    Get translated text for a given key
    
    Args:
        key: Translation key
        language: Target language (english, telugu, hindi)
    
    Returns:
        Translated text or original key if not found
    """
    # Get language from session state if not provided
    if language is None:
        language = st.session_state.get('selected_language', 'english')
    
    # Normalize language
    language = language.lower()
    
    # Return translation or fall back to English or key itself
    if language in TRANSLATIONS and key in TRANSLATIONS[language]:
        return TRANSLATIONS[language][key]
    elif key in TRANSLATIONS.get('english', {}):
        return TRANSLATIONS['english'][key]
    else:
        # Return key itself as fallback, formatted nicely
        return key.replace('_', ' ').title()

def init_language():
    """Initialize language settings in session state"""
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = 'english'

def create_language_selector():
    """Create language selector component for sidebar"""
    init_language()
    
    # Language options
    language_options = {
        'english': '🇺🇸 English',
        'telugu': '🇮🇳 తెలుగు',
        'hindi': '🇮🇳 हिंदी'
    }
    
    # Get current language
    current_language = st.session_state.get('selected_language', 'english')
    current_index = list(language_options.keys()).index(current_language)
    
    # Create selectbox
    selected_language = st.selectbox(
        label=get_translation("select_language"),
        options=list(language_options.keys()),
        index=current_index,
        format_func=lambda x: language_options[x],
        key="language_selector"
    )
    
    # Update session state if changed
    if selected_language != st.session_state.get('selected_language'):
        st.session_state.selected_language = selected_language
        st.rerun()

def t(key: str) -> str:
    """
    Shorthand function for getting translations
    
    Args:
        key: Translation key
    
    Returns:
        Translated text
    """
    return get_translation(key)

# Export commonly used functions
__all__ = ['get_translation', 't', 'init_language', 'create_language_selector', 'TRANSLATIONS'] 