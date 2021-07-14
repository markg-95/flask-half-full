from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

import os

"""
The following are globally used objects which get passed the instance of the app
after it is initialized.
"""

login_manager = LoginManager() # provides us user authentication, login/logout etc.
migrate = Migrate() # migrations for database structural changes
mail = Mail() # mail support
moment = Moment() # moment.js support

def init_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from app.models import db
    db.init_app(app)
    migrate.init_app(app=app, db=db, render_as_batch=True)

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    moment.init_app(app)

    app.config.update(dict(
        DEBUG=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    ))

    mail.init_app(app)
    moment.init_app(app)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='FlaskHalfFull Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/hannah_site.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('FlaskHalfFull startup')


    with app.app_context():
        db.create_all()
        return app