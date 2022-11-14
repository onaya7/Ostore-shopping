import os
import hmac
import hashlib
import json
import requests
import uuid
from flask_login import current_user, user_accessed
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
    current_app,
    jsonify,
)
from werkzeug.utils import secure_filename
from myapp.models import db, Product, Cart, User, Categories
from myapp.user import getLoginDetails


product = Blueprint("product", __name__, static_folder="static")


@product.route("/product")
def products():
    rows = Product.query.all()
    return render_template("product/products.html", rows=rows)

@product.route("/product<int:id>")
def singleproduct(id):
    rows = Product.query.filter_by(id=id).first()
    return render_template("product/single_product.html", rows=rows)

@product.route("/category/<int:id>")
def single_category(id):
    rows =Categories.query.filter_by(id=id).first()
    rows = rows.product
    return render_template("product/single_category.html", rows=rows)

# query product  by category route
@product.route("/category/men")
def men():
    men=Categories.query.filter_by(name='men').first()
    men = men.product
    return render_template("product/men.html", men=men)

@product.route("/category/women")
def women():
    women = Categories.query.filter_by(name='women').first()
    women = women.product
    return render_template("product/women.html", women=women)

@product.route("/category/kids")
def kids():
    kids = Categories.query.filter_by(name='kids').first()
    kids = kids.product
    return render_template("product/kids.html")

@product.route("/category/sneakers")
def sneakers():
    sneakers = Categories.query.filter_by(name='sneakers')
    sneakers = sneakers.product
    return render_template("product/sneakers.html")

@product.route("/category/heels")
def heels():

    return render_template("product/heels.html")

@product.route("/category/watches")
def watches():

    return render_template("product/watches.html")
# query product  by category route ends......
# ----------------------------

def get_categories(name):
    categories=Categories.query.filter_by(name=name).first()
    category_id =categories.id
    return category_id


      
    


@product.route("/addproduct", methods=["GET", "POST"])
def add_product():
    cat = Categories.query.all()
    if request.method == "POST":
        image = request.files["image"]
        filename = str(uuid.uuid1()) + os.path.splitext(image.filename)[1]
        print(filename)
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], secure_filename(filename)
        )
        save_file=image.save(file_path)
        print(save_file)
       
        
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        categories = request.form.get("categories")
        categories = get_categories(categories)
       
        new_pro = Product(name=name, price=price, filename=filename, description=description, categories_id=categories)
        db.session.add(new_pro)
        db.session.commit()
        flash(f"A new product has been added sucessfully", 'success')
        return redirect(url_for("product.add_product"))
    return render_template("product/addproduct.html " ,cat=cat)


@product.route("/media/<path:filename>")
def media(filename):
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )

@product.route("/editproduct<int:id>", methods=["GET", "POST"])
def edit_product(id):
    cat = Categories.query.all()
    rows = Product.query.filter_by(id=id).first()
    if request.method == "POST":
      
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        categories = request.form.get("categories")
        categories = get_categories(categories)

        rows.name = name
        rows.price = price
        rows.description=description
        rows.categories_id= categories
        
        db.session.commit()
        flash(f"Product {rows.id} has been edited")
        return redirect(url_for("product.edit_product", id=id))
    return render_template("product/editproduct.html", rows=rows, cat=cat)


@product.route("/delete/<int:id>")
def delete_product(id):
    rows = Product.query.get(id)
    db.session.delete(rows)
    db.session.commit()
    return redirect(url_for("product.products"))


############ Paystack api product#################


@product.route("/checkout_paystack", methods=["POST", "GET"])
def checkout():
    paystack_pk = os.getenv("PAYSTACK_PUBLIC_KEY")

    return render_template("store/paystack.html", paystack_pk=paystack_pk)


@product.route("/verify_paystack/<int:reference>", methods=["POST", "GET"])
def paystack_callback(reference):
    reference = requests.get("reference")
    print(reference)
    url = f"http://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
        "Content-Type": "application/json; charset=utf-8",
        "Accepts": "text/html",
    }
    response = requests.get(url=url, headers=headers)
    response = response.json()
    if response["status"] and response["data"]["status"] == "success":
        return jsonify({"status": True}, status=200)
    return jsonify({"status": False}, status=400)


@product.route("/webhook_paystack", methods=["POST"])
def paystack_webhook():
    json_body = request.get_json()
    data = json_body["data"]
    computed_hmac = hmac.new(
        bytes(os.getenv("PAYSTACK_SECRET_KEY"), "utf-8"),
        str.encode(request.get_data().decode("utf-8")),
        digestmod=hashlib.sha512,
    ).hexdigest()
    sig_header = request.headers.get("x-paystack-signature")
    if sig_header == computed_hmac:
        if json_body["event"] == "charge.success":
            data = json_body["data"]
            email = data["metadata"]["custom_fields"][0]["variable_name"]
            user = User.query.filter_by(email=email).first()
            print(user)
            user = user.id
            print(user)
            cart = Cart.query.filter_by(user_id=user).first()
            print(cart)
            cart_user=cart.user_id
            print(cart)

            
            if data["status"] == 'success':
                cart = Cart.query.filter_by(user_id=cart_user).first()
                cart.is_processed = int(True)
                db.session.commit()

        else:
            print("Unhandled event type {}".format(json_body["event"]))
    return jsonify(success=True)
