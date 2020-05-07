from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import urllib.request
<<<<<<< HEAD
UPLOAD_FOLDER = '\\static\\'
=======
UPLOAD_FOLDER = 'C:\\Users\\imeli\\OneDrive\\Documents\\CodingDojo\\Projects_Algos\\group_project\\static\\'

>>>>>>> 1560abe593965f9581040dc7495c562a15265dad


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neighborly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
app.secret_key= "jazz hands"
