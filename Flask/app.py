from flask import Flask
from extensions import db, login_manager, bcrypt
from flask_migrate import Migrate
import os


def create_app():
    app = Flask(__name__)  # создаем экземпляр приложения
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # настройка подключения к БД
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'  # путь для загрузки изображений
    app.config['SECRET_KEY'] = os.urandom(24) # создаем секретный ключ
    db.init_app(app)  # связываем с SQLAlchemy приложением
    bcrypt.init_app(app)  # хеширование паролей
    login_manager.init_app(app)  # система аутентификации
    login_manager.login_view = 'user.login'
    migrate = Migrate(app, db)

    with app.app_context():
        from models.word import Word
        from models.user import User
        from models.userword import UserWord
        from routers.word import word_bp  # импортируем routers
        from routers.user import user_bp  # импортируем routers
        app.register_blueprint(word_bp)  # подключаем routers
        app.register_blueprint(user_bp)  # подключаем routers
        db.create_all()  # создаем таблицы в БД
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

