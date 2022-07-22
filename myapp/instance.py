from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate

# creating an instance of sqlalchemy
db = SQLAlchemy()

# creating an instance of Loginmanager
login_manager = LoginManager()

# creating an instance of bcrypt
bcrypt = Bcrypt()

# creating an instance of flask-mail
mail = Mail()


# creating an instance of flask-migrate
migrate = Migrate(db)
