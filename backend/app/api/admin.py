"""Admin API endpoints"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from ..utils.admin_decorators import require_admin, log_admin_action

bp = Blueprint('admin', __name__, url_prefix='/admin')

# ============================================================================
# DASHBOARD & ANALYTICS
# ============================================================================

@bp.route('/dashboard/overview', methods=['GET'])
@require_admin()
def get_dashboard_overview():
    """Get main dashboard KPIs and metrics"""
    db = current_app.db
    period = request.args.get('period', '7d')
    
    # Calculate date range
    days = int(period.replace('d', ''))
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Total users
    total_users = db.users.count_documents({})
    new_users = db.users.count_documents({'createdAt': {'$gte': start_date}})
    
    # Active users (logged in within period)
    active_users = db.users.count_documents({'lastLogin': {'$gte': start_date}})
    
    # Documents
    total_documents = db.documents.count_documents({})
    new_documents = db.documents.count_documents({'uploadedAt': {'$gte': start_date}})
    
    # Topics
    total_topics = db.topics.count_documents({'published': True})
    topic_views = db.topics.aggregate([
        {'$match': {'metadata.lastViewed': {'$gte': start_date}}},
        {'$group': {'_id': None, 'total': {'$sum': '$metadata.views'}}}
    ])
    topic_views_count = next(topic_views, {}).get('total', 0)
    
    # Support organizations
    total_orgs = db.support_orgs.count_documents({})
    verified_orgs = db.support_orgs.count_documents({'verificationStatus': 'verified'})
    
    # Chat messages
    total_messages = db.chat_messages.count_documents({})
    new_messages = db.chat_messages.count_documents({'timestamp': {'$gte': start_date}})
    
    return jsonify({
        'users': {
            'total': total_users,
            'new': new_users,
            'active': active_users
        },
        'documents': {
            'total': total_documents,
            'new': new_documents
        },
        'topics': {
            'total': total_topics,
            'views': topic_views_count
        },
        'support': {
            'total': total_orgs,
            'verified': verified_orgs
        },
        'chat': {
            'total': total_messages,
            'new': new_messages
        },
        'period': period
    }), 200

# ============================================================================
# USER MANAGEMENT
# ============================================================================

@bp.route('/users', methods=['GET'])
@require_admin()
def list_users():
    """List all users with pagination and filtering"""
    db = current_app.db
    
    # Pagination
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 20)), current_app.config['MAX_PAGE_SIZE'])
    skip = (page - 1) * limit
    
    # Filters
    query = {}
    if request.args.get('role'):
        query['role'] = request.args.get('role')
    if request.args.get('search'):
        search = request.args.get('search')
        query['$or'] = [
            {'email': {'$regex': search, '$options': 'i'}},
            {'profile.firstName': {'$regex': search, '$options': 'i'}},
            {'profile.lastName': {'$regex': search, '$options': 'i'}}
        ]
    
    # Get users
    total = db.users.count_documents(query)
    users = db.users.find(query).sort('createdAt', -1).skip(skip).limit(limit)
    
    result = []
    for user in users:
        result.append({
            'id': str(user['_id']),
            'email': user['email'],
            'firstName': user['profile']['firstName'],
            'lastName': user['profile']['lastName'],
            'role': user['role'],
            'createdAt': user['createdAt'].isoformat(),
            'lastLogin': user.get('lastLogin').isoformat() if user.get('lastLogin') else None
        })
    
    return jsonify({
        'users': result,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit
        }
    }), 200

@bp.route('/users/<user_id>', methods=['GET'])
@require_admin()
def get_user_detail(user_id):
    """Get detailed user information"""
    db = current_app.db
    
    try:
        user = db.users.find_one({'_id': ObjectId(user_id)})
    except:
        return jsonify({'error': 'Invalid user ID'}), 400
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's documents
    documents = list(db.documents.find({'userId': ObjectId(user_id)}).sort('uploadedAt', -1).limit(10))
    
    # Get user's chat sessions
    chat_sessions = db.chat_messages.count_documents({'userId': ObjectId(user_id)})
    
    return jsonify({
        'id': str(user['_id']),
        'email': user['email'],
        'firstName': user['profile']['firstName'],
        'lastName': user['profile']['lastName'],
        'role': user['role'],
        'createdAt': user['createdAt'].isoformat(),
        'lastLogin': user.get('lastLogin').isoformat() if user.get('lastLogin') else None,
        'stats': {
            'documents': len(documents),
            'chatSessions': chat_sessions,
            'savedTopics': len(user.get('savedItems', []))
        }
    }), 200

@bp.route('/users/<user_id>/role', methods=['PATCH'])
@require_admin(['super_admin'])
def update_user_role(user_id):
    """Update user role (super_admin only)"""
    db = current_app.db
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role not in ['user', 'super_admin', 'content_admin', 'support_admin', 'read_only']:
        return jsonify({'error': 'Invalid role'}), 400
    
    try:
        user = db.users.find_one({'_id': ObjectId(user_id)})
    except:
        return jsonify({'error': 'Invalid user ID'}), 400
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    old_role = user.get('role')
    
    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'role': new_role}}
    )
    
    # Log the action
    admin_id = get_jwt_identity()
    admin = db.users.find_one({'_id': ObjectId(admin_id)})
    log_admin_action(
        admin_id=admin_id,
        admin_email=admin['email'],
        action='UPDATE_USER_ROLE',
        ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        target_entity='user',
        target_id=user_id,
        before={'role': old_role},
        after={'role': new_role}
    )
    
    return jsonify({'message': 'User role updated successfully'}), 200

# ============================================================================
# TOPICS MANAGEMENT
# ============================================================================

@bp.route('/topics', methods=['GET'])
@require_admin()
def list_admin_topics():
    """List all topics for admin (including unpublished)"""
    db = current_app.db
    
    # Pagination
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 20)), current_app.config['MAX_PAGE_SIZE'])
    skip = (page - 1) * limit
    
    # Filters
    query = {}
    if request.args.get('category'):
        query['category'] = request.args.get('category')
    if request.args.get('published') is not None:
        query['published'] = request.args.get('published').lower() == 'true'
    
    total = db.topics.count_documents(query)
    topics = db.topics.find(query).sort('createdAt', -1).skip(skip).limit(limit)
    
    result = []
    for topic in topics:
        result.append({
            'id': str(topic['_id']),
            'title': topic['title'],
            'slug': topic['slug'],
            'category': topic['category'],
            'published': topic.get('published', False),
            'views': topic.get('metadata', {}).get('views', 0),
            'createdAt': topic['createdAt'].isoformat(),
            'lastUpdated': topic.get('lastUpdated', topic['createdAt']).isoformat()
        })
    
    return jsonify({
        'topics': result,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit
        }
    }), 200

@bp.route('/topics', methods=['POST'])
@require_admin(['super_admin', 'content_admin'])
def create_topic():
    """Create a new topic"""
    db = current_app.db
    data = request.get_json()
    
    # Validate required fields
    required = ['title', 'slug', 'category', 'summary', 'body']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if slug already exists
    if db.topics.find_one({'slug': data['slug']}):
        return jsonify({'error': 'Slug already exists'}), 400
    
    admin_id = get_jwt_identity()
    
    topic = {
        'title': data['title'],
        'slug': data['slug'],
        'category': data['category'],
        'summary': data['summary'],
        'body': data['body'],
        'tags': data.get('tags', []),
        'sources': data.get('sources', []),
        'published': data.get('published', False),
        'createdBy': ObjectId(admin_id),
        'createdAt': datetime.utcnow(),
        'lastUpdated': datetime.utcnow(),
        'metadata': {
            'views': 0,
            'saves': 0,
            'helpfulVotes': 0,
            'notHelpfulVotes': 0
        }
    }
    
    result = db.topics.insert_one(topic)
    
    return jsonify({
        'id': str(result.inserted_id),
        'message': 'Topic created successfully'
    }), 201

@bp.route('/topics/<topic_id>', methods=['PUT'])
@require_admin(['super_admin', 'content_admin'])
def update_topic(topic_id):
    """Update an existing topic"""
    db = current_app.db
    data = request.get_json()
    
    try:
        topic = db.topics.find_one({'_id': ObjectId(topic_id)})
    except:
        return jsonify({'error': 'Invalid topic ID'}), 400
    
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    # Update fields
    update_data = {
        'lastUpdated': datetime.utcnow()
    }
    
    if 'title' in data:
        update_data['title'] = data['title']
    if 'summary' in data:
        update_data['summary'] = data['summary']
    if 'body' in data:
        update_data['body'] = data['body']
    if 'category' in data:
        update_data['category'] = data['category']
    if 'tags' in data:
        update_data['tags'] = data['tags']
    if 'sources' in data:
        update_data['sources'] = data['sources']
    if 'published' in data:
        update_data['published'] = data['published']
    
    db.topics.update_one(
        {'_id': ObjectId(topic_id)},
        {'$set': update_data}
    )
    
    return jsonify({'message': 'Topic updated successfully'}), 200

@bp.route('/topics/<topic_id>', methods=['DELETE'])
@require_admin(['super_admin', 'content_admin'])
def delete_topic(topic_id):
    """Delete a topic"""
    db = current_app.db
    
    try:
        result = db.topics.delete_one({'_id': ObjectId(topic_id)})
    except:
        return jsonify({'error': 'Invalid topic ID'}), 400
    
    if result.deleted_count == 0:
        return jsonify({'error': 'Topic not found'}), 404
    
    return jsonify({'message': 'Topic deleted successfully'}), 200

# ============================================================================
# SUPPORT ORGANIZATIONS MANAGEMENT
# ============================================================================

@bp.route('/support', methods=['GET'])
@require_admin()
def list_admin_support_orgs():
    """List all support organizations for admin"""
    db = current_app.db
    
    # Pagination
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 20)), current_app.config['MAX_PAGE_SIZE'])
    skip = (page - 1) * limit
    
    # Filters
    query = {}
    if request.args.get('type'):
        query['type'] = request.args.get('type')
    if request.args.get('verificationStatus'):
        query['verificationStatus'] = request.args.get('verificationStatus')
    
    total = db.support_orgs.count_documents(query)
    orgs = db.support_orgs.find(query).sort('name', 1).skip(skip).limit(limit)
    
    result = []
    for org in orgs:
        result.append({
            'id': str(org['_id']),
            'name': org['name'],
            'type': org['type'],
            'verificationStatus': org.get('verificationStatus', 'unverified'),
            'lastVerifiedAt': org.get('lastVerifiedAt').isoformat() if org.get('lastVerifiedAt') else None,
            'isAcceptingReferrals': org.get('isAcceptingReferrals', True),
            'createdAt': org.get('createdAt', datetime.utcnow()).isoformat()
        })
    
    return jsonify({
        'organizations': result,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit
        }
    }), 200

@bp.route('/support', methods=['POST'])
@require_admin(['super_admin', 'support_admin'])
def create_support_org():
    """Create a new support organization"""
    db = current_app.db
    data = request.get_json()
    
    required = ['name', 'type', 'contact']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    admin_id = get_jwt_identity()
    
    org = {
        'name': data['name'],
        'type': data['type'],
        'description': data.get('description', ''),
        'services': data.get('services', []),
        'contact': data['contact'],
        'address': data.get('address', ''),
        'location': data.get('location', {}),
        'openingHours': data.get('openingHours', {}),
        'verificationStatus': 'unverified',
        'isAcceptingReferrals': data.get('isAcceptingReferrals', True),
        'createdBy': ObjectId(admin_id),
        'createdAt': datetime.utcnow()
    }
    
    result = db.support_orgs.insert_one(org)
    
    return jsonify({
        'id': str(result.inserted_id),
        'message': 'Organization created successfully'
    }), 201

@bp.route('/support/<org_id>', methods=['PUT'])
@require_admin(['super_admin', 'support_admin'])
def update_support_org(org_id):
    """Update a support organization"""
    db = current_app.db
    data = request.get_json()
    
    try:
        org = db.support_orgs.find_one({'_id': ObjectId(org_id)})
    except:
        return jsonify({'error': 'Invalid organization ID'}), 400
    
    if not org:
        return jsonify({'error': 'Organization not found'}), 404
    
    # Update fields
    update_data = {}
    allowed_fields = ['name', 'type', 'description', 'services', 'contact', 'address', 'location', 'openingHours', 'isAcceptingReferrals']
    
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]
    
    if update_data:
        db.support_orgs.update_one(
            {'_id': ObjectId(org_id)},
            {'$set': update_data}
        )
    
    return jsonify({'message': 'Organization updated successfully'}), 200

@bp.route('/support/<org_id>/verify', methods=['POST'])
@require_admin(['super_admin', 'support_admin'])
def verify_support_org(org_id):
    """Verify a support organization"""
    db = current_app.db
    
    try:
        org = db.support_orgs.find_one({'_id': ObjectId(org_id)})
    except:
        return jsonify({'error': 'Invalid organization ID'}), 400
    
    if not org:
        return jsonify({'error': 'Organization not found'}), 404
    
    admin_id = get_jwt_identity()
    
    db.support_orgs.update_one(
        {'_id': ObjectId(org_id)},
        {
            '$set': {
                'verificationStatus': 'verified',
                'lastVerifiedAt': datetime.utcnow(),
                'verifiedBy': ObjectId(admin_id)
            }
        }
    )
    
    return jsonify({'message': 'Organization verified successfully'}), 200

@bp.route('/support/<org_id>', methods=['DELETE'])
@require_admin(['super_admin', 'support_admin'])
def delete_support_org(org_id):
    """Delete a support organization"""
    db = current_app.db
    
    try:
        result = db.support_orgs.delete_one({'_id': ObjectId(org_id)})
    except:
        return jsonify({'error': 'Invalid organization ID'}), 400
    
    if result.deleted_count == 0:
        return jsonify({'error': 'Organization not found'}), 404
    
    return jsonify({'message': 'Organization deleted successfully'}), 200

# ============================================================================
# AUDIT LOGS
# ============================================================================

@bp.route('/audit-logs', methods=['GET'])
@require_admin(['super_admin'])
def get_audit_logs():
    """Get audit logs (super_admin only)"""
    db = current_app.db
    
    # Pagination
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 50)), 100)
    skip = (page - 1) * limit
    
    # Filters
    query = {}
    if request.args.get('adminId'):
        try:
            query['adminId'] = ObjectId(request.args.get('adminId'))
        except:
            pass
    if request.args.get('action'):
        query['action'] = {'$regex': request.args.get('action'), '$options': 'i'}
    
    total = db.audit_logs.count_documents(query)
    logs = db.audit_logs.find(query).sort('timestamp', -1).skip(skip).limit(limit)
    
    result = []
    for log in logs:
        result.append({
            'id': str(log['_id']),
            'adminEmail': log['adminEmail'],
            'action': log['action'],
            'targetEntity': log.get('targetEntity'),
            'targetId': log.get('targetId'),
            'ip': log['ip'],
            'timestamp': log['timestamp'].isoformat()
        })
    
    return jsonify({
        'logs': result,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit
        }
    }), 200
