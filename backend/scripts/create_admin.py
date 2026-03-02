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

# Add comprehensive topics with proper schema
topics = [
    {
        'title': 'Section 21 Notice - No Fault Eviction',
        'slug': 'section-21-notice',
        'category': 'eviction',
        'summary': 'Understanding Section 21 notices and your rights when facing no-fault eviction',
        'body': 'A Section 21 notice is a legal notice that allows landlords to evict tenants without providing a reason. However, there are strict rules about when and how it can be served. Your landlord must give you at least 2 months notice, and the notice must be in the correct format. The notice cannot be served in the first 4 months of the tenancy. If your deposit is not protected, the landlord cannot serve a valid Section 21 notice.',
        'tags': ['eviction', 'section 21', 'notice', 'tenant rights'],
        'sources': ['Housing Act 1988', 'Deregulation Act 2015'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 245, 'saves': 12, 'helpfulVotes': 34, 'notHelpfulVotes': 2, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Section 8 Notice - Eviction for Breach',
        'slug': 'section-8-notice',
        'category': 'eviction',
        'summary': 'What is a Section 8 notice and grounds for eviction',
        'body': 'A Section 8 notice is used when a landlord wants to evict a tenant for a specific reason, such as rent arrears or antisocial behaviour. There are 17 grounds for eviction, some mandatory and some discretionary. The notice period varies from 2 weeks to 2 months depending on the ground used.',
        'tags': ['eviction', 'section 8', 'rent arrears', 'breach of tenancy'],
        'sources': ['Housing Act 1988'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 178, 'saves': 9, 'helpfulVotes': 25, 'notHelpfulVotes': 1, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Illegal Eviction and Harassment',
        'slug': 'illegal-eviction',
        'category': 'eviction',
        'summary': 'Your rights against illegal eviction and landlord harassment',
        'body': 'It is a criminal offence for a landlord to evict you without following the proper legal process. This includes changing locks, removing your belongings, or threatening you. Harassment such as cutting off utilities or entering without permission is also illegal. You can report this to the police and your local council.',
        'tags': ['illegal eviction', 'harassment', 'criminal offence', 'protection'],
        'sources': ['Protection from Eviction Act 1977'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 203, 'saves': 14, 'helpfulVotes': 31, 'notHelpfulVotes': 2, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Deposit Protection Schemes',
        'slug': 'deposit-protection',
        'category': 'deposits',
        'summary': 'How deposit protection works and what to do if your landlord hasn\'t protected your deposit',
        'body': 'By law, your landlord must protect your deposit in a government-approved scheme within 30 days of receiving it. The three approved schemes are TDS, DPS, and MyDeposits. They must also provide you with prescribed information about the scheme. If they fail to do this, you may be entitled to compensation of 1-3 times the deposit amount.',
        'tags': ['deposits', 'protection', 'TDS', 'DPS', 'MyDeposits'],
        'sources': ['Housing Act 2004'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 189, 'saves': 8, 'helpfulVotes': 28, 'notHelpfulVotes': 1, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Getting Your Deposit Back',
        'slug': 'deposit-return',
        'category': 'deposits',
        'summary': 'How to ensure you get your full deposit back at the end of your tenancy',
        'body': 'To get your deposit back, you should clean the property thoroughly, repair any damage you caused, and take photos as evidence. Your landlord can only make deductions for damage beyond normal wear and tear. If you disagree with deductions, you can use the deposit scheme\'s dispute resolution service for free.',
        'tags': ['deposits', 'end of tenancy', 'cleaning', 'disputes'],
        'sources': [],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 167, 'saves': 11, 'helpfulVotes': 22, 'notHelpfulVotes': 3, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Landlord Repair Responsibilities',
        'slug': 'landlord-repairs',
        'category': 'repairs',
        'summary': 'What repairs your landlord is legally required to carry out and how to enforce them',
        'body': 'Your landlord is responsible for repairs to the structure and exterior of your home, heating and hot water systems, basins, sinks, baths, and toilets. They must carry out repairs within a reasonable time. If they don\'t, you can report them to the council\'s environmental health department or take legal action.',
        'tags': ['repairs', 'maintenance', 'landlord duties', 'housing conditions'],
        'sources': ['Landlord and Tenant Act 1985'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 312, 'saves': 15, 'helpfulVotes': 42, 'notHelpfulVotes': 3, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Damp and Mould in Rental Properties',
        'slug': 'damp-mould',
        'category': 'repairs',
        'summary': 'Dealing with damp and mould issues in your rental home',
        'body': 'Landlords must ensure properties are free from serious damp and mould. If you have damp or mould, report it to your landlord in writing immediately. If they don\'t fix it, contact your local council\'s environmental health team. Serious damp and mould can be a health hazard and may make the property unfit for habitation.',
        'tags': ['damp', 'mould', 'health hazard', 'repairs', 'environmental health'],
        'sources': ['Housing Health and Safety Rating System'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 289, 'saves': 18, 'helpfulVotes': 37, 'notHelpfulVotes': 2, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Rent Increases and Challenges',
        'slug': 'rent-increases',
        'category': 'rent',
        'summary': 'Understanding when and how your landlord can increase rent, and how to challenge unfair increases',
        'body': 'Your landlord can only increase rent if your tenancy agreement allows it, or if you agree to the increase. For assured shorthold tenancies, they must follow specific procedures and give proper notice. You can challenge excessive rent increases through the First-tier Tribunal (Property Chamber).',
        'tags': ['rent', 'rent increase', 'tribunal', 'affordability'],
        'sources': ['Housing Act 1988'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 156, 'saves': 6, 'helpfulVotes': 19, 'notHelpfulVotes': 2, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Rent Arrears - What to Do',
        'slug': 'rent-arrears',
        'category': 'rent',
        'summary': 'Steps to take if you\'re struggling to pay rent',
        'body': 'If you\'re struggling to pay rent, contact your landlord immediately to discuss the situation. You may be able to negotiate a payment plan. Check if you\'re eligible for housing benefit or Universal Credit. Seek advice from Citizens Advice or Shelter. Don\'t ignore the problem as it could lead to eviction.',
        'tags': ['rent arrears', 'payment plan', 'benefits', 'financial difficulty'],
        'sources': [],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 134, 'saves': 10, 'helpfulVotes': 16, 'notHelpfulVotes': 1, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Tenant Rights and Responsibilities',
        'slug': 'tenant-rights',
        'category': 'rights',
        'summary': 'A comprehensive guide to your rights as a tenant in the UK',
        'body': 'As a tenant, you have the right to live in a property that is safe and in good repair. You have the right to be protected from unfair eviction and unfair rent. You also have responsibilities, including paying rent on time, looking after the property, and allowing access for repairs.',
        'tags': ['rights', 'responsibilities', 'tenant law', 'housing act'],
        'sources': ['Housing Act 1988', 'Landlord and Tenant Act 1985'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 423, 'saves': 21, 'helpfulVotes': 56, 'notHelpfulVotes': 4, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Right to Rent Checks',
        'slug': 'right-to-rent',
        'category': 'rights',
        'summary': 'Understanding right to rent checks and your immigration status',
        'body': 'Landlords must check that you have the right to rent in the UK before letting a property to you. You need to provide documents proving your identity and immigration status. This applies to all tenants, including UK citizens. Landlords can face penalties if they rent to someone without the right to rent.',
        'tags': ['right to rent', 'immigration', 'identity checks', 'documentation'],
        'sources': ['Immigration Act 2014'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 98, 'saves': 5, 'helpfulVotes': 12, 'notHelpfulVotes': 1, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Tenancy Agreements Explained',
        'slug': 'tenancy-agreements',
        'category': 'rights',
        'summary': 'Understanding your tenancy agreement and what it means',
        'body': 'A tenancy agreement is a contract between you and your landlord. It sets out your rights and responsibilities. Most private tenants have an assured shorthold tenancy (AST). Read your agreement carefully before signing. Some clauses may be unfair or unenforceable.',
        'tags': ['tenancy agreement', 'contract', 'AST', 'terms and conditions'],
        'sources': [],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 201, 'saves': 13, 'helpfulVotes': 27, 'notHelpfulVotes': 2, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Unfair Terms in Tenancy Agreements',
        'slug': 'unfair-terms',
        'category': 'rights',
        'summary': 'Identifying and challenging unfair clauses in your tenancy agreement',
        'body': 'Some terms in tenancy agreements may be unfair and unenforceable. Examples include clauses that prevent you from having visitors, require you to pay for all repairs, or allow the landlord to enter without notice. Unfair terms are not legally binding.',
        'tags': ['unfair terms', 'contract law', 'consumer rights', 'unenforceable'],
        'sources': ['Consumer Rights Act 2015'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 145, 'saves': 8, 'helpfulVotes': 19, 'notHelpfulVotes': 1, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Energy Performance Certificates (EPC)',
        'slug': 'energy-performance-certificates',
        'category': 'rights',
        'summary': 'What you need to know about EPCs in rental properties',
        'body': 'Landlords must provide an Energy Performance Certificate (EPC) before you rent a property. The property must have a minimum EPC rating of E. If the rating is below E, the landlord cannot legally rent it out unless they have an exemption. EPCs are valid for 10 years.',
        'tags': ['EPC', 'energy efficiency', 'minimum standards', 'regulations'],
        'sources': ['Energy Efficiency Regulations 2015'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 87, 'saves': 4, 'helpfulVotes': 11, 'notHelpfulVotes': 0, 'lastViewed': datetime.utcnow()}
    },
    {
        'title': 'Gas and Electrical Safety',
        'slug': 'gas-electrical-safety',
        'category': 'repairs',
        'summary': 'Your landlord\'s obligations for gas and electrical safety',
        'body': 'Landlords must ensure gas appliances are safe and serviced annually by a Gas Safe registered engineer. They must provide you with a copy of the gas safety certificate. Electrical installations must be inspected every 5 years. Landlords must also ensure electrical appliances they provide are safe.',
        'tags': ['gas safety', 'electrical safety', 'certificates', 'inspections'],
        'sources': ['Gas Safety Regulations 1998', 'Electrical Safety Standards 2020'],
        'published': True,
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {'views': 176, 'saves': 12, 'helpfulVotes': 23, 'notHelpfulVotes': 1, 'lastViewed': datetime.utcnow()}
    }
]

# Clear existing topics and insert new ones
db.topics.delete_many({})
db.topics.insert_many(topics)
print(f"✓ Inserted {len(topics)} topics")

# Add comprehensive UK support organizations with geo-spatial data
support_orgs = [
    # National Organizations
    {
        'name': 'Shelter England',
        'type': 'charity',
        'description': 'Free housing advice and support for people facing homelessness or bad housing',
        'services': ['Emergency housing', 'Legal advice', 'Advocacy', 'Support services', 'Helpline'],
        'contact': {'phone': '0808 800 4444', 'email': 'info@shelter.org.uk', 'website': 'https://england.shelter.org.uk', 'address': '88 Old Street, London, EC1V 9HU'},
        'address': '88 Old Street, London, EC1V 9HU',
        'location': {'coordinates': [-0.0877, 51.5254], 'type': 'Point'},
        'openingHours': {'mon': {'open': '08:00', 'close': '20:00'}, 'tue': {'open': '08:00', 'close': '20:00'}, 'wed': {'open': '08:00', 'close': '20:00'}, 'thu': {'open': '08:00', 'close': '20:00'}, 'fri': {'open': '08:00', 'close': '20:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Citizens Advice',
        'type': 'advice_center',
        'description': 'Free, confidential advice on housing, benefits, debt, and legal issues',
        'services': ['Housing advice', 'Benefits advice', 'Debt advice', 'Legal guidance', 'Consumer rights'],
        'contact': {'phone': '0800 144 8848', 'website': 'https://www.citizensadvice.org.uk', 'address': 'Various locations across the UK'},
        'address': 'Multiple locations',
        'location': {'coordinates': [-0.1278, 51.5074], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Crisis UK',
        'type': 'charity',
        'description': 'National charity for homeless people, providing support and advocacy',
        'services': ['Homelessness support', 'Housing advice', 'Employment support', 'Health services', 'Education'],
        'contact': {'phone': '0800 038 4444', 'email': 'enquiries@crisis.org.uk', 'website': 'https://www.crisis.org.uk', 'address': '66 Commercial Street, London, E1 6LT'},
        'address': '66 Commercial Street, London, E1 6LT',
        'location': {'coordinates': [-0.0719, 51.5176], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Law Centres Network',
        'type': 'legal_aid',
        'description': 'Free legal advice and representation for people who cannot afford a lawyer',
        'services': ['Legal advice', 'Court representation', 'Housing law', 'Welfare benefits', 'Immigration'],
        'contact': {'phone': '020 3637 1330', 'email': 'info@lawcentres.org.uk', 'website': 'https://www.lawcentres.org.uk', 'address': 'Floor 1, Tavis House, 1-6 Tavistock Square, London, WC1H 9NA'},
        'address': 'Tavis House, London, WC1H 9NA',
        'location': {'coordinates': [-0.1301, 51.5246], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:30', 'close': '17:30'}, 'tue': {'open': '09:30', 'close': '17:30'}, 'wed': {'open': '09:30', 'close': '17:30'}, 'thu': {'open': '09:30', 'close': '17:30'}, 'fri': {'open': '09:30', 'close': '17:30'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Housing Ombudsman Service',
        'type': 'council',
        'description': 'Independent service for resolving disputes between tenants and landlords',
        'services': ['Dispute resolution', 'Complaints handling', 'Mediation', 'Investigation'],
        'contact': {'phone': '0300 111 3000', 'email': 'info@housing-ombudsman.org.uk', 'website': 'https://www.housing-ombudsman.org.uk', 'address': 'Exchange Tower, London, E14 9GE'},
        'address': 'Exchange Tower, London, E14 9GE',
        'location': {'coordinates': [-0.0235, 51.5055], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:15', 'close': '17:15'}, 'tue': {'open': '09:15', 'close': '17:15'}, 'wed': {'open': '09:15', 'close': '17:15'}, 'thu': {'open': '09:15', 'close': '17:15'}, 'fri': {'open': '09:15', 'close': '17:15'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    # Additional Organizations
    {
        'name': 'Generation Rent',
        'type': 'charity',
        'description': 'Campaigning organization for private renters in England',
        'services': ['Tenant advocacy', 'Policy campaigns', 'Advice', 'Community organizing'],
        'contact': {'phone': '020 3026 1715', 'email': 'hello@generationrent.org', 'website': 'https://www.generationrent.org', 'address': 'London, UK'},
        'address': 'London, UK',
        'location': {'coordinates': [-0.1278, 51.5074], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Acorn Tenants Union',
        'type': 'charity',
        'description': 'Community union of low-income tenants fighting for housing justice',
        'services': ['Tenant organizing', 'Dispute support', 'Campaigns', 'Community action'],
        'contact': {'email': 'info@acorntheunion.org.uk', 'website': 'https://www.acorntheunion.org.uk', 'address': 'Multiple branches across UK'},
        'address': 'Multiple branches',
        'location': {'coordinates': [-0.1278, 51.5074], 'type': 'Point'},
        'openingHours': {'mon': {'open': '10:00', 'close': '18:00'}, 'tue': {'open': '10:00', 'close': '18:00'}, 'wed': {'open': '10:00', 'close': '18:00'}, 'thu': {'open': '10:00', 'close': '18:00'}, 'fri': {'open': '10:00', 'close': '18:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'StepChange Debt Charity',
        'type': 'charity',
        'description': 'Free debt advice and solutions for people in financial difficulty',
        'services': ['Debt advice', 'Budgeting help', 'Rent arrears support', 'Financial planning'],
        'contact': {'phone': '0800 138 1111', 'website': 'https://www.stepchange.org', 'address': 'Wade House, Merrion Centre, Leeds, LS2 8NG'},
        'address': 'Leeds, LS2 8NG',
        'location': {'coordinates': [-1.5491, 53.8008], 'type': 'Point'},
        'openingHours': {'mon': {'open': '08:00', 'close': '20:00'}, 'tue': {'open': '08:00', 'close': '20:00'}, 'wed': {'open': '08:00', 'close': '20:00'}, 'thu': {'open': '08:00', 'close': '20:00'}, 'fri': {'open': '08:00', 'close': '20:00'}, 'sat': {'open': '08:00', 'close': '16:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'National Debtline',
        'type': 'charity',
        'description': 'Free confidential debt advice service',
        'services': ['Debt advice', 'Rent arrears', 'Eviction prevention', 'Budgeting'],
        'contact': {'phone': '0808 808 4000', 'website': 'https://www.nationaldebtline.org', 'address': 'Tricorn House, Birmingham, B16 8TP'},
        'address': 'Birmingham, B16 8TP',
        'location': {'coordinates': [-1.9026, 52.4862], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '20:00'}, 'tue': {'open': '09:00', 'close': '20:00'}, 'wed': {'open': '09:00', 'close': '20:00'}, 'thu': {'open': '09:00', 'close': '20:00'}, 'fri': {'open': '09:00', 'close': '20:00'}, 'sat': {'open': '09:30', 'close': '13:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Residential Landlords Association (RLA)',
        'type': 'advice_center',
        'description': 'Support and advice for both landlords and tenants on tenancy issues',
        'services': ['Tenancy advice', 'Dispute resolution', 'Legal guidance', 'Documentation'],
        'contact': {'phone': '0161 962 0010', 'website': 'https://www.rla.org.uk', 'address': 'Manchester, M1 2HF'},
        'address': 'Manchester, M1 2HF',
        'location': {'coordinates': [-2.2426, 53.4808], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Centrepoint',
        'type': 'charity',
        'description': 'Youth homelessness charity providing accommodation and support',
        'services': ['Youth housing', 'Support services', 'Life skills', 'Employment help'],
        'contact': {'phone': '0808 800 0661', 'email': 'info@centrepoint.org.uk', 'website': 'https://www.centrepoint.org.uk', 'address': 'Central House, London, EC1V 7HU'},
        'address': 'London, EC1V 7HU',
        'location': {'coordinates': [-0.0877, 51.5254], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'The Trussell Trust',
        'type': 'charity',
        'description': 'Food bank network and poverty relief organization',
        'services': ['Food banks', 'Financial support', 'Advice services', 'Emergency help'],
        'contact': {'phone': '01722 580 180', 'email': 'enquiries@trusselltrust.org', 'website': 'https://www.trusselltrust.org', 'address': 'Salisbury, SP1 1EG'},
        'address': 'Salisbury, SP1 1EG',
        'location': {'coordinates': [-1.7945, 51.0693], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Turn2Us',
        'type': 'charity',
        'description': 'Helps people in financial hardship access welfare benefits and grants',
        'services': ['Benefits calculator', 'Grants search', 'Advice', 'Financial support'],
        'contact': {'phone': '0808 802 2000', 'website': 'https://www.turn2us.org.uk', 'address': 'London, N1 9LH'},
        'address': 'London, N1 9LH',
        'location': {'coordinates': [-0.1022, 51.5387], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Advice UK',
        'type': 'advice_center',
        'description': 'Network of independent advice centers across the UK',
        'services': ['Housing advice', 'Welfare benefits', 'Debt advice', 'Legal support'],
        'contact': {'phone': '020 3510 0790', 'email': 'info@adviceuk.org.uk', 'website': 'https://www.adviceuk.org.uk', 'address': 'London, SE1 7TP'},
        'address': 'London, SE1 7TP',
        'location': {'coordinates': [-0.0877, 51.5024], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
    },
    {
        'name': 'Gingerbread',
        'type': 'charity',
        'description': 'Support for single parent families including housing advice',
        'services': ['Single parent support', 'Housing advice', 'Benefits help', 'Childcare'],
        'contact': {'phone': '0808 802 0925', 'email': 'info@gingerbread.org.uk', 'website': 'https://www.gingerbread.org.uk', 'address': 'London, SE1 7TP'},
        'address': 'London, SE1 7TP',
        'location': {'coordinates': [-0.0877, 51.5024], 'type': 'Point'},
        'openingHours': {'mon': {'open': '09:00', 'close': '17:00'}, 'tue': {'open': '09:00', 'close': '17:00'}, 'wed': {'open': '09:00', 'close': '17:00'}, 'thu': {'open': '09:00', 'close': '17:00'}, 'fri': {'open': '09:00', 'close': '17:00'}},
        'verificationStatus': 'verified', 'lastVerifiedAt': datetime.utcnow(), 'isAcceptingReferrals': True, 'createdAt': datetime.utcnow()
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
