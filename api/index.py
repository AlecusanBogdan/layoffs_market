"""
Vercel serverless function entry point.
Simply imports and exposes the main Flask app.
"""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Vercel environment flag
os.environ['VERCEL'] = '1'

# Import the Flask app
from app import app, db, init_db

# Initialize database on cold start
with app.app_context():
    init_db()

# Vercel expects 'app' or 'application'
application = app
