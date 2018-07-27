from flask import render_template, flash, redirect, url_for, request, g, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm
from .models import User
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from datetime import datetime
from flask_restful import Resource
import json


@app.route('/')
@app.route('/index')
@login_required
def index():
    books = [  # fake array of posts
        {
            'author': {'username': 'John'},
            'title': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'title': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    books = [  # fake array of posts
        {
            'author': {'username': 'John'},
            'title': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'title': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('user.html',
                           user=user,
                           books=books)
#
# @app.route('/search')
# def search():
#     # books = Book.query.all()
#     books = [  # fake array of posts
#         {
#             'author': {'username': 'John'},
#             'title': 'Beautiful day in Portland!'
#         },
#         {
#             'author': {'username': 'Susan'},
#             'title': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template('results.html', results=books)

class SearchResults(Resource):
    def get(self):
        books = [  # fake array of posts
            {
                'author': {'username': 'John'},
                'title': 'Beautiful day in Portland!'
            },
            {
                'author': {'username': 'Susan'},
                'title': 'The Avengers movie was so cool!'
            }
        ]
        return books, 200, {'Access-Control-Allow-Origin': '*'}

    def options (self):
        return {'Allow' : 'GET' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'GET' }
