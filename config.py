import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG=False
    TESTING=False
    CSRF_ENABLED=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # see .env to set /.env to set these variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    UPLOAD_FOLDER = '/app/static/uploads'
    # ACCEPTABLE_FILE_TYPES is referenced in forms.py / UploadFileForm.
    # when necessary, can break into ACCEPTABLE_AUDIO_TYPES, ACCEPTABLE_IMAGE_TYPES, etc.
    ACCEPTABLE_FILE_TYPES = ['image/png', 'image/jpg', 'image/jpeg', 'audio/wav', 'audio/mp3']
    ADMINS = ['<email-addresses-of-admins']
