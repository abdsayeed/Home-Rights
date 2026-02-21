"""Admin authentication and authorization decorators"""
from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from bson import ObjectId
from datetime import datetime

def require_admin(allowed_roles=None):
    """
    Decorator to require admin authentication and optionally specific roles.
    Usage: @require_admin() or @require_admin(['super_admin', 'content_admin'])
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT token
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            # Get user from database
            db = current_app.db
            try:
                user = db.users.find_one({'_id': ObjectId(user_id)})
            except:
                return jsonify({'error': 'Invalid user ID'}), 401
            
            if not user:
                return jsonify({'error': 'User not found'}), 401
            
            # Check if user has admin role
            user_role = user.get('role', 'user')
            if user_role not in current_app.config['ADMIN_ROLES']:
                return jsonify({'error': 'Admin access required'}), 403
            
            # Check specific role if required
            if allowed_roles and user_role not in allowed_roles:
                return jsonify({'error': f'Insufficient permissions. Required: {", ".join(allowed_roles)}'}), 403
            
            # Log admin action to audit log
            log_admin_action(
                admin_id=user_id,
                admin_email=user.get('email'),
                action=f"{request.method} {request.path}",
                ip=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def log_admin_action(admin_id, admin_email, action, ip, user_agent, target_entity=None, target_id=None, before=None, after=None):
    """Log admin action to audit log"""
    from flask import current_app
    
    audit_entry = {
        'adminId': ObjectId(admin_id),
        'adminEmail': admin_email,
        'action': action,
        'targetEntity': target_entity,
        'targetId': target_id,
        'before': before,
        'after': after,
        'ip': ip,
        'userAgent': user_agent,
        'timestamp': datetime.utcnow()
    }
    
    current_app.db.audit_logs.insert_one(audit_entry)
