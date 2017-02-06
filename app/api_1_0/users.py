from flask import jsonify, request, current_app, url_for ,render_template
from . import api
from ..models import User, Post


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/test',methods = ['GET','POST'])
def test():
	message = ''
	if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        message = 'html'
	return jsonify({'success': 'test', 'message': message})


@api.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('main/post.html', posts=[post])