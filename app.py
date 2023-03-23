from flask import Flask, render_template, flash, request, redirect, url_for, session
from webforms import LoginForm, RegisterForm
from flask_bootstrap import Bootstrap
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/harendrakumar/Documents/bigmart/database.db'
app.config['SECRET_KEY'] = 'mysecretkeyforme'
db = SQLAlchemy(app=app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    joining_date = db.Column(db.DateTime, default = datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if user := User.query.filter_by(username=form.username.data).first():
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('about'))
            else:
                flash("wrong password")
        else:
            flash("Invalid username")

    return render_template('login.html', form=form)
    
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username= form.username.data, email= form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for("home"))
    return render_template('signup.html', form=form)


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))