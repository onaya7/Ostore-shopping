import os
import uuid
from myapp.auth import delete_users
from myapp.models import Product, db
from flask import (
    Flask,
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
    current_app,
)
from flask_session import Session
from werkzeug.utils import secure_filename
import stripe


product = Blueprint("product", __name__)


@product.route("/product")
def products():
    rows = Product.query.all()
    return render_template("store/products.html", rows=rows)


@product.route("/product<int:id>")
def singleproduct(id):
    rows = Product.query.filter_by(id=id).first()

    return render_template("store/productdetails.html", rows=rows)


@product.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        image = request.files['image']
        filename = str(uuid.uuid1())+os.path.splitext(image.filename)[1]
        
        file_path = (os.path.join(current_app.config['UPLOAD_FOLDER'],secure_filename(filename)))
        name = request.form.get('name')
        price = request.form.get('price')
        new_pro = Product(name=name, price=price, filename=filename)
        image.save(file_path)
        db.session.add(new_pro)
        db.session.commit()
        flash(f"A new product has been added sucessfully")
    return render_template("store/addproduct.html")


@product.route("/media/<path:filename>")
def media(filename):
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )


@product.route("/editproduct<int:id>", methods=["GET", "POST"])
def edit_product(id):
    rows = Product.query.filter_by(id=id).first()
    if request.method == "POST":
        image = request.files["image"]
        filename = str(uuid.uuid1()) + os.path.splitext(image.filename)[1]
        name = request.form.get("name")
        price = request.form.get("price")

        rows.filename = filename
        rows.name = name
        rows.price = price
        db.session.commit()
        flash(f"Product {rows.id} has been edited")
        return redirect(url_for("product.edit_product", id=id))
    return render_template("store/editproduct.html", rows=rows)


@product.route("/delete/<int:id>")
def delete_product(id):
    rows = Product.query.get(id)
    db.session.delete(rows)
    db.session.commit()
    return redirect(url_for("product.products"))

@product.route("/checkout", methods=["POST", "GET"])
def checkout():
   
    return render_template('store/checkout.html')

@product.route('/stripe_pay')
def stripe_pay():
    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1LEWFoKEds1x3dYFRUoQOx45',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('product.thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('product.checkout', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': current_app.config['STRIPE_PUBLIC_KEY']
    }

@product.route('/thanks')
def thanks():
    return render_template('store/thanks.html')

