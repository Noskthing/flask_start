from flask import render_template,session,flash,redirect,url_for,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, login_required, \
    current_user
    
from .forms import LoginForm,RegistrationForm,ChangeEmailForm,ChangePasswordForm,PasswordResetForm
from . import auth

from ..auth_email import send_email
from ..models import User
from .. import db


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password!')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
    
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email('295060015@qq.com', 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)

        flash('A confirmation email has been sent to you by email.')

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/changeemail')
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if not User.query.filter_by(email = form.email.data).first():
            flash('Not found email !')
    return render_template('auth/change_email.html',form = form)


@auth.route('/confirm/<token>')
def confirm(token):
    flash(User.check_confirm(token))
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


