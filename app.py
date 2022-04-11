# Import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CSRFProtect
# from datetime import timedelta

# Create new flask app
app = Flask(__name__)
# # Set browser expire time
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
# Config from settings.py
# app.config.from_object('settings')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app._static_folder = "./static"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Initiate DB
db = SQLAlchemy(app)
