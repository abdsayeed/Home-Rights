from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId

bp = Blueprint('topics', __name__)

@bp.route('/', methods=['GET'])
def list_topics():
    db = current_app.db
    category = request.args.get('category')
    
    query = {'published': True}
    if category:
        query['category'] = category
    
    topics = db.topics.find(query).sort('title', 1)
    
    result = []
    for topic in topics:
        result.append({
            'id': str(topic['_id']),
            'title': topic['title'],
            'slug': topic['slug'],
            'category': topic['category'],
            'summary': topic['summary'],
            'tags': topic.get('tags', [])
        })
    
    return jsonify({'topics': result}), 200

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
