from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow


# db = SQLAlchemy()
migrate = Migrate()

mysql = MySQL()

bcrypt = Bcrypt()
ma = Marshmallow()
