import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/homerights')
    DB_NAME = 'homerights'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)  # Admin: 2h, User: 24h
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Admin Configuration
    ADMIN_ROLES = ['super_admin', 'content_admin', 'support_admin', 'read_only']
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_DEFAULT = '100/minute'
    RATE_LIMIT_ADMIN = '200/minute'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DB_NAME = 'homerights_test'
