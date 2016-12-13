from flask import render_template,session,flash,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, login_required, \
    current_user
    
from .forms import LoginForm,RegistrationForm
from . import auth

from ..auth_email import send_email
from ..models import User
from .. import db

@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	
	if form.validate_on_submit():
		old_email = session.get('email',None)
		if old_email is not None and old_email != form.email.data:
			flash('Looks like u have changed your email sss%s?' %form.email.data)
		session['email'] = form.email.data
		session['password'] = form.password.data
		# return redirect(url_for('main.index'))
	return render_template('auth/login.html',form = form,
		email = session.get('email',None),
		password = generate_password_hash(session.get('password',None)) if session.get('password',None) else ''
		)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
    
        # db.session.add(user)
        # db.session.commit()

        token = user.generate_confirmation_token()
        send_email('295060015@qq.com', 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)

        flash('A confirmation email has been sent to you by email.')

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))