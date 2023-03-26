from flaskapp import db
from flask_login import UserMixin
from datetime import datetime


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
