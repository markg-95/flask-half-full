from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import init_app

app = init_app()
from app import routes, errors

if __name__ == '__main__':
    app.run()
