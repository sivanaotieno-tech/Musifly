#!/usr/bin/env python3
"""
Test script to verify backend setup
Run this to check if all dependencies and configuration are correct
"""
import os
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def test_python_version():
    """Test Python version"""
    print_header("Python Version Check")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print("✓ Python version is supported")
    return True


def test_env_file():
    """Test .env file exists"""
    print_header("Environment Configuration")
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("   Create it from .env.example: cp .env.example .env")
        return False
    
    print("✓ .env file exists")
    
    # Load and check for required variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET']
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing.append(var)
            print(f"⚠️  {var}: not configured")
        else:
            print(f"✓ {var}: configured")
    
    if missing:
        print("\n❌ Missing or invalid Spotify credentials")
        return False
    
    return True


def test_dependencies():
    """Test required packages are installed"""
    print_header("Dependencies Check")
    
    dependencies = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'dotenv': 'python-dotenv',
        'spotipy': 'Spotipy',
        'requests': 'Requests'
    }
    
    all_ok = True
    for module_name, display_name in dependencies.items():
        try:
            __import__(module_name)
            print(f"✓ {display_name}")
        except ImportError:
            print(f"❌ {display_name} not installed")
            all_ok = False
    
    if not all_ok:
        print("\nInstall missing packages with: pip install -r requirements.txt")
    
    return all_ok


def test_imports():
    """Test application imports"""
    print_header("Application Import Check")
    
    try:
        from app import app
        print("✓ app.py imports successfully")
    except Exception as e:
        print(f"❌ app.py import error: {e}")
        return False
    
    try:
        from spotify_auth import SpotifyAuthManager
        print("✓ spotify_auth.py imports successfully")
    except Exception as e:
        print(f"❌ spotify_auth.py import error: {e}")
        return False
    
    return True


def test_auth_manager():
    """Test SpotifyAuthManager initialization"""
    print_header("Spotify Auth Manager Check")
    
    try:
        from spotify_auth import SpotifyAuthManager
        auth = SpotifyAuthManager()
        print("✓ SpotifyAuthManager initialized successfully")
        print(f"  Client ID configured: {bool(auth.client_id)}")
        print(f"  Redirect URI: {auth.redirect_uri}")
        return True
    except Exception as e:
        print(f"❌ SpotifyAuthManager initialization error: {e}")
        return False


def test_flask_routes():
    """Test Flask app routes are defined"""
    print_header("Flask Routes Check")
    
    try:
        from app import app
        
        routes = [
            '/api/health',
            '/api/auth/login',
            '/api/auth/callback',
            '/api/auth/logout',
            '/api/auth/token',
            '/api/user/profile',
            '/api/user/top-tracks',
            '/api/user/saved-tracks',
            '/api/search',
            '/api/recommendations'
        ]
        
        app_routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        for route in routes:
            if any(route in str(r) for r in app_routes):
                print(f"✓ {route}")
            else:
                print(f"❌ {route} not found")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Route check error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🎵 " + "="*56)
    print("  SPOTIFY CLONE BACKEND - SETUP VERIFICATION")
    print("=" * 60 + "\n")
    
    tests = [
        ("Python Version", test_python_version),
        ("Environment File", test_env_file),
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Auth Manager", test_auth_manager),
        ("Flask Routes", test_flask_routes)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} check failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓" if result else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All checks passed! Backend is ready to run.")
        print("\nStart the backend with: python app.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
