from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_envvar('SPOTIFY_SETTINGS')
db = SQLAlchemy(app)
Bootstrap(app)
lm = LoginManager()
lm.init_app(app)

from app import views, models
