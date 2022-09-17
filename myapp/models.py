from re import T
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy()

# Admin model
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False)
    lastname = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), nullable=False)

def __repr__(self):
        return f"User('{self.name}','{self.email}', '{self.id}')"

#User model
class  User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False)
    lastname = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), nullable=False)
    cart = db.relationship("Cart", back_populates="user", lazy=True)

    def add_to_cart(self, product_id):
        # p = Product(id=self.id)
        p = Product.query.filter_by(id=self.id).first()
        c = Cart(product_id=product_id, user_id=self.id)
        line_item = LineItem(product_id=product_id)
        c.line_items.append(line_item)
        db.session.add(c)
        db.session.commit()
        flash("Your item has been added to your cart!", "sucess")

    def __repr__(self):
        return f"User('{self.firstname}','{self.email}', '{self.id}')"


class LineItem(db.Model):
    __tablename__ = "line_items"
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, ForeignKey("cart.id"), nullable=True)
    product_id = db.Column(db.Integer, ForeignKey("product.id"), nullable=True)
    price = db.Column(db.Float)
    cart = db.relationship("Cart", back_populates="line_items")
    product = db.relationship("Product", back_populates="carts")


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey("product.id"), nullable=False)
    line_items = db.relationship("LineItem", back_populates="cart")
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="cart")
    quantity = db.Column(db.Integer, nullable=False, default=1)
    is_open = db.Column(db.Boolean, default=False, nullable=False)
    is_processed = db.Column(db.Boolean, default=False, nullable = False)

    def __repr__(self):
        return f"Cart('id:{self.id}','user_id:{self.user_id}')"


class Product(db.Model):

    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    price =  db.Column(db.String(78), nullable=True)
    
    filename = db.Column(
        db.String(89),
        nullable=True,
    )
    carts = db.relationship("LineItem", back_populates="product")

    def __repr__(self):
        return f"Product('id:{self.id}')"


class CustomerInfo:
    __tablename__ = "CustomerInfo"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    address = db.Column(db.String(500), nullable=False)
