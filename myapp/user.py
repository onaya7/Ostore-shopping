import os
from flask_login import login_user, login_required, current_user, logout_user
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    jsonify,
)
from flask_mail import Message
from myapp.models import db, User, Cart, Product
from myapp.forms import  RegistrationForm, LoginForm, UpdateAccountForm, EmailForm, PasswordForm
from myapp.instance import bcrypt , mail
from myapp.util import ts
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired
import smtplib
import ssl
from email.message import EmailMessage



user = Blueprint("user", __name__ , static_folder="static")

# Home route
@user.route("/")
@user.route("/home")

def home():
    
    return render_template("store/home.html")
    
@user.route("/about")
def about():
    # noOfItems = getLoginDetails()
    return render_template("store/about.html")
@user.route("/contact")
def contact():
    # noOfItems = getLoginDetails()
    return render_template("store/contact.html")

# Registration route
@user.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=hashed_password,
        )
        
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for("user.login"))
    return render_template(
        "user/signup.html",
        title="Register",
        form=form,
    )


# Login route
@user.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("user.home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("user/login.html", title="Login", form=form)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.home"))


@user.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("user.profile"))
    elif request.method == "GET":
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
    return render_template("store/profile.html", title="Account", form=form)


@user.route("/reset", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("user.home"))

    form = EmailForm()
    if form.validate_on_submit():
        # verify if user exists
        email = User.query.filter_by(email=form.email.data).first()
        form_mail = form.email.data

        # sending the email confirmation link
        token = ts.dumps(form_mail, salt="password-reset-salt")

        recover_url = url_for("user.token_reset", token=token, _external=True)
        
        email_username = os.getenv("MAIL_USERNAME")
        email_password =  os.getenv("MAIL_PASSWORD")
        # email_default_sender = os.getenv("MAIL_DEFAULT_SENDER")
        email_receiver = form_mail

        subject = "Ostore Reset password request"
        body = f"To reset the password to continue shopping with Ostore click the link below:{recover_url}"
        em = EmailMessage()
        em['From'] = email_username
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)


        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_username, email_password)
            smtp.sendmail(email_username, email_receiver, em.as_string())
            
        flash(
            "An email has been sent with instructions to reset your password.", "info"
        )
        return redirect(url_for("user.reset_password"))
    return render_template("user/reset_password.html", form=form)


@user.route("/reset/<token>", methods=["POST","GET"])
def token_reset(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('users.home'))
    try:
        # token generated
        email = ts.loads(token, salt="password-reset-salt", max_age=200)
    except SignatureExpired:
        flash("The password reset link is invalid or has expired.", "warning")
        return redirect(url_for("user.login"))
    form = PasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8" )
        print(hashed_password)
        user = User.query.filter_by(email=email).first()
        print(user)
        user.password=hashed_password
        print(user.password)
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("user.login"))
    return render_template("user/reset_with_token.html", token=token, form=form)


##### USERS CART ROUTE ####

def getLoginDetails():
    if current_user.is_authenticated:
        noOfItems = Cart.query.filter_by(user=current_user).first()
    else:
        noOfItems = 0

    return noOfItems


@user.route("/process_quantity", methods=["POST"])
def process_quantity():
    quantity = int(request.form.get("quantity"))
    print(quantity)
    return jsonify({'message': 'Quantity updated successfully'})

def update_cart_item(product_id, quantity):
    cart_item = Cart.query.filter_by(product_id=product_id, user=current_user).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
        flash("This item is already in your cart, quantity updated!", "success")
    else:
        user = User.query.get(current_user.id)
        user.add_to_cart(product_id, quantity)

@user.route("/addToCart/<int:product_id>", methods=["POST"])
@login_required
def addToCart(product_id):
    quantity = int(request.form.get("quantity"))
    update_cart_item(product_id, quantity)
    return redirect(url_for("product.products"))

def get_cart_items():
    cart = (
        Product.query.join(Cart)
        .add_columns(
            Cart.quantity, Product.price, Product.name, Product.id, Product.filename
        )
        .filter_by(user=current_user)
        .all()
    )
    return cart

def calculate_subtotal(cart):
    subtotal = sum(int(item.price) * int(item.quantity) for item in cart)
    return subtotal

@user.route("/carts", methods=["GET", "POST"])
@login_required
def carts():
    paystack_pk = os.getenv("PAYSTACK_PUBLIC_KEY")
    noOfItems = getLoginDetails()
    user = User.query.filter_by(id=current_user.id).first()
    email = user.email
    name = user.firstname
    cart = get_cart_items()
    subtotal = calculate_subtotal(cart)
    
    if request.method == "POST":
        qty = request.form.get("qty")
        idpd = request.form.get("idpd")
        update_cart_item(idpd, qty)
        cart = get_cart_items()
        subtotal = calculate_subtotal(cart)
        print(email)
        
    return render_template(
        "store/carts.html", cart=cart, noOfItems=noOfItems, subtotal=subtotal, paystack_pk=paystack_pk, email=email, name=name
    )


@user.route("/removeFromCart/<int:product_id>")
@login_required
def removeFromCart(product_id):
    item_to_remove =Cart.query.filter_by(user=current_user).first()
    print(item_to_remove)
    db.session.delete(item_to_remove)
    db.session.commit()
    flash("Your item has been removed from your cart!", "success")
    return redirect(url_for("user.carts"))
    


