from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship  # связь с другими моделями
from app.backend.db import Base  #


# Промежуточная таблица для связи "многие ко многим"
# user_book_association = Table(
#     'user_book',
#     Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
#     Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
#     Column('is_read', Boolean, default=False)
# )

class UserBook(Base):
    __tablename__ = 'user_book'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    is_read = Column(Boolean, default=False)

    user = relationship('User', back_populates='user_books')
    book = relationship('Book', back_populates='user_books')
