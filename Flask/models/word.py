
from extensions import db


class Word(db.Model):
    __tablename__= 'word'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    translation = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    img = db.Column(db.String, nullable=True)

    users = db.relationship('UserWord', back_populates='word', cascade='all, delete-orphan')