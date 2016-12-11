from flask import render_template,session,flash,redirect,url_for
from .forms import LoginForm
from . import auth
from werkzeug.security import generate_password_hash,check_password_hash

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
	return render_template('login.html',form = form,
		email = session.get('email',None),
		password = generate_password_hash(session.get('password',None)) if session.get('password',None) else ''
		)
