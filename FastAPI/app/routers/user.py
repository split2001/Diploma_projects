from fastapi import APIRouter, Depends, status, HTTPException, Form, Request, Response
from sqlalchemy.orm import Session
# # Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.shemas import CreateUser, UpdateUser
from app.models.user import User
from app.models.book import Book
from app.models.association import UserBook
# # Функции работы с записями.
from sqlalchemy import select, insert, delete, update
from passlib.context import CryptContext  # хеширование паролей
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse  # переадресация на другую страницу


templates = Jinja2Templates(directory='app/templates')

router = APIRouter(prefix='/user', tags=['user'])


# Объект с настройками для хеширования
# schemes алгоритм хеширования, можно использовать несколько
# deprecated помечает устаревшие алгоритмы
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для хеширования паролей
def hash_password(password: str) -> str:  # хэшируем пароль
    return pwd_context.hash(password)


# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:  # проверяем пароль
    return pwd_context.verify(plain_password, hashed_password)


# функция извлекает текущего пользователя из сессии
# Depends позволяет подключить зависимость(функцию) и передать ее результат маршруту
def get_current_user(request: Request, db: Annotated[Session, Depends(get_db)]) -> User:
    user_id = request.session.get('user_id')  # извлечение user из сессии по user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не авторизован'
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    return user


@router.get('/logout')
async def logout_user(request: Request):
    request.session.clear()
    return RedirectResponse('/', status_code=303)


@router.get('/all')
async def all_users(db: Annotated[Session, Depends(get_db)]):  # подключается к базе данных в момент обращения при
    # помощи функции get_db
    users = db.query(User).all()
    return users  # возвращать список всех пользователей из


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):  # подключается к базе данных в момент
    # обращения при помощи функции get_db
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    else:
        return user


@router.get('/register')  # запрос GET для получения формы регистрации
async def register_form(request: Request):
    print('request object:', request)
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/register')
async def register(request: Request, db: Annotated[Session, Depends(get_db)], username: str = Form(),
                   password: str = Form(), firstname: str = Form(), lastname: str = Form(), age: int = Form()
                   ):  # подключается к базе данных
    # в момент обращения при помощи функции get_db
    existing_user = db.query(User).filter(User.username == username).first()  # проверка на наличие пользователя
    if existing_user:
        error = 'Пользователь уже существует'
        return templates.TemplateResponse('register.html', {'request': request, 'error': error})

    hashed_password = hash_password(password)  # задаем переменную для хэшированного пароля
    new_user = User(username=username, password=hashed_password, firstname=firstname, lastname=lastname, age=age)
    db.add(new_user)  # добавляем нового пользователя
    db.commit()
    request.session['user_id'] = new_user.id  # сохраняем user_id в сессии
    return RedirectResponse('/', status_code=303)


@router.get('/login')  # запрос GET для получения формы авторизации
async def login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/login')
# Авторизация пользователя
def login_user(request: Request, db: Annotated[Session, Depends(get_db)], username: str = Form(),
               password: str = Form()):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):  # проверка на совпадение хэша паролей и username
        error = 'Неверный логин или пароль'
        return templates.TemplateResponse('login.html', {'request': request, 'error': error})
    request.session['user_id'] = user.id  # сохраняем user_id в сессии
    return RedirectResponse('/', status_code=303)


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    # подключается к базе данных в момент обращения при помощи функции get_db
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    db.query(UserBook).filter(UserBook.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Пользователь успешно удален!'}