#Responsável pela criação do aplicativo, inicializa o BD
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt
import secrets

app = Flask(__name__)
# secret_key = secrets.token_hex(16) #Create HEX Key
# bcrypt = Bcrypt(app) #Init Bcrypt
# secret_key_hash = bcrypt.generate_password_hash(secret_key) #hash the HEX key with Bcrypt
app.config['SECRET_KEY'] = 'MinhaSenha' #secret_key_hash #setup secret key
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/salao'
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://okqwabkszrscvv:58ddc1ca23718b9ec14d0563fba1505bc3c30203f4ab6fd4806d5f309f49c2a3@ec2-44-199-22-207.compute-1.amazonaws.com:5432/d70bb2hn2m9roi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from app.controllers import main
from app.controllers import forms
