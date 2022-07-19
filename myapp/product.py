import os
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
    jsonify
)
from werkzeug.utils import secure_filename
from myapp.models import Product, db



product = Blueprint("product", __name__ , static_folder="static")


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
        print(image)

        filename = str(uuid.uuid1())+os.path.splitext(image.filename)[1]
        print(image.filename)
        
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


############ Stripe api product#################

@product.route("/v1/products", methods=["POST"])
def stripe_create_product():
    event = None
    payload = request.data
    sig_header = request.headers["STRIPE_SIGNATURE"]
    # endpoint_secret = current_app.config["WEBHOOK_SECRET_KEY"]
    endpoint_secret = "whsec_zIHPWoLSFGvcWjOqbm3TWUXEvrJA6Q4G"

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
    if event['type'] == 'price.created':
      price = event['data']['object']
      price_id = price["id"]
      print(price_id)
    elif event['type'] == 'price.deleted':
      price = event['data']['object']
    elif event['type'] == 'price.updated':
      price = event['data']['object']
    elif event['type'] == 'product.created':
      product = event['data']['object']
      product_id = product["id"]
      print(product_id)
    elif event['type'] == 'product.deleted':
      product = event['data']['object']
    elif event['type'] == 'product.updated':
      product = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)


