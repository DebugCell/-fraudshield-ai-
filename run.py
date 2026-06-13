#!/usr/bin/env python
# ============================================================================
# FraudShield AI - Application Launcher
# ============================================================================
# Simple script to run the Dash application with proper configuration

import os
import sys
import platform
from pathlib import Path

try:
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        'dash', 'plotly', 'pandas', 'numpy', 
        'scikit-learn', 'imblearn', 'dash_bootstrap_components'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing packages:", ", ".join(missing_packages))
        print("\nInstalling missing dependencies...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        print("\n✓ Dependencies installed!")
    else:
        print("✓ All dependencies are installed")


def print_banner():
    """Print application banner."""
    try:
        banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║         🛡️  FraudShield AI - Credit Card Fraud Detection      ║
    ║                                                                ║
    ║          Enterprise Fraud Detection & Risk Analytics          ║
    ║                       v1.0.0                                  ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    except UnicodeEncodeError:
        banner = """
    +----------------------------------------------------------------+
    |                                                                |
    |            FraudShield AI - Credit Card Fraud Detection        |
    |                                                                |
    |          Enterprise Fraud Detection & Risk Analytics          |
    |                       v1.0.0                                  |
    |                                                                |
    +----------------------------------------------------------------+
        """
        print(banner)


def main():
    """Main launcher function."""
    print_banner()
    
    print("\n📦 Checking dependencies...")
    check_dependencies()
    
    print("\n🚀 Starting FraudShield AI Dashboard...")
    print("─" * 65)
    print("📍 Dashboard URL: http://localhost:8050")
    print("🔧 Environment: Development Mode")
    print("⌨️  Press Ctrl+C to stop the server")
    print("─" * 65)
    print()
    
    # Import and run the app
    try:
        from app import app
        
        print("✓ Application loaded successfully\n")
        app.run(
            debug=True,
            host='0.0.0.0',
            port=8050,
            dev_tools_ui=True,
            dev_tools_props_check=True
        )
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
