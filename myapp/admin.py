from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from myapp.models import Admin, User ,db





admin=Blueprint('users', __name__,)

####   ADMIN AUTHENTICATION   #######
@admin.route('/Adminlogin')
def login():
    
   
    return render_template('main/adminlogin.html')

@admin.route('/Adminlogin', methods=['POST'])
def users_login():
    email = request.form.get('email')
    password= request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Admin.query.filter_by(email=email).first()
    if user:
         if not user: #or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('admin.login'))

    login_user(user, remember=remember)
    return redirect(url_for('auth.users'))

@admin.route('/insertuser')
def insert_admin():
    return render_template('main/adminadduser.html')

   

@admin.route('/insertadmin')
def insert_user():
    return render_template('main/adminuser.html')

@admin.route('/insertadmin', methods=['GET','POST'])
def insertadmin():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    password = request.form.get('password')

    user = Admin.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = Admin(email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    flash('A new Admin has been added successfully ')
    return redirect(url_for('auth.users',))
#### AUTHENTICATION END ######


@admin.route('/insertuser', methods=['GET','POST'])
def insertuser():
    # code to validate and add user to database goes here
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(name=name).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(name=name,email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    flash('A new user has been added successfully ')
    return redirect(url_for('auth.users',))

@admin.route('/edituser/<int:id>', methods=['GET','POST'])
def edit_user(id):

    

    if request.method == 'POST':
        users = User.query.filter_by(id=id).first()
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        users.name=name
        users.email=email
        users.password=password
        db.session.commit()
        flash(f'User has been edited successfully')
        return redirect(url_for('auth.users'))
    users = User.query.filter_by(id=id).first()
    return render_template('main/adminedituser.html', users=users)


        


#### AUTHENTICATION END ######


####  OSTORE ####

@admin.route('/home')
def home():
    return render_template('store/index.html')

@admin.route('/about')
def about():
    return render_template('store/about.html')

@admin.route('/contact')
def contact():
    return render_template('store/contact.html')

@admin.route('/cart')
def cart():
    return render_template('store/cart.html')



