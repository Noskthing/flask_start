from flask import render_template,redirect,url_for,session,flash
from . import main
from .forms import NameForm

@main.route('/')
def index():
	return render_template('index.html')


@main.route('/login',methods=['GET','POST'])
def login():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session['name']
		if old_name is not None and old_name != form.name.data:
			flash('Looks like u have changed ur name !')
		session['name'] = form.name.data
		session['password'] = form.password.data
		return redirect(url_for('.index'))
	return render_template('login.html',form = form,name = session.get('name'),password = session.get('password'))

	