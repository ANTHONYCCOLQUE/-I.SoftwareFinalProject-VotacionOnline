# app/views.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.forms import RegistrationForm, LoginForm, ChangeForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
@views_bp.route('/home')
def home():
    return render_template('home.html')

@views_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('views.login'))
    return render_template('register.html', form=form)

@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('views.login'))
        login_user(user)
        return redirect(url_for('views.home'))
    return render_template('login.html', form=form)

@views_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@views_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ChangeForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('account.html', form=form)


""""
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
"""