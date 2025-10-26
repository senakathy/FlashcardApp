from datetime import datetime
from app import db
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    profile_image_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    folders = db.relationship('Folder', backref='user', lazy=True, cascade='all, delete-orphan')
    flashcards = db.relationship('Flashcard', backref='user', lazy=True, cascade='all, delete-orphan')


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.String, db.ForeignKey(User.id))
    browser_session_key = db.Column(db.String, nullable=False)
    user = db.relationship(User)

    __table_args__ = (UniqueConstraint(
        'user_id',
        'browser_session_key',
        'provider',
        name='uq_user_browser_session_key_provider',
    ),)


class Folder(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    flashcards = db.relationship('Flashcard', backref='folder', lazy=True, cascade='all, delete-orphan')


class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    meaning = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    folder_id = db.Column(db.String, db.ForeignKey('folders.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
