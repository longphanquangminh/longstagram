class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column('created_at', db.Integer, default=lambda: int(datetime.now().timestamp())),
    updated_at = db.Column('updated_at', db.Integer, default=lambda: int(datetime.now().timestamp()), onupdate=int(datetime.now().timestamp())),

    def __repr__(self):
        return f'Post id={self.id} user_id={self.user_id}'
    
    def to_dict(self, include_user=False, include_likes=False, current_user=None):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'image_url': self.image_url,
            'caption': self.caption,
            'deleted': self.deleted,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if include_user:
            user = User.query.get(self.user_id)
            data['user'] = user.to_dict()
            
        if include_likes:
            data['like_count'] = Like.query.filter_by(post_id=self.id).count()
            if current_user:
                data['liked_by_current_user'] = Like.query.filter_by(post_id=self.id, user_id=current_user.id).first() is not None
            else:
                data['liked_by_current_user'] = False
        return data

