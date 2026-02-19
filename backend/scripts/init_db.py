"""
Initialize MongoDB database with indexes and sample data
"""
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import os

def init_database():
    # Connect to MongoDB
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/homerights')
    client = MongoClient(mongodb_uri)
    db = client['homerights']
    
    print("Initializing HomeRights AI database...")
    
    # Create indexes
    print("Creating indexes...")
    
    # Users collection
    db.users.create_index([('email', ASCENDING)], unique=True)
    print("✓ Users indexes created")
    
    # Topics collection
    db.topics.create_index([('slug', ASCENDING)], unique=True)
    db.topics.create_index([('category', ASCENDING), ('published', ASCENDING)])
    db.topics.create_index([('tags', ASCENDING)])
    print("✓ Topics indexes created")
    
    # Documents collection
    db.documents.create_index([('userId', ASCENDING), ('createdAt', DESCENDING)])
    print("✓ Documents indexes created")
    
    # Agencies collection
    db.agencies.create_index([('address.postcode', ASCENDING)])
    db.agencies.create_index([('address.coordinates', '2dsphere')])
    print("✓ Agencies indexes created")
    
    # Chat sessions collection
    db.chat_sessions.create_index([('userId', ASCENDING), ('createdAt', DESCENDING)])
    print("✓ Chat sessions indexes created")
    
    # Insert sample topics
    print("\nInserting sample topics...")
    
    sample_topics = [
        {
            'title': 'Understanding Your Tenancy Agreement',
            'slug': 'understanding-tenancy-agreement',
            'category': 'rights',
            'summary': 'Learn about the key components of a tenancy agreement and your rights as a tenant.',
            'body': '''# Understanding Your Tenancy Agreement

A tenancy agreement is a contract between you and your landlord. It sets out the legal terms and conditions of your tenancy.

## Key Points

- Your tenancy agreement should be in writing
- It should clearly state the rent amount and payment dates
- It should specify the length of the tenancy
- Both parties should have a signed copy

## Your Rights

As a tenant, you have the right to:
- Live in a property that's safe and in good repair
- Have your deposit protected in a government-approved scheme
- Be protected from unfair eviction
- Challenge excessive rent increases

## Important Clauses to Check

1. **Rent and payment terms**
2. **Deposit amount and protection**
3. **Repair responsibilities**
4. **Notice periods**
5. **Restrictions on the property use**

Always read your tenancy agreement carefully before signing.''',
            'tags': ['tenancy', 'agreement', 'rights', 'contract'],
            'sources': [
                {
                    'title': 'Gov.uk - Tenancy Agreements',
                    'url': 'https://www.gov.uk/tenancy-agreements-a-guide-for-landlords',
                    'lastChecked': datetime.utcnow()
                }
            ],
            'metadata': {
                'views': 0,
                'saves': 0,
                'avgRating': 0
            },
            'lastUpdated': datetime.utcnow(),
            'createdAt': datetime.utcnow(),
            'published': True
        },
        {
            'title': 'Repairs and Maintenance',
            'slug': 'repairs-and-maintenance',
            'category': 'repairs',
            'summary': 'Understand your landlord\'s responsibilities for repairs and how to report issues.',
            'body': '''# Repairs and Maintenance

Your landlord is responsible for most repairs in your rented home.

## Landlord's Responsibilities

Your landlord must keep in repair:
- The structure and exterior of the property
- Basins, sinks, baths, toilets
- Water and gas pipes, electrical wiring
- Heating and hot water

## How to Report Repairs

1. Report the issue to your landlord in writing
2. Keep a record of all communications
3. Give reasonable access for repairs
4. If urgent, follow up with a phone call

## What if Repairs Aren't Done?

If your landlord doesn't do repairs:
- Contact your local council's environmental health department
- Consider legal action
- You may be able to do repairs and deduct from rent (get legal advice first)

## Emergency Repairs

For emergencies like:
- No heating in winter
- Serious leaks
- No electricity or gas

Contact your landlord immediately and follow up in writing.''',
            'tags': ['repairs', 'maintenance', 'landlord', 'responsibilities'],
            'sources': [
                {
                    'title': 'Shelter - Repairs',
                    'url': 'https://england.shelter.org.uk/housing_advice/repairs',
                    'lastChecked': datetime.utcnow()
                }
            ],
            'metadata': {
                'views': 0,
                'saves': 0,
                'avgRating': 0
            },
            'lastUpdated': datetime.utcnow(),
            'createdAt': datetime.utcnow(),
            'published': True
        },
        {
            'title': 'Deposit Protection',
            'slug': 'deposit-protection',
            'category': 'deposits',
            'summary': 'Learn about deposit protection schemes and how to get your deposit back.',
            'body': '''# Deposit Protection

Your landlord must protect your deposit in a government-approved scheme.

## The Three Schemes

1. **Deposit Protection Service (DPS)**
2. **MyDeposits**
3. **Tenancy Deposit Scheme (TDS)**

## Timeline

Your landlord must:
- Protect your deposit within 30 days of receiving it
- Give you prescribed information about the scheme

## Getting Your Deposit Back

At the end of your tenancy:
- Clean the property thoroughly
- Fix any damage you caused
- Take photos as evidence
- Attend the checkout inspection

## If There's a Dispute

If you disagree with deductions:
- Use the scheme's free dispute resolution service
- Provide evidence (photos, inventory)
- The decision is binding

## Penalties for Non-Protection

If your landlord doesn't protect your deposit:
- You can take them to court
- They may have to pay you 1-3 times the deposit amount
- They cannot serve a Section 21 eviction notice''',
            'tags': ['deposit', 'protection', 'scheme', 'money'],
            'sources': [
                {
                    'title': 'Gov.uk - Tenancy Deposit Protection',
                    'url': 'https://www.gov.uk/tenancy-deposit-protection',
                    'lastChecked': datetime.utcnow()
                }
            ],
            'metadata': {
                'views': 0,
                'saves': 0,
                'avgRating': 0
            },
            'lastUpdated': datetime.utcnow(),
            'createdAt': datetime.utcnow(),
            'published': True
        }
    ]
    
    for topic in sample_topics:
        db.topics.update_one(
            {'slug': topic['slug']},
            {'$setOnInsert': topic},
            upsert=True
        )
    
    print(f"✓ Inserted {len(sample_topics)} sample topics")
    
    # Insert sample agencies
    print("\nInserting sample support agencies...")
    
    sample_agencies = [
        {
            'name': 'Shelter England',
            'type': 'charity',
            'contact': {
                'phone': '0808 800 4444',
                'email': 'info@shelter.org.uk',
                'website': 'https://england.shelter.org.uk'
            },
            'address': {
                'street': '88 Old Street',
                'city': 'London',
                'postcode': 'EC1V 9HU',
                'coordinates': {
                    'lat': 51.5254,
                    'lng': -0.0877
                }
            },
            'services': ['Housing advice', 'Legal support', 'Emergency accommodation'],
            'openingHours': {
                'monday': '8am-8pm',
                'tuesday': '8am-8pm',
                'wednesday': '8am-8pm',
                'thursday': '8am-8pm',
                'friday': '8am-8pm',
                'saturday': '8am-5pm',
                'sunday': '8am-5pm'
            },
            'lastVerified': datetime.utcnow(),
            'createdAt': datetime.utcnow()
        },
        {
            'name': 'Citizens Advice',
            'type': 'advice_center',
            'contact': {
                'phone': '0800 144 8848',
                'email': 'contact@citizensadvice.org.uk',
                'website': 'https://www.citizensadvice.org.uk'
            },
            'address': {
                'street': '3rd Floor North',
                'city': 'London',
                'postcode': 'E14 5HP',
                'coordinates': {
                    'lat': 51.5074,
                    'lng': -0.1278
                }
            },
            'services': ['General advice', 'Housing rights', 'Debt advice', 'Benefits'],
            'openingHours': {
                'monday': '9am-5pm',
                'tuesday': '9am-5pm',
                'wednesday': '9am-5pm',
                'thursday': '9am-5pm',
                'friday': '9am-5pm',
                'saturday': 'Closed',
                'sunday': 'Closed'
            },
            'lastVerified': datetime.utcnow(),
            'createdAt': datetime.utcnow()
        }
    ]
    
    for agency in sample_agencies:
        db.agencies.update_one(
            {'name': agency['name']},
            {'$setOnInsert': agency},
            upsert=True
        )
    
    print(f"✓ Inserted {len(sample_agencies)} sample agencies")
    
    print("\n✅ Database initialization complete!")
    print("\nYou can now:")
    print("1. Start the backend: cd backend && python wsgi.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Register a new user at http://localhost:4200/auth/register")

if __name__ == '__main__':
    init_database()
