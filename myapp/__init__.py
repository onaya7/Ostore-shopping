import os
from flask import Flask
from myapp.admin import admin
from myapp.auth import auth, login
from flask_migrate import Migrate
from myapp.models import db
from flask_login import LoginManager
from myapp.models import User













#"""Application-factory pattern"""
def create_app():
        #BLUEPRINTS REGISTRATION
        app = Flask(__name__, instance_relative_config=True)
        app.register_blueprint(admin, url_prefix='/')
        app.register_blueprint(auth)
     

        
        
        ##DATABASE CONFIG
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] =\
                'sqlite:///' + os.path.join(basedir, 'database.db')
        app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["DEBUG"] = True
        app.config['SECRET_KEY'] = 'ereryttfguguftdrdyg4e4325364@345'    

        ##DATABASE MIGRATIONS
        migrate = Migrate()

        from sqlalchemy import create_engine
        engine = create_engine( 'sqlite:///app.db')
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

    



        if __name__ == '__main__':
                app.run(debug=True)
        return app
