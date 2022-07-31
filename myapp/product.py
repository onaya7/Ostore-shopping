from math import prod
import os
import hmac
import hashlib
import json
import requests
from tkinter import image_types
import uuid
import stripe
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
from myapp.models import Product, db


product = Blueprint("product", __name__, static_folder="static")


@product.route("/product")
def products():
    rows = Product.query.all()
    return render_template("store/products.html", rows=rows)


@product.route("/product<int:id>")
def singleproduct(id):
    rows = Product.query.filter_by(id=id).first()

    return render_template("store/productdetails.html", rows=rows)


@product.route("/addproduct", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        image = request.files["image"]
        filename = str(uuid.uuid1()) + os.path.splitext(image.filename)[1]
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], secure_filename(filename)
        )
        name = request.form.get("name")
        price = request.form.get("price")

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

def save_image():
    image = request.files["image"]
    filename = str(uuid.uuid1()) + os.path.splitext(image.filename)[1]
    file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], secure_filename(filename)
        )
    image.save(file_path)

@product.route("/editproduct<int:id>", methods=["GET", "POST"])
def edit_product(id):

    rows = Product.query.filter_by(id=id).first()
    if request.method == "POST":
        image = request.files["image"]
        filename = str(uuid.uuid1()) + os.path.splitext(image.filename)[1]
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], secure_filename(filename)
        )
        image.save(file_path)

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


############ Stripe api product#################


@product.route("/v1/products", methods=["POST"])
def stripe_create_product():
    event = None
    payload = request.data
    sig_header = request.headers["STRIPE_SIGNATURE"]
    # endpoint_secret = current_app.config["WEBHOOK_SECRET_KEY"]
    endpoint_secret = "whsec_tIJsQPPo6b3YQnwbgRKcISjKnudNO0Zc"

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    print(event["type"])
    if event["type"] == "product.created":
        object = event["data"]["object"]
        product_id = object["id"]
        product = Product.query.filter_by(stripe_id=product_id).first()
        import uuid

        file = str(uuid.uuid1()) + ".png"
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file)
        images = requests.get(object["images"][0])
        save = open(file_path, "wb").write(images.content)
        if product:
            print("true")
            product.stripe_id = object["id"]
            product.name = object["name"]
            product.filename = file
            db.session.commit()
        else:
            print("false")
            p = Product(stripe_id=object["id"], name=object["name"], filename=file)
            db.session.add(p)
            db.session.commit()
    elif event["type"] == "price.created":
        price = event["data"]["object"]
        product_id = price["product"]
        print(product_id)
        product = Product.query.filter_by(stripe_id=product_id).first()
        if product:
            print("No")
            product.price = price["id"]
            db.session.commit()
        else:
            print("yes")
            prices = Product(stripe_id=price["product"], price=price["id"])
            db.session.add(prices)
            db.session.commit()

    elif event["type"] == "product.updated":
        product = event["data"]["object"]
    elif event["type"] == "product.deleted":
        product = event["data"]["object"]
    elif event["type"] == "price.deleted":
        price = event["data"]["object"]
    elif event["type"] == "price.updated":
        price = event["data"]["object"]

    # ... handle other event types
    else:
        print("Unhandled event type {}".format(event["type"]))

    return jsonify(success=True)


@product.route("/checkout_paystack", methods=["POST", "GET"])
def checkout():
    paystack_pk = os.getenv("PAYSTACK_PUBLIC_KEY")

    return render_template("store/paystack.html", paystack_pk=paystack_pk)


@product.route("/verify_paystack", methods=["POST","GET"])
def paystack_callback():
    reference = requests.get_json().get("reference")

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
            print(json_body["event"])

        else:
            print("Unhandled event type {}".format(json_body["event"]))
    return jsonify(success=True)
