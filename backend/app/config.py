import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/homerights')
    DB_NAME = 'homerights'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DB_NAME = 'homerights_test'
