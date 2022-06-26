import os
from flask import Flask
from myapp.admin import admin
from myapp.auth import auth, login
from flask_migrate import Migrate
from myapp.models import db
from flask_login import LoginManager
from myapp.models import User
from myapp.product import product
from myapp.config import Config
from paystackapi.paystack import Paystack













#"""Application-factory pattern"""
def create_app(config_name= Config):
        #BLUEPRINTS REGISTRATION
        app = Flask(__name__, instance_relative_config=True, static_url_path="/static", static_folder="static")
       
        app.register_blueprint(admin, url_prefix='/')
        app.register_blueprint(auth)
        app.register_blueprint(product)
        app.config.from_object(Config)
     

        
        
        ##DATABASE CONFIG
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] =\
                'sqlite:///' + os.path.join(basedir, 'app.db')
      
        app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'media/images/')       
        app.config['ALLOWED_EXTENSIONS'] = ['jpg', 'png']

        # ##### PAYSTACK #####
        # app.config['PAYSTACK_SECRET_KEY'] = 'sk_test_6a9390b7f01159126150071a6b2b584cb5b8766a'
        # app.config['PAYSTACK_PUBLIC_KEY'] = 'pk_test_0ecf4e6c096500b78cdd3681b282269385cbde9d'
        # paystack = Paystack(secret_key= app.config['PAYSTACK_SECRET_KEY'])
        # # to use transaction class
        # paystack.transaction.list()

      
        
        ##DATABASE MIGRATIONS
        migrate = Migrate()

        ##FLASK LOGIN LOADER
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.login_view
        login_manager.init_app(app)


        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))




        ##INITIALIZATIONS
        db.init_app(app)
        migrate.init_app(app, db)



        # if __name__ == '__main__':
        #         app.run(debug=True)
        return app
