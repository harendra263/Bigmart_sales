from flask import Flask, render_template, flash, request, redirect, url_for, session
from webforms import LoginForm, RegisterForm, UserForm, PredictForm
from flask_bootstrap import Bootstrap
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from src.pipeline.predict import CustomData, PredictPipeline

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

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"

class Predict(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    Item_Identifier = db.Column(db.String(15), unique=True, nullable=False)
    Item_Weight = db.Column(db.Numeric(10, 3), nullable=False)
    Item_Fat_Content = db.Column(db.String(15), nullable=False)
    Item_Visibility = db.Column(db.Numeric(10, 3), nullable=False)
    Item_Type = db.Column(db.String(15), nullable=False)
    Item_MRP = db.Column(db.Numeric(10, 3), nullable=False)
    Outlet_Identifier = db.Column(db.String(15), unique=True, nullable=False)
    Outlet_Size = db.Column(db.String(15), nullable=False)
    Outlet_Location_Type = db.Column(db.String(15), nullable=False)
    Outlet_Type = db.Column(db.String(15), nullable=False)
    Prediction = db.Column(db.Numeric(10, 3), nullable=False)


class ItemIdentifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50),unique=True)


class StoreIdentifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(50),unique=True)

class FatContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Content = db.Column(db.String(50), unique=True)

class OutletType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Outlet_Type = db.Column(db.String(50), unique=True)

class LocationType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Location_Type = db.Column(db.String(50), unique=True)



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


@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    form = UserForm()
    user_id = current_user.id
    name_to_update = User.query.get_or_404(user_id)


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    form = PredictForm()
    user_id = current_user.id
    if request.method == "GET":
        return render_template("home.html")
    if form.validate_on_submit():
        data = CustomData(
            Item_Identifier= form.Item_Identifier.data,
            Item_Weight= form.Item_Weight.data,
            Item_Fat_Content= form.Item_Fat_Content.data,
            Item_Visibility = form.Item_Visibility.data,
            Item_Type = form.Item_Type.data,
            Item_MRP = form.Item_MRP.data,
            Outlet_Identifier= form.Outlet_Identifier.data,
            Outlet_Type= form.Outlet_Type.data,
            Outlet_Location_Type= form.Outlet_Location_Type.data,
            Outlet_Size= form.Outlet_Size
        )
        pred_df = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        data_db = Predict(
            user_id = user_id,
            Item_Identifier= form.Item_Identifier.data,
            Item_Weight= form.Item_Weight.data,
            Item_Fat_Content= form.Item_Fat_Content.data,
            Item_Visibility = form.Item_Visibility.data,
            Item_Type = form.Item_Type.data,
            Item_MRP = form.Item_MRP.data,
            Outlet_Identifier= form.Outlet_Identifier.data,
            Outlet_Size= form.Outlet_Size,
            Outlet_Location_Type= form.Outlet_Location_Type.data,
            Outlet_Type= form.Outlet_Type.data,
            Prediction = results
        )
        db.session.add(data_db)
        db.session.commit()

        return render_template('predict.html', results = results[0])