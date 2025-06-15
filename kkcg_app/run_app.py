#!/usr/bin/env python3
"""
KKCG Analytics Dashboard Launcher
Simple script to launch the Streamlit multipage app with error handling
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        import numpy
        import requests
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements with: pip install -r requirements.txt")
        return False

def check_file_structure():
    """Check if all required files exist"""
    required_files = [
        "Home.py",
        "pages/Forecasting_Tool.py", 
        "pages/Heatmap_Comparison.py",
        "utils/__init__.py",
        "utils/data_simulation.py",
        "utils/heatmap_utils.py",
        "utils/insights.py",
        ".streamlit/config.toml",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files are present")
    return True

def launch_app():
    """Launch the Streamlit app"""
    try:
        print("🚀 Launching KKCG Analytics Dashboard...")
        print("📱 The app will open in your default browser at http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the app")
        print("-" * 60)
        
        # Launch Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "Home.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching app: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  App stopped by user")
        return True

def main():
    """Main launcher function"""
    print("🍛 KKCG Analytics Dashboard Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("Home.py").exists():
        print("❌ Please run this script from the kkcg_app directory")
        print("   Current directory:", os.getcwd())
        print("   Expected file: Home.py")
        sys.exit(1)
    
    # Run checks
    if not check_requirements():
        sys.exit(1)
    
    if not check_file_structure():
        sys.exit(1)
    
    print("🎯 All checks passed! Ready to launch...")
    print()
    
    # Launch the app
    launch_app()

if __name__ == "__main__":
    main() 