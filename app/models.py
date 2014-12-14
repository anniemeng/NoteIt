from . import db, login_manager
from flask import request
from flask.ext.login import UserMixin, login_required
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    documents = db.relationship('Document', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_doc(self, title, article, notes, highlight):
        all_docs = Document.query.all()
        found = False
        for doc in all_docs:
            if (doc.article == article):
                note = Note(body=notes, document_id=doc.id, highlight=highlight)
                doc.notes.append(note)
                found = True
                db.session.add(note)
                db.session.add(doc)
                db.session.commit()
                break
        if (not found):
            new_doc = Document(title=title, article=article, user_id=self.id)
            note = Note(body=notes, document_id=new_doc.id, highlight=highlight)
            new_doc.notes.append(note)
            self.documents.append(new_doc)
            db.session.add(self)
            db.session.add(note)
            db.session.add(new_doc)
            db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Document(db.Model):
    __tablename__='docs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    article = db.Column(db.Text)
    notes = db.relationship('Note', backref='notes', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Document %r>' % self.id

class Note(db.Model):
    __tablename__='notes'
    id = db.Column(db.Integer, primary_key=True)
    highlight = db.Column(db.Text)
    body = db.Column(db.Text)
    document_id = db.Column(db.Integer, db.ForeignKey('docs.id'))

    def __repr__(self):
        return '<Note %r>' % self.id
