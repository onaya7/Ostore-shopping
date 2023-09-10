from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from myapp.forms import LoginForm, RegistrationForm
from myapp.instance import bcrypt
from myapp.models import Admin, User, db

admin = Blueprint(
    "admin",
    __name__,
)


####   ADMIN AUTHENTICATION   #######
@admin.route("/users")
def users():
    user = User.query.all()

    return render_template("admin/users.html", title="Users", user=user)


@admin.route("/create_user", methods=["GET", "POST"])
def create_user():
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
        flash("Your account has been created!", "success")
        return redirect(url_for("admin.users"))
    return render_template(
        "admin/create_user.html",
        title="create_user",
        form=form,
    )


# Login route
@admin.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("users.users"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page) if next_page else redirect(url_for("users.users"))
            )
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("user/login.html", title="Login", form=form)


@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.home"))


@admin.route("/<int:user_id>/delete/")
def delete_users(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin.users", user_id=user_id))


#### AUTHENTICATION END ######
