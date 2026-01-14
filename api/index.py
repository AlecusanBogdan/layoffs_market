import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, init_db

# Initialize database on cold start
with app.app_context():
    init_db()

# Vercel expects the app to be named 'app' or 'application'
application = app

# For local testing
if __name__ == "__main__":
    app.run(debug=True)

