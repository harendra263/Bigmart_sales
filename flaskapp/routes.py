from flask import Flask, render_template, flash, request, redirect, url_for, session
from .webforms import LoginForm, RegisterForm, UserForm, PredictForm, UpdateAccountForm
from .models import User, Predict
from flaskapp import db
from flaskapp import app
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from src.pipeline.predict import CustomData, PredictPipeline
import secrets
from PIL import Image


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
                flash("Login Succesful", category="success")
                return redirect(url_for('about'))
            else:
                flash("wrong password", category="danger")
                return redirect(url_for('login'))
        else:
            flash("Invalid username", category="danger")
            return redirect(url_for('login'))
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


@app.route('/profile')
@login_required
def profile():
    form = UserForm()
    user_id = current_user.id
    name = User.query.get_or_404(user_id)
    image_file = url_for(
        'static', filename=f'profile_pics/{current_user.profile_pic}'
    )
    return render_template('cards.html', form=form, name=name, id=user_id, image_file=image_file)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename=f'profile_pics/{current_user.profile_pic}'
    )
    return render_template('profile.html', form=form, title='Account', image_file=image_file)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Grab all the users from the database"""
    user = User.query.all()
    image_file = url_for(
        'static', filename=f'profile_pics/{current_user.profile_pic}'
    )
    return render_template('admin.html', name=user, image_file=image_file)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UpdateAccountForm()
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.username = request.form['username']
        user.email = request.form['email']
        try:
            db.session.commit()
            flash("Account has been updated!", "success")
            return redirect(url_for('update', id = user.id))
        except Exception:
            return "An error"
    elif request.method == "GET":
        form.username.data = user.username
        form.email.data = user.email
    return render_template('update.html', form=form, user=user)



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

