"""Create admin user and seed data for HomeRights AI"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['homerights']

print("Creating admin user and seed data...")

# Create admin user
admin_email = 'admin@homerights.ai'
existing_admin = db.users.find_one({'email': admin_email})

if existing_admin:
    print(f"✓ Admin user already exists: {admin_email}")
    # Update to ensure it has admin role
    db.users.update_one(
        {'email': admin_email},
        {'$set': {'role': 'super_admin'}}
    )
    print("✓ Updated admin role to super_admin")
else:
    admin_user = {
        'email': admin_email,
        'passwordHash': generate_password_hash('Admin123!'),
        'role': 'super_admin',
        'profile': {
            'firstName': 'Admin',
            'lastName': 'User'
        },
        'savedItems': [],
        'createdAt': datetime.utcnow(),
        'lastLogin': None
    }
    db.users.insert_one(admin_user)
    print(f"✓ Created admin user: {admin_email} / Admin123!")

# Add sample topics with proper schema
topics = [
    {
        'title': 'Section 21 Notice - No Fault Eviction',
        'slug': 'section-21-notice',
        'category': 'eviction',
        'summary': 'Understanding Section 21 notices and your rights when facing no-fault eviction',
        'body': 'A Section 21 notice is a legal notice that allows landlords to evict tenants without providing a reason. However, there are strict rules about when and how it can be served. Your landlord must give you at least 2 months notice, and the notice must be in the correct format.',
        'tags': ['eviction', 'section 21', 'notice', 'tenant rights'],
        'sources': [],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {
            'views': 245,
            'saves': 12,
            'helpfulVotes': 34,
            'notHelpfulVotes': 2,
            'lastViewed': datetime.utcnow()
        }
    },
    {
        'title': 'Deposit Protection Schemes',
        'slug': 'deposit-protection',
        'category': 'deposits',
        'summary': 'How deposit protection works and what to do if your landlord hasn\'t protected your deposit',
        'body': 'By law, your landlord must protect your deposit in a government-approved scheme within 30 days of receiving it. They must also provide you with prescribed information about the scheme. If they fail to do this, you may be entitled to compensation.',
        'tags': ['deposits', 'protection', 'TDS', 'DPS', 'MyDeposits'],
        'sources': [],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {
            'views': 189,
            'saves': 8,
            'helpfulVotes': 28,
            'notHelpfulVotes': 1,
            'lastViewed': datetime.utcnow()
        }
    },
    {
        'title': 'Landlord Repair Responsibilities',
        'slug': 'landlord-repairs',
        'category': 'repairs',
        'summary': 'What repairs your landlord is legally required to carry out and how to enforce them',
        'body': 'Your landlord is responsible for most repairs to the structure and exterior of your home, as well as heating and hot water systems. They must carry out repairs within a reasonable time. If they don\'t, you can report them to the council or take legal action.',
        'tags': ['repairs', 'maintenance', 'landlord duties', 'housing conditions'],
        'sources': [],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {
            'views': 312,
            'saves': 15,
            'helpfulVotes': 42,
            'notHelpfulVotes': 3,
            'lastViewed': datetime.utcnow()
        }
    },
    {
        'title': 'Rent Increases and Challenges',
        'slug': 'rent-increases',
        'category': 'rent',
        'summary': 'Understanding when and how your landlord can increase rent, and how to challenge unfair increases',
        'body': 'Your landlord can only increase rent if your tenancy agreement allows it, or if you agree to the increase. For assured shorthold tenancies, they must follow specific procedures. You can challenge excessive rent increases through the First-tier Tribunal.',
        'tags': ['rent', 'rent increase', 'tribunal', 'affordability'],
        'sources': [],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {
            'views': 156,
            'saves': 6,
            'helpfulVotes': 19,
            'notHelpfulVotes': 2,
            'lastViewed': datetime.utcnow()
        }
    },
    {
        'title': 'Tenant Rights and Responsibilities',
        'slug': 'tenant-rights',
        'category': 'rights',
        'summary': 'A comprehensive guide to your rights as a tenant in the UK',
        'body': 'As a tenant, you have the right to live in a property that is safe and in good repair. You have the right to be protected from unfair eviction and unfair rent. You also have responsibilities, including paying rent on time and looking after the property.',
        'tags': ['rights', 'responsibilities', 'tenant law', 'housing act'],
        'sources': [],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {
            'views': 423,
            'saves': 21,
            'helpfulVotes': 56,
            'notHelpfulVotes': 4,
            'lastViewed': datetime.utcnow()
        }
    }
]

# Clear existing topics and insert new ones
db.topics.delete_many({})
db.topics.insert_many(topics)
print(f"✓ Inserted {len(topics)} topics")

# Add sample support organizations with geo-spatial data
support_orgs = [
    {
        'name': 'Shelter England',
        'type': 'charity',
        'description': 'Free housing advice and support for people facing homelessness or bad housing',
        'services': ['Emergency housing', 'Legal advice', 'Advocacy', 'Support services'],
        'contact': {
            'phone': '0808 800 4444',
            'email': 'info@shelter.org.uk',
            'website': 'https://england.shelter.org.uk',
            'address': '88 Old Street, London, EC1V 9HU'
        },
        'address': '88 Old Street, London, EC1V 9HU',
        'location': {
            'coordinates': [-0.0877, 51.5254],  # [longitude, latitude] for London
            'type': 'Point'
        },
        'openingHours': {
            'mon': {'open': '08:00', 'close': '20:00'},
            'tue': {'open': '08:00', 'close': '20:00'},
            'wed': {'open': '08:00', 'close': '20:00'},
            'thu': {'open': '08:00', 'close': '20:00'},
            'fri': {'open': '08:00', 'close': '20:00'}
        },
        'verificationStatus': 'verified',
        'lastVerifiedAt': datetime.utcnow(),
        'isAcceptingReferrals': True,
        'createdAt': datetime.utcnow()
    },
    {
        'name': 'Citizens Advice',
        'type': 'advice_center',
        'description': 'Free, confidential advice on housing, benefits, debt, and legal issues',
        'services': ['Housing advice', 'Benefits advice', 'Debt advice', 'Legal guidance'],
        'contact': {
            'phone': '0800 144 8848',
            'website': 'https://www.citizensadvice.org.uk',
            'address': 'Various locations across the UK'
        },
        'address': 'Multiple locations',
        'location': {
            'coordinates': [-0.1278, 51.5074],  # Central London
            'type': 'Point'
        },
        'openingHours': {
            'mon': {'open': '09:00', 'close': '17:00'},
            'tue': {'open': '09:00', 'close': '17:00'},
            'wed': {'open': '09:00', 'close': '17:00'},
            'thu': {'open': '09:00', 'close': '17:00'},
            'fri': {'open': '09:00', 'close': '17:00'}
        },
        'verificationStatus': 'verified',
        'lastVerifiedAt': datetime.utcnow(),
        'isAcceptingReferrals': True,
        'createdAt': datetime.utcnow()
    },
    {
        'name': 'Crisis UK',
        'type': 'charity',
        'description': 'National charity for homeless people, providing support and advocacy',
        'services': ['Homelessness support', 'Housing advice', 'Employment support', 'Health services'],
        'contact': {
            'phone': '0800 038 4444',
            'email': 'enquiries@crisis.org.uk',
            'website': 'https://www.crisis.org.uk',
            'address': '66 Commercial Street, London, E1 6LT'
        },
        'address': '66 Commercial Street, London, E1 6LT',
        'location': {
            'coordinates': [-0.0719, 51.5176],
            'type': 'Point'
        },
        'openingHours': {
            'mon': {'open': '09:00', 'close': '17:00'},
            'tue': {'open': '09:00', 'close': '17:00'},
            'wed': {'open': '09:00', 'close': '17:00'},
            'thu': {'open': '09:00', 'close': '17:00'},
            'fri': {'open': '09:00', 'close': '17:00'}
        },
        'verificationStatus': 'verified',
        'lastVerifiedAt': datetime.utcnow(),
        'isAcceptingReferrals': True,
        'createdAt': datetime.utcnow()
    },
    {
        'name': 'Law Centres Network',
        'type': 'legal_aid',
        'description': 'Free legal advice and representation for people who cannot afford a lawyer',
        'services': ['Legal advice', 'Court representation', 'Housing law', 'Welfare benefits'],
        'contact': {
            'phone': '020 3637 1330',
            'email': 'info@lawcentres.org.uk',
            'website': 'https://www.lawcentres.org.uk',
            'address': 'Floor 1, Tavis House, 1-6 Tavistock Square, London, WC1H 9NA'
        },
        'address': 'Tavis House, London, WC1H 9NA',
        'location': {
            'coordinates': [-0.1301, 51.5246],
            'type': 'Point'
        },
        'openingHours': {
            'mon': {'open': '09:30', 'close': '17:30'},
            'tue': {'open': '09:30', 'close': '17:30'},
            'wed': {'open': '09:30', 'close': '17:30'},
            'thu': {'open': '09:30', 'close': '17:30'},
            'fri': {'open': '09:30', 'close': '17:30'}
        },
        'verificationStatus': 'verified',
        'lastVerifiedAt': datetime.utcnow(),
        'isAcceptingReferrals': True,
        'createdAt': datetime.utcnow()
    },
    {
        'name': 'Housing Ombudsman Service',
        'type': 'council',
        'description': 'Independent service for resolving disputes between tenants and landlords',
        'services': ['Dispute resolution', 'Complaints handling', 'Mediation', 'Investigation'],
        'contact': {
            'phone': '0300 111 3000',
            'email': 'info@housing-ombudsman.org.uk',
            'website': 'https://www.housing-ombudsman.org.uk',
            'address': 'Exchange Tower, London, E14 9GE'
        },
        'address': 'Exchange Tower, London, E14 9GE',
        'location': {
            'coordinates': [-0.0235, 51.5055],
            'type': 'Point'
        },
        'openingHours': {
            'mon': {'open': '09:15', 'close': '17:15'},
            'tue': {'open': '09:15', 'close': '17:15'},
            'wed': {'open': '09:15', 'close': '17:15'},
            'thu': {'open': '09:15', 'close': '17:15'},
            'fri': {'open': '09:15', 'close': '17:15'}
        },
        'verificationStatus': 'verified',
        'lastVerifiedAt': datetime.utcnow(),
        'isAcceptingReferrals': True,
        'createdAt': datetime.utcnow()
    }
]

# Clear existing support_orgs and insert new ones
db.support_orgs.delete_many({})
db.support_orgs.insert_many(support_orgs)
print(f"✓ Inserted {len(support_orgs)} support organizations")

print("\n✅ Setup complete!")
print("\nAdmin Login:")
print(f"  Email: {admin_email}")
print("  Password: Admin123!")
print("\nYou can now:")
print("  1. Login at http://localhost:4200/auth/login")
print("  2. Access admin dashboard at http://localhost:4200/admin")
print("  3. Browse topics at http://localhost:4200/topics")
print("  4. Find support at http://localhost:4200/support")

client.close()
