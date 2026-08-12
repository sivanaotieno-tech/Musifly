#!/usr/bin/env python3
"""
Setup script for Spotify Clone Backend
Run this script to set up the backend environment
"""
import os
import sys
import shutil
from pathlib import Path


def create_env_file():
    """Create .env file from .env.example"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_file.exists():
        print("✓ .env file already exists")
        return
    
    if not env_example.exists():
        print("✗ .env.example not found")
        sys.exit(1)
    
    shutil.copy(env_example, env_file)
    print("✓ Created .env file from .env.example")
    print("  Please edit .env and add your Spotify API credentials")


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python 3.8+ is required (you have {version.major}.{version.minor})")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor} is supported")


def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists('venv'):
        print("✓ Virtual environment already exists")
        return
    
    print("Creating virtual environment...")
    os.system(f"{sys.executable} -m venv venv")
    print("✓ Virtual environment created")
    print("  Activate it with:")
    if sys.platform == 'win32':
        print("    venv\\Scripts\\activate")
    else:
        print("    source venv/bin/activate")


def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    if sys.platform == 'win32':
        pip_cmd = 'venv\\Scripts\\pip'
    else:
        pip_cmd = 'venv/bin/pip'
    
    os.system(f"{pip_cmd} install -r requirements.txt")
    print("✓ Dependencies installed")


def main():
    """Run setup"""
    print("🎵 Spotify Clone Backend Setup\n")
    
    check_python_version()
    create_env_file()
    create_virtual_environment()
    
    print("\n" + "="*50)
    print("Setup complete! ✓")
    print("="*50)
    print("\nNext steps:")
    print("1. Activate virtual environment:")
    if sys.platform == 'win32':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("\n2. Get Spotify API credentials:")
    print("   Visit https://developer.spotify.com/dashboard")
    print("   Create an app and copy the credentials")
    print("\n3. Edit .env file with your credentials")
    print("\n4. Run the backend:")
    print("   python app.py")
    print("\n5. The backend will be available at http://localhost:5000")


if __name__ == '__main__':
    main()
