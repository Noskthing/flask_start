from app import create_app,db
# from flask_script import Manager, Shell

app = create_app('default')
# manager = Manager(app)


if __name__ == '__main__':
	# with app.app_context():
 #        # Extensions like Flask-SQLAlchemy now know what the "current" app
 #        # is while within this block. Therefore, you can now run........
	# 	db.create_all()
	app.run()