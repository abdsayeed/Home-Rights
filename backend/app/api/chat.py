from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from app.services.chat_service import ChatService

bp = Blueprint('chat', __name__)

@bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    user_id = get_jwt_identity()
    db = current_app.db
    
    sessions = db.chat_sessions.find({'userId': ObjectId(user_id)}).sort('updatedAt', -1).limit(20)
    
    result = []
    for session in sessions:
        last_message = session['messages'][-1] if session['messages'] else None
        result.append({
            'id': str(session['_id']),
            'lastMessage': last_message['content'][:50] if last_message else '',
            'updatedAt': session['updatedAt'].isoformat(),
            'messageCount': len(session['messages'])
        })
    
    return jsonify({'sessions': result}), 200

@bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_session():
    user_id = get_jwt_identity()
    db = current_app.db
    
    session = {
        'userId': ObjectId(user_id),
        'messages': [],
        'metadata': {
            'topic': None,
            'resolved': False
        },
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    }
    
    result = db.chat_sessions.insert_one(session)
    
    return jsonify({
        'session_id': str(result.inserted_id)
    }), 201

@bp.route('/sessions/<session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    user_id = get_jwt_identity()
    db = current_app.db
    
    try:
        session = db.chat_sessions.find_one({
            '_id': ObjectId(session_id),
            'userId': ObjectId(user_id)
        })
    except:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify({
        'id': str(session['_id']),
        'messages': session['messages'],
        'createdAt': session['createdAt'].isoformat(),
        'updatedAt': session['updatedAt'].isoformat()
    }), 200

@bp.route('/sessions/<session_id>/messages', methods=['POST'])
@jwt_required()
def send_message(session_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Message content is required'}), 400
    
    db = current_app.db
    
    try:
        session = db.chat_sessions.find_one({
            '_id': ObjectId(session_id),
            'userId': ObjectId(user_id)
        })
    except:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    user_message = {
        'role': 'user',
        'content': content,
        'timestamp': datetime.utcnow(),
        'attachments': []
    }
    
    # Generate intelligent AI response using ChatService
    try:
        # Get conversation history for context
        conversation_history = session.get('messages', [])
        
        # Generate response
        ai_response = ChatService.generate_response(content, conversation_history)
        
        assistant_message = {
            'role': 'assistant',
            'content': ai_response['response'],
            'timestamp': datetime.utcnow(),
            'metadata': {
                'intent': ai_response.get('intent'),
                'needs_followup': ai_response.get('needs_followup', False)
            },
            'attachments': []
        }
    except Exception as e:
        print(f"Error generating AI response: {e}")
        assistant_message = {
            'role': 'assistant',
            'content': "I apologize, but I'm having trouble processing your message right now. Could you try rephrasing your question? I'm here to help with housing law questions, document reviews, and tenant rights.",
            'timestamp': datetime.utcnow(),
            'attachments': []
        }
    
    db.chat_sessions.update_one(
        {'_id': ObjectId(session_id)},
        {
            '$push': {
                'messages': {
                    '$each': [user_message, assistant_message]
                }
            },
            '$set': {'updatedAt': datetime.utcnow()}
        }
    )
    
    return jsonify({
        'user_message': user_message,
        'assistant_message': assistant_message
    }), 200

@bp.route('/message', methods=['POST'])
@jwt_required()
def quick_message():
    """
    Quick message endpoint without session management
    For simple chat interactions
    """
    data = request.get_json()
    
    message = data.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        # Generate intelligent response
        ai_response = ChatService.generate_response(message)
        
        return jsonify({
            'response': ai_response['response'],
            'intent': ai_response.get('intent'),
            'needs_followup': ai_response.get('needs_followup', False)
        }), 200
        
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return jsonify({
            'response': "I apologize, but I'm having trouble processing your message right now. Could you try rephrasing your question? I'm here to help with housing law questions, document reviews, and tenant rights.",
            'intent': 'error',
            'needs_followup': True
        }), 200
