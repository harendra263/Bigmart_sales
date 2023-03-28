from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateTimeField, TextAreaField, FloatField, ValidationError
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectField
from .models import item_identifier, fat_content, store_identifier, outlet_type, location_type, item_type, outlet_size
from .models import User, ItemIdentifier, FatContent, OutletType, StoreIdentifier, OutletSize, LocationType, ItemType


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
    Item_Identifier = QuerySelectField("Item Identifier", validators=[DataRequired()], query_factory=item_identifier, allow_blank=False, get_label='item_name')
    Item_Weight = FloatField("Item Weight", validators=[DataRequired()])
    Item_Fat_Content = QuerySelectField('Item Fat Content', validators=[DataRequired()], query_factory=fat_content, allow_blank=False, get_label='Content')
    Item_Visibility = FloatField("Item Visibility", validators=[DataRequired()])
    Item_Type = QuerySelectField("Item Type", validators=[DataRequired()], query_factory=item_type, allow_blank=False, get_label='Item_Type')
    Item_MRP = FloatField("Item MRP", validators=[DataRequired()])
    Outlet_Identifier = QuerySelectField("Outlet Identifier", validators=[DataRequired()], query_factory=store_identifier, allow_blank=False, get_label='store_name')
    Outlet_Size = QuerySelectField("Outlet Size", validators=[DataRequired()], query_factory=outlet_size, allow_blank=False, get_label='Outlet_Size')
    Outlet_Location_Type = QuerySelectField("Outlet Location Type", validators=[DataRequired()], query_factory=location_type, allow_blank=False, get_label='Location_Type')
    Outlet_Type = QuerySelectField("Outlet Type", validators=[DataRequired()], query_factory=outlet_type, allow_blank=False, get_label='Outlet_Type')
    submit = SubmitField("Predict")


class UpdateAccountForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(label='Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            if user := User.query.filter_by(username=username.data).first():
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            if user := User.query.filter_by(email=email.data).first():
                raise ValidationError('That email is taken. Please choose a different one.')
    