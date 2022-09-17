# Ostore-shopping
An ecommerce website using flask ( Python web framework)



![Screenshot (3)](https://user-images.githubusercontent.com/63925047/166123163-e4ec22f5-89d3-4554-ad39-a1fd659e38a4.png)
![Screenshot (4)](https://user-images.githubusercontent.com/63925047/166123168-3bdc6af0-2931-4b7b-8f7e-843193ca3c80.png)
![Screenshot (5)](https://user-images.githubusercontent.com/63925047/166123169-d17998e1-1e56-47b3-b210-310f12b48d68.png)

## Focus

On this project I focused on implementing a shopping cart, a Paystack API webhook endpoint to receive events that 
happens from my account to my application and a payment method 

## Features
An Authentication system
- Login
- Registration
- Logout
- Password Reset

A Dashboard 
- Of new products
-To create Users

A Cart System
- To allow users persist orders over sessions
- To close a cart via an order event
- A checkout system (Using Paystack Payment Gatway)
- Product list view for users
- Add to cart and cart preview view

## Event 
Once logged in, users can:
- Add products to their shopping cart 
- Update the quantity, or Remove items
- See the total cost.
- Trigger a checkout by event
- Make payment
- Logout
## How to run this application locally

To install all the packages, run:

```
pip3 install -r requirements.txt

```    

create a .flaskenv and include:

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=TRUE

```

In your config.py include:

```
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(os.getenv('DEBUG'))
   
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
SQLALCHEMY_DATABASE_URI= os.getenv('SQLALCHEMY_DATABASE_URI')

ALLOWED_EXTENTIONS =['jpg', 'png']

MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')  
MAIL_USE_TSL= bool(os.getenv('MAIL_USE_TSL'))
MAIL_USE_SSL= bool(os.getenv('MAIL_USE_SSL'))
MAIL_USERNAME=os.getenv('MAIL_USERNAME')
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER= os.getenv('MAIL_DEFAULT_SENDER')

PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')

```
and create a .env file to include enviroment variables

Then run:

```
flask run

```

## Resources
-   Flask/SQLAlchemy documentation
https://flask-sqlalchemy.palletsprojects.com/en/2.x/


