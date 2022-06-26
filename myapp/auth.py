import os
from flask_login import login_user, login_required, current_user, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from myapp.models import db, User, Cart, Product, LineItem


auth = Blueprint("auth", __name__)


# @auth.route("/index")
# def index():

#     return render_template("store/index.html")


@auth.route("/")
@login_required
def profile():

    return render_template("store/profile.html", name=current_user.name)


@auth.route("/login")
def login():
    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("auth.profile"))


@auth.route("/signup")
def signup():
    return render_template("auth/signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database

    if (
        user
    ):  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for("auth.signup"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.profile"))


###### ADMIN #######


@auth.route("/Users")
def users():
    user = User.query.all()

    return render_template("main/users.html", title="Users", user=user)


@auth.route("/<int:user_id>/delete/")
def delete_users(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("auth.users", user_id=user_id))


##### CART ####


def getLoginDetails():
    if current_user.is_authenticated:
        noOfItems = Cart.query.filter_by(user=current_user).count()
    else:
        noOfItems = 0

    return noOfItems


@auth.route("/addToCart/<int:product_id>")
@login_required
def addToCart(product_id):

    row = Cart.query.filter_by(product_id=product_id, user=current_user).first()
    if row:
        # if in cart update quantity : +1
        row.quantity += 1
        db.session.commit()
        flash("This item is already in your cart, 1 quantity added!", "success")

        # if not, add item to cart
    else:
        user = User.query.get(current_user.id)
        user.add_to_cart(product_id)
    return redirect(url_for("product.products"))


@auth.route("/carts", methods=["GET", "POST"])
@login_required
def carts():
    noOfItems = getLoginDetails()
    # display items in cart
    cart = (
        Product.query.join(Cart)
        .add_columns(
            Cart.quantity, Product.price, Product.name, Product.id, Product.filename
        )
        .filter_by(user=current_user)
        .all()
    )

    subtotal = 0
    for item in cart:
        subtotal += int(item.price) * int(item.quantity)
    if request.method == "POST":
        qty = request.form.get("qty")
        idpd = request.form.get("idpd")
        cartitem = Cart.query.filter_by(product_id=idpd).first()
        cartitem.quantity = qty
        db.session.commit()
        cart = (
            Product.query.join(Cart)
            .add_columns(
                Cart.quantity, Product.price, Product.name, Product.id, Product.filename
            )
            .filter_by(user=current_user)
            .all()
        )
        subtotal = 0
        for item in cart:
            subtotal += int(item.price) * int(item.quantity)
    return render_template(
        "store/carts.html", cart=cart, noOfItems=noOfItems, subtotal=subtotal
    )


@auth.route("/removeFromCart/<int:product_id>")
@login_required
def removeFromCart(product_id):
    item_to_remove = LineItem.query.filter_by(product_id=product_id).first()
    print(item_to_remove)
    db.session.delete(item_to_remove)
    db.session.commit()
    flash("Your item has been removed from your cart!", "success")
    return redirect(url_for("auth.carts"))
