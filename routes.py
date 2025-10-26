from flask import session, render_template, request, redirect, url_for
from flask_login import current_user
import uuid

from app import app, db
from replit_auth import require_login, make_replit_blueprint
from models import Folder, Flashcard

app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('landing.html')


@app.route('/home', methods=['GET', 'POST'])
@require_login
def home():
    if request.method == 'POST':
        word_list = request.form['words'].split('\n')
        for line in word_list:
            if ':' in line:
                word, meaning = line.split(':', 1)
                flashcard = Flashcard(
                    word=word.strip(),
                    meaning=meaning.strip(),
                    user_id=current_user.id
                )
                db.session.add(flashcard)
        db.session.commit()
    return render_template('input.html', user=current_user)


@app.route('/review')
@require_login
def review():
    flashcards = Flashcard.query.filter_by(user_id=current_user.id).all()
    current_index = 0
    return render_template('review.html', flashcards=flashcards, current_index=current_index, user=current_user)


@app.route('/my-flashcards')
@require_login
def my_flashcards():
    folders = Folder.query.filter_by(user_id=current_user.id).all()
    uncategorized = Flashcard.query.filter_by(user_id=current_user.id, folder_id=None).all()
    return render_template('my-flashcards.html', folders=folders, uncategorized=uncategorized, user=current_user)


@app.route('/create-folder', methods=['POST'])
@require_login
def create_folder():
    folder_name = request.form.get('folder_name', '').strip()
    if folder_name:
        new_folder = Folder(
            id=str(uuid.uuid4()),
            name=folder_name,
            user_id=current_user.id
        )
        db.session.add(new_folder)
        db.session.commit()
    return redirect(url_for('my_flashcards'))


@app.route('/move-flashcard', methods=['POST'])
@require_login
def move_flashcard():
    flashcard_id = int(request.form.get('flashcard_id', 0))
    to_folder = request.form.get('to_folder', '')
    
    flashcard = Flashcard.query.filter_by(id=flashcard_id, user_id=current_user.id).first()
    
    if flashcard:
        if to_folder == 'uncategorized':
            flashcard.folder_id = None
        else:
            folder = Folder.query.filter_by(id=to_folder, user_id=current_user.id).first()
            if folder:
                flashcard.folder_id = folder.id
        db.session.commit()
    
    return redirect(url_for('my_flashcards'))


@app.route('/delete-folder/<folder_id>', methods=['POST'])
@require_login
def delete_folder(folder_id):
    folder = Folder.query.filter_by(id=folder_id, user_id=current_user.id).first()
    if folder:
        for flashcard in folder.flashcards:
            flashcard.folder_id = None
        db.session.delete(folder)
        db.session.commit()
    return redirect(url_for('my_flashcards'))
