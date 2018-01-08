from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from flask_pymongo import PyMongo


bootstrap = Bootstrap()
mail = Mail()
mongo = PyMongo()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    MONGO_PORT = 83
    MONGODB = '/myflix'
    app.config['MONGO_DBNAME'] = 'myflix'
    req_MONGO = urllib.request.Request('https://enabledns.com/ip')
    with urllib.request.urlopen(req_MONGO) as response:
        MONGO_PAGE = response.read()
    IP_MONGO = MONGO_PAGE[2:15]
    app.config['MONGO_URI'] = 'mongodb://%s:%s%s'%(IP_MONGO, MONGO_PORT, MONGODB)
    
    bootstrap.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
