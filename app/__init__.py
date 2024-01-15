from flask import Flask
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment


app = Flask(__name__)

moment = Moment(app)

app.config["SQLALCHEMY_DATABASE_URI"] = ("mysql+pymysql://root:%s@localhost/flightapp?charset=utf8mb4"
                                         % quote('nam123'))

app.secret_key = 'dsaplqwfnhqwoprfpwqjpeojsqpfjaswqojk@#$%^&*()_+'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(cloud_name='djncibcll',
                  api_key='662432432768125',
                  api_secret='RYig-mSAge5NejSxN0QwxgH4AQI')


