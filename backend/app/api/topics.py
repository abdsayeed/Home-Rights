from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId

bp = Blueprint('topics', __name__)

@bp.route('/', methods=['GET'])
def list_topics():
    db = current_app.db
    
    # Pagination
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 20)), 100)
    skip = (page - 1) * limit
    
    # Filters
    query = {'published': True}
    
    if request.args.get('category'):
        query['category'] = request.args.get('category')
    
    # Search functionality
    if request.args.get('search'):
        search_term = request.args.get('search')
        query['$or'] = [
            {'title': {'$regex': search_term, '$options': 'i'}},
            {'summary': {'$regex': search_term, '$options': 'i'}},
            {'body': {'$regex': search_term, '$options': 'i'}},
            {'tags': {'$regex': search_term, '$options': 'i'}}
        ]
    
    # Sorting
    sort_by = request.args.get('sort', 'title')
    sort_order = -1 if request.args.get('order') == 'desc' else 1
    
    if sort_by == 'views':
        sort_field = 'metadata.views'
    elif sort_by == 'date':
        sort_field = 'createdAt'
    else:
        sort_field = 'title'
    
    # Get total count
    total = db.topics.count_documents(query)
    
    # Get topics
    topics = db.topics.find(query).sort(sort_field, sort_order).skip(skip).limit(limit)
    
    result = []
    for topic in topics:
        result.append({
            'id': str(topic['_id']),
            'title': topic['title'],
            'slug': topic['slug'],
            'category': topic['category'],
            'summary': topic['summary'],
            'tags': topic.get('tags', []),
            'views': topic.get('metadata', {}).get('views', 0)
        })
    
    return jsonify({
        'topics': result,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit,
            'hasNext': page * limit < total,
            'hasPrev': page > 1
        }
    }), 200

@bp.route('/<slug>', methods=['GET'])
def get_topic(slug):
    db = current_app.db
    topic = db.topics.find_one({'slug': slug, 'published': True})
    
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    # Increment view count
    db.topics.update_one(
        {'_id': topic['_id']},
        {'$inc': {'metadata.views': 1}}
    )
    
    return jsonify({
        'id': str(topic['_id']),
        'title': topic['title'],
        'slug': topic['slug'],
        'category': topic['category'],
        'summary': topic['summary'],
        'body': topic['body'],
        'tags': topic.get('tags', []),
        'sources': topic.get('sources', []),
        'lastUpdated': topic.get('lastUpdated', topic['createdAt']).isoformat()
    }), 200

@bp.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({
        'categories': [
            {'value': 'repairs', 'label': 'Repairs & Maintenance'},
            {'value': 'deposits', 'label': 'Deposits'},
            {'value': 'eviction', 'label': 'Eviction & Notices'},
            {'value': 'rent', 'label': 'Rent & Payments'},
            {'value': 'rights', 'label': 'Tenant Rights'}
        ]
    }), 200

@bp.route('/<topic_id>/save', methods=['POST'])
@jwt_required()
def save_topic(topic_id):
    user_id = get_jwt_identity()
    db = current_app.db
    
    try:
        topic_obj_id = ObjectId(topic_id)
    except:
        return jsonify({'error': 'Invalid topic ID'}), 400
    
    topic = db.topics.find_one({'_id': topic_obj_id})
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$addToSet': {'savedItems': topic_obj_id}}
    )
    
    db.topics.update_one(
        {'_id': topic_obj_id},
        {'$inc': {'metadata.saves': 1}}
    )
    
    return jsonify({'message': 'Topic saved successfully'}), 200

@bp.route('/<topic_id>/unsave', methods=['POST'])
@jwt_required()
def unsave_topic(topic_id):
    user_id = get_jwt_identity()
    db = current_app.db
    
    try:
        topic_obj_id = ObjectId(topic_id)
    except:
        return jsonify({'error': 'Invalid topic ID'}), 400
    
    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$pull': {'savedItems': topic_obj_id}}
    )
    
    db.topics.update_one(
        {'_id': topic_obj_id},
        {'$inc': {'metadata.saves': -1}}
    )
    
    return jsonify({'message': 'Topic unsaved successfully'}), 200


@bp.route('/<topic_id>/feedback', methods=['POST'])
@jwt_required()
def submit_feedback(topic_id):
    """Submit helpful/not helpful feedback for a topic"""
    user_id = get_jwt_identity()
    db = current_app.db
    data = request.get_json()
    
    helpful = data.get('helpful')  # True or False
    if helpful is None:
        return jsonify({'error': 'helpful field is required'}), 400
    
    try:
        topic_obj_id = ObjectId(topic_id)
    except:
        return jsonify({'error': 'Invalid topic ID'}), 400
    
    topic = db.topics.find_one({'_id': topic_obj_id})
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    # Update vote count
    field = 'metadata.helpfulVotes' if helpful else 'metadata.notHelpfulVotes'
    db.topics.update_one(
        {'_id': topic_obj_id},
        {'$inc': {field: 1}}
    )
    
    return jsonify({'message': 'Feedback submitted successfully'}), 200

@bp.route('/<topic_id>/view', methods=['POST'])
def track_view(topic_id):
    """Track topic view"""
    db = current_app.db
    
    try:
        topic_obj_id = ObjectId(topic_id)
    except:
        return jsonify({'error': 'Invalid topic ID'}), 400
    
    db.topics.update_one(
        {'_id': topic_obj_id},
        {
            '$inc': {'metadata.views': 1},
            '$set': {'metadata.lastViewed': datetime.utcnow()}
        }
    )
    
    return jsonify({'message': 'View tracked'}), 200
