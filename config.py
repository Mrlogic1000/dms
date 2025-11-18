from os import path, environ, getenv

BASE_DIR =path.abspath(path.dirname(__file__))





class Config:
    SECRET_KEY = 'key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Key@a1b2'
    MYSQL_DB = 'dms'
    MYSQL_CURSORCLASS = 'DictCursor'
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    UPLOAD_FOLDER = path.join(BASE_DIR,'static','images','portfolio')

    # MAIL_SERVER= getenv('MAIL_SERVER')
    # MAIL_PORT = getenv('MAIL_PORT')
    # MAIL_UserNAME = getenv('MAIL_UserNAME')
    # MAIL_PASSWORD= getenv('MAIL_PASSWORD')
    # MAIL_USE_TLS = getenv('MAIL_USE_TLS')
    # MAIL_USE_SSL = getenv('MAIL_USE_SSL')
