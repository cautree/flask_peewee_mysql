from flask import Flask, g,render_template, flash, redirect, url_for
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user

import models
import forms

DEBUG = True
PORT = 8000
HOST = '0,0,0,0'

app = Flask(__name__)
app.secret_key ="abcdefghijklmnopqrstuv"  #generate randomn key for session

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# a function that login manager can use to look up the user
@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

@app.before_request
def before_request():
	"""Connect to the database before each request."""
	g.db = models.DATABASE
	#g.db.connect()
	g.db.get_conn()
	g.user = current_user

@app.after_request
def after_request(response):
	"""Close the database connection after each request"""
	g.db.close()
	return response


@app.route('/register', methods =('GET','POST'))
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit():
		flash("Yay, you registered!","success")
		models.User.create_user(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data
			)
		return redirect(url_for('index'))
	return render_template('register.html',form=form)

@app.route('/login', methods=('GET','POST'))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user= models.User.get(models.User.email == form.email.data)
		except models.DoesNotExist:
			flash("your email or password does not match!", "error")
		else:
		    if check_password_hash(user.password, form.password.data):
			    login_user(user)
			    flash("You've been logged in!", "success")
			    return redirect(url_for('index'))
		    else:
			    flash("your email or password does not match!", "error")

	return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out!", "success")
	return redirect(url_for('index'))

@app.route('/new_post', methods =('GET','POST'))
@login_required
def post():
	form = forms.PostForm()
	if form.validate_on_submit():
		models.Post.create(user=g.user._get_current_object(),
			content= form.content.data.strip())
		flash("Message posted! Thanks!", "success")
		return redirect(url_for('index'))
	return render_template('post.html', form=form)

@app.route('/')
def index():
	stream = models.Post.select().limit(100)
	return render_template('stream.html', stream=stream)


@app.route('/stream')
@app.route('/stream/<username>')
def stream(username = None):
	template = 'stream.html'
	if username and username != current_user.username:
		user = models.User.select().where(models.User.username**username).get()
		stream = user.posts.limit(100)
	else:
		stream = current_user.get_stream().limit(100)
		user = current_user

	if username:
		template ='user_stream.html'
	return render_template(template, stream=stream, user=user)



if __name__ == '__main__':
	models.initialize()
	try:
		with models.DATABASE.transaction():
			models.User.create_user(
				username = 'Yanyan',
				email = 'yanyan@example.com',
				password = 'password',
				admin = True
				)
	except ValueError:
		pass
	#app.run(debug=DEBUG, host= HOST, port = PORT)
	app.run(debug=DEBUG)



