from extensions import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_name = db.Column(db.String(100))
    user_role = db.Column(db.String(100))
    avatar = db.Column(db.String(300))
    post_text = db.Column(db.String(500))
    post_image = db.Column(db.String(300))
    post_time = db.Column(db.DateTime, default=datetime.utcnow)



    

