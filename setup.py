"""Setup script to verify and prepare Mirror installation."""
import sys
import subprocess

def check_python_version():
    """Check Python version."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def install_dependencies():
    """Install required packages."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def download_nltk_data():
    """Download required NLTK data."""
    print("Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        print("✅ NLTK data downloaded")
        return True
    except Exception as e:
        print(f"⚠️  NLTK data download issue: {e}")
        print("You can download manually later if needed")
        return False

def verify_imports():
    """Verify all imports work."""
    print("Verifying imports...")
    try:
        import streamlit
        import flask
        import pandas
        import textblob
        import vaderSentiment
        import plotly
        print("✅ All core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run setup verification."""
    print("=" * 50)
    print("Mirror Setup Verification")
    print("=" * 50)
    print()
    
    all_ok = True
    
    all_ok &= check_python_version()
    all_ok &= verify_imports()
    
    response = input("\nInstall/update dependencies? (y/n): ")
    if response.lower() == 'y':
        all_ok &= install_dependencies()
    
    response = input("\nDownload NLTK data? (y/n): ")
    if response.lower() == 'y':
        download_nltk_data()
    
    print()
    print("=" * 50)
    if all_ok:
        print("✅ Setup complete! You can now run the application.")
        print("\nTo start:")
        print("  - Run: ./start.sh (Linux/Mac) or start.bat (Windows)")
        print("  - Or manually: cd backend && streamlit run app.py")
    else:
        print("⚠️  Setup completed with some issues. Please review above.")
    print("=" * 50)

if __name__ == "__main__":
    main()

