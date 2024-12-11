from flask import Blueprint, request, redirect,render_template
from flask_login import login_user, logout_user, current_user
from forms import RegisterForm, LoginForm
from models.user import User
from extensions import db, bcrypt


user_bp = Blueprint('user', __name__)  # для связи routers c app.py

@user_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm() # получаем форму авторизации
    if form.validate_on_submit(): # проверяем ее на валидность
        user = User.query.filter_by(username=form.username.data).first()  # проверяем наличие пользователя в БД
        if user and bcrypt.check_password_hash(user.password, form.password.data): # проверка совпадения
    # сохраненного пароля в БД и введенного в форме
            login_user(user)  # логиним пользователя
            return redirect('/')
        else:
            form.password.errors.append('Неправильное имя пользователя или пароль.')
    return render_template('login.html', form=form)


@user_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()  # получаем форму регистрации
    if form.validate_on_submit(): # проверяем ее на валидность
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # проверяем ее на валидность
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)  # логиним пользователя
        return redirect ('/')
    return render_template('register.html', form=form)


@user_bp.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect('/login')