from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateTimeField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo
from flask_wtf.file import FileField
from wtforms_sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message="invalid email"), Length(max=50)])
    password = StringField('password', validators=[InputRequired(), Length(min=4, max=80)])


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(), Length(4, 80)])
    email = StringField('email', validators=[InputRequired(), Email(message="invalid email"), Length(max=50)])
    about = TextAreaField('About Author')
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password must match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    profile_pic = FileField('Profile Pic')
    submit = SubmitField("Submit")

class PredictForm(FlaskForm):
    ItemIdentifier = StringField("Item Identifier", validators=[DataRequired()])
    Item_Weight = FloatField("Item_Weight", validators=[DataRequired()])
    Item_Fat_Content = StringField('Item_Fat_Content', validators=[DataRequired()])
    Item_Visibility = FloatField("Item_Visibility", validators=[DataRequired()])
    Item_Type = StringField("Item_Type", validators=[DataRequired()])
    Item_MRP = FloatField("Item_MRP", validators=[DataRequired()])
    Outlet_Identifier = StringField("Outlet_Identifier", validators=[DataRequired()])
    Outlet_Size = StringField("Outlet_Size", validators=[DataRequired()])
    Outlet_Location_Type = StringField("Outlet_Location_Type", validators=[DataRequired()])
    Outlet_Type = StringField("Outlet_Type", validators=[DataRequired()])
    submit = SubmitField("Predict")