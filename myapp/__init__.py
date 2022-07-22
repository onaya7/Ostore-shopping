import os
from flask import Flask
from myapp.admin import admin
from myapp.user import user
from myapp.charge import charge
from myapp.instance import login_manager ,bcrypt, mail ,migrate
from myapp.models import db
from myapp.models import User
from myapp.product import product
from myapp.config import Config
from paystackapi.paystack import Paystack



#"""Application-factory pattern"""
def create_app(config_name= Config):
        #BLUEPRINTS REGISTRATION
        app = Flask(__name__, instance_relative_config=True, static_url_path="/static", static_folder="static")
       
        app.register_blueprint(admin, url_prefix='/')
        app.register_blueprint(product)
        app.register_blueprint(user)
        app.register_blueprint(charge)
        app.config.from_object(Config)
        
        ##DATABASE CONFIG
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'media/images/')       
        app.config['ALLOWED_EXTENSIONS'] = ['jpg', 'png']

        # initializing bcrypt
        bcrypt.init_app(app)
        #initializing flask-mail
        mail.init_app(app)
        ##initializing flask-migrate
        migrate.init_app(app,db)
        ##initializing flask login

        # initializing db
        db.init_app(app)
        login_manager.login_view = 'user.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
       

          # ##### PAYSTACK #####
        # app.config['PAYSTACK_SECRET_KEY'] = 'sk_test_6a9390b7f01159126150071a6b2b584cb5b8766a'
        # app.config['PAYSTACK_PUBLIC_KEY'] = 'pk_test_0ecf4e6c096500b78cdd3681b282269385cbde9d'
        # paystack = Paystack(secret_key= app.config['PAYSTACK_SECRET_KEY'])
        # # to use transaction class
        # paystack.transaction.list()
        app.config['MAIL_USE_TLS'] = True       
        app.config['MAIL_USE_SSL'] = False

        return app
