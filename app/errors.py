from flask import render_template
from app.models import db
from wsgi import app

@app.errorhandler(404)
def not_found_error(error):
    print(error)
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    print(error)
    db.session.rollback()
    return render_template('error/500.html'), 500