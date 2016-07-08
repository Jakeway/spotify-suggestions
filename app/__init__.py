from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import os
from redis import Redis
from flask.ext.session import Session


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
Bootstrap(app)
lm = LoginManager()
lm.login_view = 'index.html'
lm.init_app(app)
redis_host = app.config['REDIS_HOST']
redis_port = app.config['REDIS_PORT']
redis_password = app.config['REDIS_PASSWORD']
redis_conn = Redis(host=redis_host, port=redis_port, password=redis_password)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_conn
Session(app)

from app import views, models
