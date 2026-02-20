from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('support', __name__)

@bp.route('/find', methods=['GET'])
def find_support():
    postcode = request.args.get('postcode')
    
    if not postcode:
        return jsonify({'error': 'Postcode is required'}), 400
    
    db = current_app.db
    agencies = db.agencies.find().limit(10)
    
    result = []
    for agency in agencies:
        result.append({
            'id': str(agency['_id']),
            'name': agency['name'],
            'type': agency['type'],
            'contact': agency['contact'],
            'address': agency['address'],
            'services': agency.get('services', [])
        })
    
    return jsonify({'agencies': result}), 200

@bp.route('/types', methods=['GET'])
def get_support_types():
    return jsonify({
        'types': [
            {'value': 'council', 'label': 'Local Council'},
            {'value': 'charity', 'label': 'Charity'},
            {'value': 'legal_aid', 'label': 'Legal Aid'},
            {'value': 'advice_center', 'label': 'Advice Center'}
        ]
    }), 200
