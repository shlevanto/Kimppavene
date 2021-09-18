from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

# database configurations
uri = getenv('DATABASE_URL')

# SQLAlchemy 1.4.x does not support postgres:// uri scheme
# it has to be changed to postgresql://

if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri 
db = SQLAlchemy(app)

# get rid of error message when starting server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
