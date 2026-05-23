"""
Clean start script - removes .pyc files and starts server
"""
import os
import sys
import shutil
import subprocess

# Remove __pycache__ directories
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        pycache_path = os.path.join(root, '__pycache__')
        print(f"Removing {pycache_path}")
        shutil.rmtree(pycache_path)

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Start the server
print("Starting server...")
subprocess.run([sys.executable, "main.py"])

# Made with Bob
