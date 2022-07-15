# Define the application directory
import os
from flask import current_app
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

base_dir = os.path.abspath(os.path.dirname(__file__)) 


class Config:
     # Statement for enabling the development environment
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = bool(os.getenv('DEBUG'))
   
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    ALLOWED_EXTENTIONS =['jpg', 'png']
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
    
    # Stripe CLI webhook secret for testing your endpoint locally.
    WEBHOOK_SECRET_KEY = os.getenv('WEBHOOK_SECRET_KEY')
    STRIPE_SIGNATURE = os.getenv('STRIPE_SIGNATURE ')
