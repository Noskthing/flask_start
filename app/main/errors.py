from . import main
from flask import render_template

@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

@main.app_errorhandler(500)
def page_not_found(e):
	return render_template('500.html')