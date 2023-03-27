from flask import Flask, render_template, flash, request, redirect, url_for, session
from .webforms import LoginForm, RegisterForm, UserForm, PredictForm
from .models import User, Predict
from flaskapp import db
from flaskapp import app
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from src.pipeline.predict import CustomData, PredictPipeline




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




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
                user.update_login()
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
    form = UserForm()
    user_id = current_user.id
    name = User.query.get(user_id)
    return render_template('about.html', name=name)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        current_user.update_logout()
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
            Item_Identifier= request.form['Item_Identifier'],
            Item_Weight= request.form['Item_Weight'],
            Item_Fat_Content= request.form['Item_Fat_Content'],
            Item_Visibility = request.form['Item_Visibility'],
            Item_Type = request.form['Item_Type'],
            Item_MRP = request.form['Item_MRP'],
            Outlet_Identifier= request.form['Outlet_Identifier'],
            Outlet_Size= request.form['Outlet_Size'],
            Outlet_Location_Type= request.form['Outlet_Location_Type'],
            Outlet_Type= request.form['Outlet_Type'],
            Prediction = results[0],
            user_id = user_id
        )
        db.session.add(data_db)
        db.session.commit()

        return render_template('predict.html',form=form, results = results[0])
    
    # Add a default return statement here
    return render_template('predict.html', form=form)

