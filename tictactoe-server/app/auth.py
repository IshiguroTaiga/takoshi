from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import db, User
from . import bcrypt
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            return "Username exists"
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form.get('password')):
            login_user(user)
            return redirect(url_for('client.lobby'))
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))