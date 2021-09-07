from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Tervetuloa Kimppaveneeseen'

@app.route('/login')
def login():
    return ''