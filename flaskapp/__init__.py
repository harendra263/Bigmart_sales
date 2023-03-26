from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/harendrakumar/Documents/bigmart/flaskapp/database.db'
app.config['SECRET_KEY'] = 'mysecretkeyforme'
db = SQLAlchemy(app=app)
Bootstrap(app)

from flaskapp import routes