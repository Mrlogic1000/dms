from flask import Flask, render_template, request, session, redirect, url_for, flash
from .extensions import mysql,migrate, bcrypt,ma
from dotenv import load_dotenv
from flask_cors import CORS


from os import environ
from os import path

load_dotenv()

BASE_DIR =path.abspath(path.dirname(__file__))

def get_settings():
    return environ.get('SETTINGS')

def create_app():

    app = Flask(__name__)
    CORS(app)

    app.config.from_object(get_settings())

    # db.init_app(app)
    mysql.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    # migrate.init_app(app,db)
    
    

    # from . import models
    
    from .api import api
    from .home import home

    app.register_blueprint(home,url_prefix='/')    
   
    app.register_blueprint(api, url_prefix='/api' )

   


    return app








