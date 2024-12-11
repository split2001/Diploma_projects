from flask_sqlalchemy import SQLAlchemy  # для работы с БД
from flask_bcrypt import Bcrypt  # хеширование паролей
from flask_login import LoginManager   # авторизация, регистрация пользователей


bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()

