from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import timedelta
import os
import urllib.parse

load_dotenv()

# Configuración MongoDB con TLS
try:
    mongo_client = MongoClient(
        os.getenv('MONGO_URI'),
        serverSelectionTimeoutMS=5000,
        tls=True,
        tlsAllowInvalidCertificates=False
    )
    # Test the connection
    mongo_client.admin.command('ping')
    print("✓ MongoDB connected successfully!")
except Exception as e:
    print(f"✗ MongoDB connection error: {e}")
    
db = mongo_client['inventory_system']

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Enable CORS
    CORS(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.items import items_bp
    from app.routes.stats import stats_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')
    
    return app
