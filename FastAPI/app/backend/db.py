from sqlalchemy import create_engine  # позволит запускать БД
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine('sqlite:///database.db', echo=True)  # для связи с базой данных
#  echo=True позволяет увидеть все SQL запросы в консоли

SessionLocal = sessionmaker(bind=engine)  # создаем сессию связи с БД


class Base(DeclarativeBase):  # DeclarativeBase позволяет объединить наш класс и таблицу с БД
    pass

