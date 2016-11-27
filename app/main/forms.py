from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required


class NameForm(Form):
	name = StringField('Username',validators=[Required()])
	password = StringField('Password',validators=[Required()])
	submit = SubmitField('Submit')