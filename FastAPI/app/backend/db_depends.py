from app.backend.db import SessionLocal  # сессия связи с БД


async def get_db():
    db = SessionLocal()  # Создаем сессию
    try:
        yield db  # Возвращаем созданную сессию
    finally:
        db.close()  # закрываем сессию
