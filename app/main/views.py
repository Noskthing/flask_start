from flask import render_template,redirect,url_for,session,flash,redirect
from . import main
from .forms import NameForm


@main.route('/')
def index():
	return render_template('index.html')




	