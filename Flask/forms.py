from flask_wtf import FlaskForm  # создание форм получения данных
from wtforms import StringField, EmailField, PasswordField, SubmitField  # поля форм
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError  # валидаторы для полей в формах
from models.user import User

# форма Регистрации
class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4,max=20)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=4,max=20)])
    password = PasswordField('Пароль',validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль',validators=[DataRequired(),
                                                                      EqualTo('password', message='Пароли не совпадают.')])
    submit = SubmitField('Зарегистрироваться')

    # проверка имени пользователя на повтор
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Пользователь уже существует.')


# Форма Авторизации
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')