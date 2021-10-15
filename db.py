from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app


URI = getenv('DATABASE_URL')

if URI.startswith('postgres://'):
    URI = URI.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)

# get rid of error message when starting server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
