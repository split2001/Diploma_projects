from sqlalchemy import ForeignKey
from extensions import db
from models.word import Word
from models.user import User

class UserWord(db.Model):
    __tablename__= 'user_word'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id', ondelete='CASCADE', name='key_user'))
    word_id = db.Column(db.Integer, ForeignKey('word.id',  ondelete='CASCADE', name='key_user'))
    is_learned = db.Column(db.Boolean, default=False, nullable=False)

    word = db.relationship('Word', back_populates='users')
    user  = db.relationship('User', back_populates='words')