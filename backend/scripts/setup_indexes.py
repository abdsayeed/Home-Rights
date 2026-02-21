"""
Database index setup script for HomeRights AI
Creates necessary indexes for optimal performance
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT, GEOSPHERE
from app.config import Config

def setup_indexes():
    """Create all necessary database indexes"""
    config = Config()
    client = MongoClient(config.MONGODB_URI)
    db = client[config.DB_NAME]
    
    print("Setting up database indexes...")
    
    # Users collection
    print("- Creating users indexes...")
    db.users.create_index([('email', ASCENDING)], unique=True)
    db.users.create_index([('role', ASCENDING)])
    db.users.create_index([('createdAt', DESCENDING)])
    db.users.create_index([('lastLogin', DESCENDING)])
    
    # Topics collection
    print("- Creating topics indexes...")
    db.topics.create_index([('slug', ASCENDING)], unique=True)
    db.topics.create_index([('category', ASCENDING)])
    db.topics.create_index([('published', ASCENDING)])
    db.topics.create_index([('createdAt', DESCENDING)])
    db.topics.create_index([('metadata.views', DESCENDING)])
    # Full-text search index
    db.topics.create_index([
        ('title', TEXT),
        ('summary', TEXT),
        ('body', TEXT),
        ('tags', TEXT)
    ], name='topic_text_search')
    
    # Support organizations collection
    print("- Creating support_orgs indexes...")
    db.support_orgs.create_index([('name', ASCENDING)])
    db.support_orgs.create_index([('type', ASCENDING)])
    db.support_orgs.create_index([('verificationStatus', ASCENDING)])
    db.support_orgs.create_index([('isAcceptingReferrals', ASCENDING)])
    # Geo-spatial index for location-based search
    db.support_orgs.create_index([('location.coordinates', GEOSPHERE)])
    
    # Documents collection
    print("- Creating documents indexes...")
    db.documents.create_index([('userId', ASCENDING)])
    db.documents.create_index([('uploadedAt', DESCENDING)])
    db.documents.create_index([('analysis.riskLevel', ASCENDING)])
    
    # Chat messages collection
    print("- Creating chat_messages indexes...")
    db.chat_messages.create_index([('userId', ASCENDING)])
    db.chat_messages.create_index([('timestamp', DESCENDING)])
    db.chat_messages.create_index([('sessionId', ASCENDING)])
    
    # Audit logs collection
    print("- Creating audit_logs indexes...")
    db.audit_logs.create_index([('adminId', ASCENDING)])
    db.audit_logs.create_index([('timestamp', DESCENDING)])
    db.audit_logs.create_index([('action', ASCENDING)])
    db.audit_logs.create_index([('targetEntity', ASCENDING)])
    
    # Referrals collection
    print("- Creating referrals indexes...")
    db.referrals.create_index([('orgId', ASCENDING)])
    db.referrals.create_index([('timestamp', DESCENDING)])
    
    print("✓ All indexes created successfully!")
    
    # Print index information
    print("\nIndex Summary:")
    for collection_name in ['users', 'topics', 'support_orgs', 'documents', 'chat_messages', 'audit_logs', 'referrals']:
        indexes = db[collection_name].list_indexes()
        print(f"\n{collection_name}:")
        for idx in indexes:
            print(f"  - {idx['name']}")
    
    client.close()

if __name__ == '__main__':
    setup_indexes()
