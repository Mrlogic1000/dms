from flask import Blueprint


home = Blueprint('/',__name__)
from . import route