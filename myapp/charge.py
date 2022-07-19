import os
import stripe
from flask import Blueprint,  render_template, redirect, url_for, request, flash, current_app, jsonify
   





charge = Blueprint("charge", __name__)


@charge.route("/stripe_pay")
def stripe_pay():
    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": "price_1LEWFoKEds1x3dYFRUoQOx45",
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=url_for("charge.thanks", _external=True)
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=url_for("user.cart", _external=True),
    )
    return {
        "checkout_session_id": session["id"],
        "checkout_public_key": current_app.config["STRIPE_PUBLIC_KEY"],
    }


@charge.route("/checkout")
def checkout():

    return render_template("store/checkout.html")

@charge.route("/thanks")
def thanks():
    return render_template("store/thanks.html")


@charge.route("/webhooks", methods=["POST"])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = "whsec_eXShuqOQ4qs3xeYt7QL3K1WIFxlF0d5h"
    try:
        # print(payload)
        # print(sig_header)
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        # print(e)
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        # print(e)
        raise e

    # Handle the event
    print(event["type"])
    if event["type"] == "payment_intent.canceled":
        payment_intent = event["data"]["object"]
    elif event["type"] == "payment_intent.created":
        payment_intent = event["data"]["object"]
    elif event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
    elif event["type"] == "customer.created":
        payment_intent = event["data"]["object"]
    elif event["type"] == "checkout.session.completed":
        payment_intent = event["data"]["object"]
    elif event["type"] == "charge.succeeded":
        payment_intent = event["data"]["object"]
    # ... handle other event types
    else:
        print("Unhandled event type {}".format(event["type"]))

    return jsonify(success=True)