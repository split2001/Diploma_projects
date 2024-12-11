
from flask import Blueprint, request, redirect, render_template, flash
from flask_login import login_required
from flask_login import current_user
from werkzeug.utils import secure_filename
from models.word import Word
from models.userword import UserWord
from extensions import db
import os

word_bp = Blueprint('word', __name__)  # для связи роутеров с app.py

UPLOAD_FOLDER = 'static/uploads'


@word_bp.route('/')
def main():
    return render_template('main.html')


@word_bp.route('/dictionary',methods=['POST', 'GET'])
def dictionary():
    user_favorites = []
    if request.method == 'POST':
        search_word = request.form['search']  # получаем данные для поиска слов из формы
        words = Word.query.filter(Word.title.ilike(f'{search_word}')).all() or Word.query.filter(Word.translation.ilike(f'{search_word}')).all()   # используем
        # ilike для нечувствительнсти к регистру при поиске
    else:
        words = Word.query.all()  # выводим слова для неавторизованных пользователей без видимости избранного
    if current_user.is_authenticated:  # проверка авторизован или нет
        user_favorites = [user_word.word_id for user_word in db.session.query(UserWord.word_id).
        filter_by(user_id=current_user.id).all()]  # получаем не кортеж, а список с id слов
    return render_template('dictionary.html', words=words, user_favorites=user_favorites)


@word_bp.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        translation = request.form['translation']
        description = request.form['description']
        img = request.files['img']

        # Проверка на существование слова
        existing_word = Word.query.filter_by(title=title).first()
        if existing_word:
            error = 'Такое слово уже существует'
            return render_template('create.html', error=error)

        # Сохранение изображения, если оно есть
        filename = None
        if img and img.filename:
            filename = secure_filename(img.filename)  # автоматическая обработка имени файла от Flask
            img_path = os.path.join(UPLOAD_FOLDER, filename) #  путь для загрузки файла
            img.save(img_path)

        # Создание нового объекта слова
        word = Word(title=title, translation=translation, description=description, img=filename)
        db.session.add(word)
        db.session.commit()
        return redirect('/dictionary', )
    else:
        return render_template('create.html')


@word_bp.route('/add_favorites/<int:word_id>', methods=['POST', 'GET'])
@login_required
def add_favorite(word_id):
    word = Word.query.get_or_404(word_id)  # получаем слово по id
    exist_word = UserWord.query.filter_by(user_id=current_user.id, word_id=word.id).first()  # проверяем добавлял
    # ли пользователь это слово ранее

    if not exist_word:
        user_word = UserWord(user_id=current_user.id, word_id=word.id)  # добавляем в избранное
        db.session.add(user_word)
        db.session.commit()
        return redirect ('/dictionary')
    else:
        db.session.delete(exist_word) # удаляем из избранного
        db.session.commit()
    return redirect('/dictionary')


@word_bp.route('/favorites', methods=['POST', 'GET'])
@login_required
def favorites():
    words = Word.query.join(UserWord).filter(UserWord.user_id==current_user.id).all()  # соединяем 2 таблицы по внешнему
    # ключу с фильтром на текущего пользователя
    learned_words = [user_word.word_id for user_word in db.session.query(UserWord.word_id).
    filter_by(user_id=current_user.id, is_learned=True).all()]
    learned_count = len(learned_words)  # считаем количество слов со статусом is_learned=True у данного пользователя
    words = Word.query.join(UserWord).filter(UserWord.user_id == current_user.id).all()  # выводим все слова
    # из избранного
    return render_template('favorites.html', words=words,learned_count=learned_count, learned_words=learned_words)


@word_bp.route('/delete_favorites/<int:word_id>', methods=['POST', 'GET'])
@login_required
def delete_favorites(word_id):
    word = Word.query.get_or_404(word_id)  # получаем слово по id
    exist_word = UserWord.query.filter_by(user_id=current_user.id, word_id=word.id).first()# проверяем добавлял
    # ли пользователь это слово ранее
    if exist_word:
        db.session.delete(exist_word)
        db.session.commit()
        return redirect('/favorites')

# @word_bp.route('/change_status/<int:word_id>', methods=['POST', 'GET'])
# @login_required
# def change_status(word_id):
#     word = Word.query.get_or_404(word_id)
#     learned_word = UserWord.query.filter_by(user_id=current_user.id, word_id=word.id).first()
#     if learned_word:
#         learned_word.is_learned = not learned_word.is_learned
#         db.session.commit()
#     words = Word.query.join(UserWord).filter(UserWord.user_id == current_user.id).all()
#     return render_template('favorites.html', words=words)



@word_bp.route('/change_status/<int:word_id>', methods=['POST', 'GET'])
@login_required
def change_status(word_id):
    word = Word.query.get_or_404(word_id)
    learned_word = UserWord.query.filter_by(user_id=current_user.id, word_id=word.id).first()
    if learned_word:
        learned_word.is_learned = not learned_word.is_learned  # МЕНЯЕМ СТАТУС СЛОВА
        db.session.commit()
    else:
        new_learned_word = UserWord(user_id=current_user.id, word_id=word.id, is_learned=True)
        db.session.add(new_learned_word)
        db.session.commit()
    learned_words= [user_word.word_id for user_word in db.session.query(UserWord.word_id).
    filter_by(user_id=current_user.id, is_learned=True).all()]
    learned_count = len(learned_words)  # считаем количество слов со статусом is_learned=True у данного пользователя
    words = Word.query.join(UserWord).filter(UserWord.user_id == current_user.id).all()  # выводим все слова
                                                                                                        # из избранного
    return render_template('favorites.html', words=words, learned_count=learned_count, learned_words=learned_words)
