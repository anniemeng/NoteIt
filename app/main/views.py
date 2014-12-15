from flask import flash, render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User, Document
from .forms import LoginForm, DocumentForm, NoteForm
from . import main
from flask.ext.login import login_user, login_required, current_user, logout_user
import requests
from werkzeug.datastructures import ImmutableMultiDict

from ..retrievePage import retrieve_text

@main.route('/')
@main.route('/index')
def index():
    return render_template('main/landing.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    app = current_app._get_current_object()
    form = LoginForm(CSRF_ENABLED=app.config['WTF_CSRF_ENABLED'])
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.menu'))
        flash('Invalid username or password.')
    return render_template('main/login.html', form=form)


@main.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    form = DocumentForm()
    if form.validate_on_submit():
        content = retrieve_text(form.data['url'])
        title = form.data['title']
        descrip = form.data['descrip']
        return redirect(url_for('main.document', content=content, title=title, description=descrip))
    return render_template('main/menu.html', user=current_user, form=form)


@main.route('/document', methods=['GET', 'POST'])
@login_required
def document():
    orig = request.args.get('content')
    content = orig.split("\n\n")
    title = request.args.get('title')
    descrip = request.args.get('description')
    form = NoteForm()
    if form.validate_on_submit():
        current_user.add_doc(title, descrip, orig, form.data['note'], form.data['highlight'])
    return render_template('main/document.html', user=current_user, content=content, form=form)


@main.route('/document/<document_id>', methods=['GET','POST'])
@login_required
def doc(document_id):
    document = Document.query.get(document_id)
    content = document.article.split("\n\n")
    notes = document.notes
    highlights = []
    for note in notes:
        highlight = note.highlight.split("\s+");
        for hl in highlight:
            highlights.append(hl.replace('\n', '\\n'));
    return render_template('main/view.html', user=current_user, document=document, content=content, notes=notes, highlights=highlights)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
