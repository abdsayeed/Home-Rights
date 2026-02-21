from flask import Blueprint, request, jsonify, current_app
import requests

bp = Blueprint('support', __name__)

def resolve_postcode(postcode):
    """Resolve UK postcode to coordinates using postcodes.io API"""
    try:
        response = requests.get(f'https://api.postcodes.io/postcodes/{postcode}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 200:
                result = data.get('result', {})
                return {
                    'lat': result.get('latitude'),
                    'lng': result.get('longitude'),
                    'region': result.get('region'),
                    'district': result.get('admin_district')
                }
    except:
        pass
    return None

@bp.route('/find', methods=['GET'])
def find_support():
    """Find support organizations with geo-spatial search"""
    db = current_app.db
    
    # Pagination
    page = int(request.args.get('page', 1))
    limit = min(int(request.args.get('limit', 20)), 100)
    skip = (page - 1) * limit
    
    query = {}
    use_geo = False
    lat = None
    lng = None
    
    # Location-based search
    postcode = request.args.get('postcode')
    lat_param = request.args.get('lat')
    lng_param = request.args.get('lng')
    radius = float(request.args.get('radius', 10))  # km
    
    if postcode:
        # Resolve postcode to coordinates
        location_data = resolve_postcode(postcode)
        if location_data:
            lat = location_data['lat']
            lng = location_data['lng']
    elif lat_param and lng_param:
        lat = float(lat_param)
        lng = float(lng_param)
    
    # Filter by type
    if request.args.get('type'):
        query['type'] = request.args.get('type')
    
    # Filter by service
    if request.args.get('service'):
        query['services'] = request.args.get('service')
    
    # Only show verified and accepting referrals
    query['verificationStatus'] = {'$in': ['verified', 'unverified']}
    query['isAcceptingReferrals'] = True
    
    # Get organizations
    if lat and lng:
        # Use aggregation pipeline for geo-spatial query
        use_geo = True
        pipeline = [
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': [float(lng), float(lat)]
                    },
                    'distanceField': 'distanceMeters',
                    'maxDistance': radius * 1000,  # Convert km to meters
                    'spherical': True,
                    'query': query
                }
            },
            {'$skip': skip},
            {'$limit': limit}
        ]
        
        agencies_cursor = db.support_orgs.aggregate(pipeline)
        agencies = list(agencies_cursor)
        
        # For total count with geo query, we need a separate aggregation
        count_pipeline = [
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': [float(lng), float(lat)]
                    },
                    'distanceField': 'distanceMeters',
                    'maxDistance': radius * 1000,
                    'spherical': True,
                    'query': query
                }
            },
            {'$count': 'total'}
        ]
        count_result = list(db.support_orgs.aggregate(count_pipeline))
        total = count_result[0]['total'] if count_result else 0
    else:
        # Regular query without geo
        total = db.support_orgs.count_documents(query)
        agencies = list(db.support_orgs.find(query).skip(skip).limit(limit))
    
    result = []
    for agency in agencies:
        org_data = {
            'id': str(agency['_id']),
            'name': agency['name'],
            'type': agency['type'],
            'description': agency.get('description', ''),
            'contact': agency['contact'],
            'address': agency['address'],
            'services': agency.get('services', []),
            'verificationStatus': agency.get('verificationStatus', 'unverified'),
            'openingHours': agency.get('openingHours', {})
        }
        
        # Add distance if geo query was used
        if use_geo and 'distanceMeters' in agency:
            org_data['distanceKm'] = round(agency['distanceMeters'] / 1000, 2)
        
        result.append(org_data)
    
    return jsonify({
        'organizations': result,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit
        }
    }), 200

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


@bp.route('/<org_id>', methods=['GET'])
def get_organization(org_id):
    """Get detailed organization information"""
    db = current_app.db
    
    from bson import ObjectId
    try:
        org = db.support_orgs.find_one({'_id': ObjectId(org_id)})
    except:
        return jsonify({'error': 'Invalid organization ID'}), 400
    
    if not org:
        return jsonify({'error': 'Organization not found'}), 404
    
    return jsonify({
        'id': str(org['_id']),
        'name': org['name'],
        'type': org['type'],
        'description': org.get('description', ''),
        'services': org.get('services', []),
        'contact': org['contact'],
        'address': org['address'],
        'location': org.get('location', {}),
        'openingHours': org.get('openingHours', {}),
        'verificationStatus': org.get('verificationStatus', 'unverified'),
        'lastVerifiedAt': org.get('lastVerifiedAt').isoformat() if org.get('lastVerifiedAt') else None,
        'isAcceptingReferrals': org.get('isAcceptingReferrals', True)
    }), 200

@bp.route('/<org_id>/referral', methods=['POST'])
def track_referral(org_id):
    """Track when a user contacts an organization"""
    db = current_app.db
    data = request.get_json()
    
    from bson import ObjectId
    from datetime import datetime
    
    try:
        org_obj_id = ObjectId(org_id)
    except:
        return jsonify({'error': 'Invalid organization ID'}), 400
    
    referral = {
        'orgId': org_obj_id,
        'referralType': data.get('type', 'website'),  # phone, email, website, directions
        'timestamp': datetime.utcnow()
    }
    
    db.referrals.insert_one(referral)
    
    return jsonify({'message': 'Referral tracked'}), 200

@bp.route('/submit', methods=['POST'])
def submit_organization():
    """Public endpoint for organizations to submit themselves"""
    db = current_app.db
    data = request.get_json()
    
    from datetime import datetime
    
    required = ['name', 'type', 'contact', 'description']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    org = {
        'name': data['name'],
        'type': data['type'],
        'description': data['description'],
        'services': data.get('services', []),
        'contact': data['contact'],
        'address': data.get('address', ''),
        'location': data.get('location', {}),
        'openingHours': data.get('openingHours', {}),
        'verificationStatus': 'pending',
        'isAcceptingReferrals': True,
        'submittedAt': datetime.utcnow(),
        'status': 'pending_review'
    }
    
    result = db.support_orgs.insert_one(org)
    
    return jsonify({
        'id': str(result.inserted_id),
        'message': 'Organization submitted for review',
        'referenceNumber': str(result.inserted_id)[:8].upper()
    }), 201
