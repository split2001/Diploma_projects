from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # Сессия БД
from app.backend.db_depends import get_db  # Функция подключения к БД
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.book import Book
from app.models.user import User
from app.models.association import UserBook
from app.shemas import CreateUser, UpdateUser, CreateBook, UpdateBook, UpdateBookStatus
from sqlalchemy import insert, select, update, delete  # Функции работы с записями
from app.routers.user import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.routers.user import get_current_user

templates = Jinja2Templates(directory='app/templates')

router = APIRouter(prefix='/book', tags=['book'])


@router.get('/library')
async def all_books(request: Request, db: Annotated[Session, Depends(get_db)], user: User = Depends(get_current_user)):
    # подключается к базе данных в момент обращения при помощи функции get_db
    books = db.query(Book).all()
    return templates.TemplateResponse('books.html', {'request': request, 'books': books, 'user': user})


@router.get('/author')  # форма для поиска по автору
async def author_form(request: Request):
    return templates.TemplateResponse('author.html', {'request': request})


@router.post('/author')
async def book_by_author(request: Request, db: Annotated[Session, Depends(get_db)], book_author: str = Form()):
    # подключается к базе данных в момент обращения при помощи функции get_db:
    books = db.query(Book).filter(Book.author == book_author).all()
    if not books:  # if books is None всегда возвращает список, даже пустой
        error = 'Автор не найден'
        return templates.TemplateResponse('author.html', {'request': request, 'error': error})
    return templates.TemplateResponse('author.html', {'request': request, 'books': books})


@router.get('/genre')  # форма для поиска по жанру
async def genre_form(request: Request):
    return templates.TemplateResponse('genre.html', {'request': request})


@router.post('/genre')
async def book_by_genre(request: Request, db: Annotated[Session, Depends(get_db)], book_genre: str = Form()): #  подключается к базе данных в момент
    # обращения при помощи функции get_db:
    books = db.query(Book).filter(Book.genre == book_genre).all()
    if not books:  # if books is None всегда возвращает список, даже пустой
        error = 'Жанр не найден'
        return templates.TemplateResponse('genre.html', {'request': request, 'error': error})
    return templates.TemplateResponse('genre.html', {'request': request, 'books': books})


@router.get('/create')  # форма для добавления книги
async def create_form(request: Request):
    return templates.TemplateResponse('create.html', {'request': request})


@router.post('/create')
async def create_book(request: Request, db: Annotated[Session, Depends(get_db)], title: str = Form(),
                      description: str = Form(), author: str = Form(), genre: str = Form()):
    existing_book = db.query(Book).filter(Book.title == title).first()
    if existing_book is None:
        new_book = Book(title=title, description=description, author=author, genre=genre)
        db.add(new_book)
        db.commit()
        return RedirectResponse('/book/library', status_code=303)
    else:
        error = 'Такая книга уже существует'
        return templates.TemplateResponse('create.html', {'request': request, 'error': error})


@router.put('/update')
async def update_book(db: Annotated[Session, Depends(get_db)], book_id: int, update_book: UpdateBook):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
        # Обновляем поля книги
    if update_book.title is not None:
        book.title = update_book.title
    if update_book.description is not None:
        book.description = update_book.description
    if update_book.author is not None:
        book.author = update_book.author
    if update_book.genre is not None:
        book.genre = update_book.genre
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Книга успешно обновлена!'}


@router.get('/add/{book_id}')
async def add_favorite(request: Request, book_id: int, db: Annotated[Session, Depends(get_db)],
                   user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    if book in user.books:
        user.books.remove(book)
    else:
        user.books.append(book)
    db.commit()
    return templates.TemplateResponse('books.html', {'request': request, 'user': user,
                                                     'user_books': user.books, 'books': db.query(Book).all()})


@router.get('/delete_favorite/{book_id}')
async def delete_favorite(request: Request, book_id: int, db: Annotated[Session, Depends(get_db)],
                          user: User = Depends(get_current_user)):
    # подключается к базе данных в момент обращения при помощи функции get_db
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    if book in user.books:
        user.books.remove(book)
        db.commit()
    return templates.TemplateResponse('favorites.html', {'request': request, 'books': user.books,
                                                         'username': user.username})


@router.get('/favorites')
async def favorite(request: Request, db: Annotated[Session, Depends(get_db)], user: User = Depends(get_current_user)):
    user_books = db.query(Book).join(UserBook).filter(UserBook.user_id == user.id).all()
    read_books = [user_book.book.id for user_book in
                  db.query(UserBook).filter_by(user_id=user.id, is_read=True)]
    return templates.TemplateResponse('favorites.html', {'request': request, 'books': user_books,
                                                         'username': user.username, 'read_books': read_books})


@router.post('/update_book_status/{book_id}')
async def update_book_status(request: Request, db: Annotated[Session, Depends(get_db)], book_id: int,
                             user: User = Depends(get_current_user)):
    # Получаем данные из промежуточной таблицы
    user_book = db.query(UserBook).filter_by(user_id=user.id, book_id=book_id).first()
    if not user_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о книге не найдена в списке пользователя"
        )
    user_book.is_read = not user_book.is_read  # Переключаем статус книги
    db.commit()  # сохраняем статус книги в БД
    # Объединяем таблицы. Получаем обновленный список книг пользователя с их статусами
    user_books = db.query(Book).join(UserBook).filter(UserBook.user_id == user.id).all()
    read_books = [user_book.book.id for user_book in
                  db.query(UserBook).filter_by(user_id=user.id, is_read=True)]
    return templates.TemplateResponse('favorites.html', {'request': request, 'books': user_books, 'user': user,
                                                         'read_books': read_books})


@router.delete('/delete')
async def delete_book(db: Annotated[Session, Depends(get_db)], book_id: int):
    # подключается к базе данных в момент обращения при помощи функции get_db
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    db.query(UserBook).filter(UserBook.book_id == book_id).delete()
    db.delete(book)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Книга успешно удалена'}
