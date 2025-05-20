from flask import Blueprint

from app.utils import api_response, token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return api_response(data=current_user['profile'])

@user_bp.route('/<int:user_id>/profile', methods=['GET'])
@token_required
def view_other_profile(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return api_response(message="User not found", status=404)

@user_bp.route('/profile', methods=['PUT'])
@token_required
def edit_profile(current_user):
    data = request.get_json() or {}
    allowed_fields = ['fullname', 'email', 'username', 'bio']
    fields_to_update = {k: v for k, v in data.items() if k in allowed_fields and v}

    # If no fields to update, return error
    if not fields_to_update:
        return api_response(message="No fields to update", status=400)

    if 'username' in fields_to_update and fields_to_update['username'] != current_user.username:
        if User.query.filter_by(username=fields_to_update['username']).first():
            return api_response(message="Username already exists", status=400)

    if 'email' in fields_to_update and fields_to_update['email'] != current_user.email:
        if User.query.filter_by(email=fields_to_update['email']).first():
            return api_response(message="Email already exists", status=400)

    # Update user info
    for key, value in fields_to_update.items():
        setattr(current_user, key, value)

    try:
        db.session.commit()
        return api_response(message="Update profile successfully", data=current_user.to_dict())
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error updating profile: {str(e)}", status=500)

@user_bp.route('/<int:user_id>/follow', methods=['POST'])
@token_required
def follow_user(current_user, user_id):
    if current_user.id == user_id:
        return api_response(message="Cannot follow yourself!", status=400)
    target_user = User.query.get(user_id)
    if not target_user:
        return api_response(message="User does not exist!", status=404)
    existing = Follow.query.filter_by(follower_id=current_user.id, following_id=user_id).first()
    if existing:
        return api_response(message="Already followed this user!", status=400)
    follow = Follow(follower_id=current_user.id, following_id=user_id)
    
    try:
        db.session.add(follow)
        db.session.commit()
        return api_response(message="Follow user successfully!")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error following user: {str(e)}", status=500)

@user_bp.route('/<int:user_id>/follow', methods=['DELETE'])
@token_required
def unfollow_user(current_user, user_id):
    # Cannot unfollow self
    if current_user.id == user_id:
        return api_response(message="Cannot unfollow yourself!", status=400)
  
    # Check target exists
    target_user = User.query.get(user_id)
    if not target_user:
        return api_response(message="User does not exist!", status=404)
  
    # Check existing follow relationship
    existing = Follow.query.filter_by(follower_id=current_user.id, following_id=user_id).first()
    if existing is None or not existing:
        return api_response(message="You have not followed this user before!", status=400)
        
  
    # Remove follow relationship
    try:
        db.session.delete(existing)
        db.session.commit()
        return api_response(message="Unfollow user successfully!")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error unfollowing user: {str(e)}", status=500)
