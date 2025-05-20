from flask import Blueprint, request
from app import db
from app.utils import api_response, token_required
from app.models.post import Post

post_bp = Blueprint('post', __name__)

@post_bp.route('', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json() or {}
    caption = data.get('caption')
    image_url = data.get('image_url')
    
    if image_url is None:
        return api_response(message="Image is required!", status=400)
    
    try:
        post = Post(
            image_url=image_url,
            caption=caption,
            user_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        return api_response(
            message="Create post successfully!",
            data=post.to_dict(),
            status=201
        )
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error creating post: {str(e)}", status=500)

@post_bp.route('/<int:post_id>', methods=['GET'])
@token_required
def get_post(current_user, post_id):
    post = Post.query.get(post_id)
    
    if not post or post.deleted:
        return api_response(message="Post not found!", status=404)
    
    post_data = post.to_dict()
    
    return api_response(data=post_data)

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    post = Post.query.get(post_id)
    
    if not post or post.deleted:
        return api_response(message="Post not found!", status=404)
        
    if post.user_id != current_user.id:
        return api_response(message="Unauthorized to delete this post!", status=403)
    
    try:
        post.deleted = True
        db.session.commit()
        return api_response(message="Successfully deleted post!")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error deleting post: {str(e)}", status=500)

@user_bp.route('/<int:user_id>/posts', methods=['GET'])
@token_required
def get_user_posts(current_user, user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = Post.query.filter_by(user_id=user_id, deleted=False)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    response_data = {
        'items': [post.to_dict() for post in posts.items],
        'pagination': {
            'page': posts.page,
            'per_page': posts.per_page,
            'total': posts.total,
            'pages': posts.pages
        }
    }
    
    return api_response(data=response_data)

@post_bp.route('/<int:post_id>/like', methods=['POST'])
@token_required
def like_post(current_user, post_id):
    target_post = Post.query.get(post_id)
    if not target_post:
        return api_response(message="Post does not exist!", status=404)

    existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing:
        return api_response(message="Already liked this post!", status=400)
    like = Like(user_id=current_user.id, post_id=post_id)

    try:
        db.session.add(like)
        db.session.commit()
        return api_response(message="Liked post successfully!")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error like post: {str(e)}", status=500)


@post_bp.route('/<int:post_id>/like', methods=['DELETE'])
@token_required
def unlike_post(current_user, post_id):
    target_post = Post.query.get(post_id)
    if not target_post:
        return api_response(message="Post does not exist!", status=404)

    existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing is None or not existing:
        return api_response(message="You have not liked this post!", status=400)

    try:
        db.session.delete(existing)
        db.session.commit()
        return api_response(message="Unliked post successfully")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error unlike post: {str(e)}", status=500)

@post_bp.route('/newsfeed', methods=['GET'])
@token_required
def view_news_feed(current_user):
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Get posts from database with pagination
    # [Complete this]

    # Prepare response data
    # [Complete this]

    return api_response(data=response_data)