from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv, environ

# database configurations

# development
# app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ohyvnilgnbwrpa:10fdd44d77a8fed845a712f37a4a8b9aa46068b147e1bf36a7d5ca2ea3f7359e@ec2-44-198-151-32.compute-1.amazonaws.com:5432/d3utq4fl0ipuuj'

db = SQLAlchemy(app)

# get rid of error message when starting server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
