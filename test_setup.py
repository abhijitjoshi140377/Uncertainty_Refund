"""
Quick setup verification script
"""

import sys
import subprocess

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing Python package imports...")
    
    packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'numpy',
        'pandas',
        'sklearn',
    ]
    
    failed = []
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            failed.append(package)
    
    if failed:
        print(f"\n❌ Failed to import: {', '.join(failed)}")
        return False
    else:
        print("\n✅ All packages imported successfully!")
        return True

def check_node():
    """Check if Node.js is available"""
    print("\nChecking Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"✓ Node.js version: {result.stdout.strip()}")
        return True
    except:
        print("✗ Node.js not found")
        return False

def check_npm():
    """Check if npm is available"""
    print("\nChecking npm...")
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        print(f"✓ npm version: {result.stdout.strip()}")
        return True
    except:
        print("✗ npm not found")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Setup Verification Test")
    print("=" * 50)
    
    python_ok = test_imports()
    node_ok = check_node()
    npm_ok = check_npm()
    
    print("\n" + "=" * 50)
    if python_ok and node_ok and npm_ok:
        print("✅ Setup verification PASSED!")
        print("=" * 50)
        sys.exit(0)
    else:
        print("❌ Setup verification FAILED!")
        print("=" * 50)
        sys.exit(1)

# Made with Bob
