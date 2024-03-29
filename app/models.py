import os
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime 

SECRET_KEY = os.environ.get('SECRET_KEY')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
 
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable =False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    

class Quotes():
    def __init__ (self,author,quote,permalink):
        self.author = author
        self.quote = quote
        self.permalink = permalink

# class Comment(db.Model):
#     __tablename__ = 'comments'

#     id = db.Column(db.Integer,primary_key = True)
#     comment = db.Column(db.String(1000))
#     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
#     post = db.Column(db.Integer,db.ForeignKey("post.id"))

#     def save_comment(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_comments(cls,pitch):
#         comments = Comment.query.filter_by(post_id=post).all()
#         return comments
        