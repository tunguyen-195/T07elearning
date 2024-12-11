# app/auth/routes.py
import logging

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.auth import bp
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegisterForm, ResetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        logging.debug("POST request received")
        if form.validate_on_submit():
            logging.debug("Form submitted successfully")
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                logging.debug(f"User found: {user.username}")
                if user.check_password(form.password.data):
                    logging.debug("Password check passed")
                    login_user(user, remember=form.remember_me.data)
                    flash('Đăng nhập thành công!', 'success')
                    return redirect(url_for('main.index'))
                else:
                    logging.debug("Password check failed")
            else:
                logging.debug("User not found")
            flash('Tên đăng nhập hoặc mật khẩu không đúng.', 'danger')
        else:
            logging.debug("Form validation failed")
            logging.debug(f"Form errors: {form.errors}")
    else:
        logging.debug("GET request received")
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.', 'danger')
            return redirect(url_for('auth.register'))
        new_user = User(
            username=form.username.data,
            fullname=form.fullname.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # Tìm kiếm bằng username
        if user:
            # Logic để gửi email khôi phục mật khẩu
            flash('Một email khôi phục mật khẩu đã được gửi đến địa chỉ email của bạn.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Tên đăng nhập không tồn tại.', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # Your signup logic here
    return render_template('auth/signup.html')
