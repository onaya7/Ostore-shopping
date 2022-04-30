from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash
from myapp.models import Admin, User ,db





admin=Blueprint('users', __name__,)

####   ADMIN AUTHENTICATION   #######
@admin.route('/Userslogin')
def login():
    
   
    return render_template('main/adminlogin.html')

@admin.route('/Userslogin', methods=['POST'])
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
def insert_user():
    return render_template('main/adminuser.html')

@admin.route('/insertuser', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form.get('name')
        password =request.form['password']
        
        adduser= User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(adduser)
        db.session.commit()
        flash('A new user has been added successfully ')
        return redirect(url_for('auth.users',))
#### AUTHENTICATION END ######



####  OSTORE ####

@admin.route('/home')
def home():
    return render_template('store/index.html')

@admin.route('/product')
def product():
    return render_template('store/products.html')

@admin.route('/productdetails')
def productdetails():
    return render_template('store/productdetails.html')


@admin.route('/about')
def about():
    return render_template('store/about.html')

@admin.route('/contact')
def contact():
    return render_template('store/contact.html')

@admin.route('/cart')
def cart():
    return render_template('store/cart.html')



