from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask import flash

from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


# Models


class Admin(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


def __repr__(self):
    return f"<Admin {self.id}>"


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    cart = db.relationship("Cart", back_populates="user", lazy=True)

    def add_to_cart(self, product_id):
        p = Product(id=self.id)
        c = Cart(product_id=product_id, user_id=self.id)
        line_item = LineItem(product_id=product_id)
        c.line_items.append(line_item)
        db.session.add(c)
        db.session.commit()
        flash("Your item has been added to your cart!", "sucess")

    def __repr__(self):
        return f"User('{self.name}','{self.email}', '{self.id}')"


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

    def __repr__(self):
        return f"Cart('id:{self.id}','user_id:{self.user_id}')"


class Product(db.Model):

    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    stripe_id = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.String(78), nullable=False)
    filename = db.Column(
        db.String(89),
        unique=True,
        nullable=False,
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
