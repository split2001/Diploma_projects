from extensions import db, login_manager
from flask_login import UserMixin  # добавляет такие свойства как is_authenticated, is_active



# загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    words = db.relationship('UserWord', back_populates='user', cascade='all, delete-orphan')