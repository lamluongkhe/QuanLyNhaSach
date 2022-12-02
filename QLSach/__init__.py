from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary


app=Flask(__name__)
app.secret_key='asdfasfewfasdffdsg4sdf'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/book01?charset=utf8mb4" %quote('123456789')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["CART_KEY"] = 'cart'


cloudinary.config(cloud_name='dfmwmngkc',api_key='426292114139152',api_secret='nuFlkbWPJSTneEpfcaaKlXafjDU')

db=SQLAlchemy(app=app)

login=LoginManager(app=app)

babel=Babel(app=app)

@babel.localeselector
def load_locale():
    return 'vi'
