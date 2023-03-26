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
    Item_Weight = db.Column(db.Float, nullable=False)
    Item_Fat_Content = db.Column(db.String(15), nullable=False)
    Item_Visibility = db.Column(db.Float, nullable=False)
    Item_Type = db.Column(db.String(15), nullable=False)
    Item_MRP = db.Column(db.Float, nullable=False)
    Outlet_Identifier = db.Column(db.String(15), unique=True, nullable=False)
    Outlet_Size = db.Column(db.String(15), nullable=False)
    Outlet_Location_Type = db.Column(db.String(15), nullable=False)
    Outlet_Type = db.Column(db.String(15), nullable=False)
    Prediction = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Predict(Item_Identifier='{self.Item_Identifier}')>"


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

class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Item_Type = db.Column(db.String(50), unique=True)

class OutletSize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Outlet_Size = db.Column(db.String(50), unique=True)



def item_identifier():
    return ItemIdentifier.query.all()

def store_identifier():
    return StoreIdentifier.query.all()

def fat_content():
    return FatContent.query.all()

def outlet_type():
    return OutletType.query.all()

def location_type():
    return LocationType.query.all()

def item_type():
    return ItemType.query.all()


def outlet_size():
    return OutletSize.query.all()

