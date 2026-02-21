from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from datetime import datetime, timedelta
import os

# Initialize logging first
from app.utils.logging_config import setup_logging
setup_logging()

from app.utils.logging_config import get_logger
logger = get_logger('app')

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Disable strict slashes to allow both /api/topics and /api/topics/
    app.url_map.strict_slashes = False
    
    logger.info("Starting application initialization")
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # 24 hours
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # 30 days
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/homerights')
    app.config['DB_NAME'] = 'homerights'
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
    app.config['ML_MODEL_PATH'] = os.getenv('ML_MODEL_PATH', 'ml_models')
    
    # Admin Configuration
    app.config['ADMIN_ROLES'] = ['super_admin', 'content_admin', 'support_admin', 'read_only']
    app.config['DEFAULT_PAGE_SIZE'] = 20
    app.config['MAX_PAGE_SIZE'] = 100
    
    # Initialize extensions
    CORS(app, origins=['http://localhost:4200'])
    jwt = JWTManager(app)
    
    logger.info("Extensions initialized")
    
    # MongoDB connection
    try:
        mongo_client = MongoClient(app.config['MONGODB_URI'])
        app.db = mongo_client[app.config['DB_NAME']]
        logger.info("MongoDB connection established")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}", exc_info=True)
        raise
    
    # Initialize ML Service
    logger.info("Initializing ML Service...")
    from app.services.ml_service import MLService
    try:
        MLService.initialize(model_path=app.config['ML_MODEL_PATH'])
        logger.info("✓ ML Service initialized successfully")
    except Exception as e:
        logger.warning(
            f"ML Service initialization warning: {e}",
            exc_info=True
        )
        logger.info("ML features will use fallback mode")
    
    # Register blueprints
    from app.api import auth, topics, documents, support, chat, admin
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(topics.bp, url_prefix='/api/topics')
    app.register_blueprint(documents.bp, url_prefix='/api/documents')
    app.register_blueprint(support.bp, url_prefix='/api/support')
    app.register_blueprint(chat.bp, url_prefix='/api/chat')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')
    
    logger.info("Blueprints registered")
    
    @app.route('/health')
    def health():
        """Health check endpoint for monitoring"""
        try:
            # Check MongoDB connection
            app.db.command('ping')
            db_status = 'healthy'
        except Exception:
            db_status = 'unhealthy'
        
        # Check ML service
        ml_status = 'initialized' if MLService._initialized else 'fallback'
        
        # Get circuit breaker states
        from app.utils.circuit_breaker import (
            ocr_circuit_breaker,
            ml_circuit_breaker,
            database_circuit_breaker
        )
        
        circuit_breakers = {
            'ocr': ocr_circuit_breaker.get_state(),
            'ml': ml_circuit_breaker.get_state(),
            'database': database_circuit_breaker.get_state()
        }
        
        health_status = {
            'status': 'healthy' if db_status == 'healthy' else 'degraded',
            'database': db_status,
            'ml_service': ml_status,
            'circuit_breakers': circuit_breakers,
            'version': '2.0.0',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        status_code = 200 if health_status['status'] == 'healthy' else 503
        
        logger.info(
            "Health check",
            extra={'health_status': health_status}
        )
        
        return health_status, status_code
    
    @app.route('/metrics')
    def metrics_endpoint():
        """Metrics endpoint for monitoring"""
        from app.utils.metrics import get_all_metrics
        
        metrics_data = get_all_metrics()
        
        return {
            'metrics': metrics_data,
            'timestamp': datetime.utcnow().isoformat()
        }, 200
    
    logger.info("Application initialization complete")
    
    return app
