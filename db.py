from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

# database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
db = SQLAlchemy(app)

# get rid of error message when starting server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
