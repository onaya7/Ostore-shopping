
from flask_login import login_user, login_required, current_user,logout_user
from flask import Blueprint, render_template,redirect , url_for , request ,flash
from werkzeug.security import generate_password_hash, check_password_hash

from myapp.models import db,User


auth = Blueprint('auth', __name__)

@auth.route('/')
def index():

    return render_template('store/index.html')

@auth.route('/profile')
@login_required
def profile():

    return render_template('store/profile.html', name=current_user.name)


@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password= request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))

     


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

###### ADMIN #######

@auth.route('/Users')
def users():
       user = User.query.all()
      
       return render_template('main/users.html', title="Users", user=user)

@auth.route('/<int:user_id>/delete/')
def delete_users(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect (url_for('auth.users', user_id=user_id ))


