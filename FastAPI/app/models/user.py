from sqlalchemy import Column, Integer, String, Boolean
from app.backend.db import Base
from sqlalchemy.orm import relationship  # связь с другими моделями
# from sqlalchemy.schema import CreateTable
from app.models.association import UserBook


class User(Base):  # модель User, наследованная от ранее написанного Base
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    age = Column(Integer)
    user_books = relationship('UserBook', back_populates='user')
    books = relationship('Book', secondary='user_book', back_populates='users')
    # объект связи с таблицей Book, UserBook
    # back_populates содержит в себе название объекта для связи

# print(CreateTable(User.__table__))
