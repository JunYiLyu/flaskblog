from flaskblog import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique=True,nullable=False)
    password = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    image_file = db.Column(db.String(50),default='default.jpg')
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(500),nullable=False)
    post_date = db.Column(db.Date,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.content}','{self.post_date}')"
