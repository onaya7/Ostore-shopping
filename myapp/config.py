# Define the application directory
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
     # Statement for enabling the development environment
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = bool(os.getenv('DEBUG'))
   

    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_DATABASE_URI= os.getenv('SQLALCHEMY_DATABASE_URI')
    
    ALLOWED_EXTENTIONS =['jpg', 'png']
    
     #Mails
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')  
#   MAIL_USE_TSL= bool(os.getenv('MAIL_USE_TSL'))
#   MAIL_USE_SSL= bool(os.getenv('MAIL_USE_SSL'))
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER= os.getenv('MAIL_DEFAULT_SENDER')

    PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
    PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')