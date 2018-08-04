from flask import Flask, render_template, request, url_for, redirect, flash, session, g
from dbconnect import connection
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from flask_mail import Mail, Message
import gc
from wtforms.fields.html5 import EmailField

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def homepage():
	if session.get('logged_in') == True:
		return redirect(url_for('dashboard'))
	else:
		return render_template("main.html")

@app.route('/Terms/')
def terms():
	return render_template("terms.html")

@app.route('/About/')
def about():
	return render_template("about.html")

@app.route('/Contact/')
def contact():
	return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(e):
	try:
		gc.collect()
		rule = request.path
		if "feed" in rule or "favicon" in rule or "wp-content" in rule or "wp-login" in rule or "wp-login" in rule or "wp-admin" in rule or "xmlrpc" in rule or "tag" in rule or "wp-include" in rule or "style" in rule or "apple-touch" in rule or "genericons" in rule or "topics" in rule or "category" in rule or "index" in rule or "include" in rule or "trackback" in rule or "download" in rule or "viewtopic" in rule or "browserconfig" in rule:
			pass
		else:
			pass
		return render_template('404.html'), 404
	except Exception as e:
		return(str(e))

# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login_page'))
	return wrap

# logout required decorator
def logout_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			flash('You need to logout first.')
			return redirect(url_for('dashboard'))
		else:
			return f(*args, **kwargs)
	return wrap

@app.route('/dashboard/')
@login_required
def dashboard():
	return render_template("dashboard.html")

@app.route('/logout/')
@login_required
def logout():
	session.pop('logged_in', None)
	session.clear()
	flash('You have been logged out.')
	gc.collect()
	return redirect(url_for('homepage'))

@app.route('/user/<name_user>/')
@login_required
def user(name_user):
	if session.get('username') == name_user:
		return render_template("user.html")
	else:
		return render_template("404.html")

@app.route('/login/', methods=["GET","POST"])
@logout_required
def login_page():
	error = ''
	try:
		c, conn = connection()
		if request.method == "POST":

			data = c.execute("SELECT * FROM users WHERE username = (%s)",
							 (thwart(request.form['username']),))
			
			data = c.fetchone()[2]

			if sha256_crypt.verify(request.form['password'], data):
				session['logged_in'] = True
				session['username'] = request.form['username']

				flash("You are now logged in")
				return redirect(url_for("dashboard"))

			else:
				error = "Invalid credentials, try again."

		gc.collect()

		return render_template("login.html", error=error)

	except Exception as e:
		#flash(e)
		error = "Invalid credentials, try again."
		return render_template("login.html", error = error)

class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=20)])
	# email = TextField('Email Address', [validators.Length(min=6, max=50)])
	email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
	password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the <a href="/Terms" target="blank">Terms of Service</a>', [validators.Required()])

@app.route('/register/', methods=['GET', 'POST'])
@logout_required
def register():

	try:
		form = RegistrationForm(request.form)
		if request.method == 'POST' and form.validate():
			#flash("register attempted")

			username = form.username.data
			email = form.email.data

			password = sha256_crypt.encrypt((str(form.password.data)))
			c,conn = connection()

			x = c.execute("SELECT * FROM users WHERE username = (%s)",
				(thwart(username),))
			y = c.execute("SELECT * FROM users WHERE email = (%s)",
				(thwart(email),))

			if int(x) > 0:
				flash("That username is already taken, please choose another")
				return render_template('register.html', form=form)
			elif int(y) > 0:
				flash("This email is already in use")
				return render_template('register.html', form=form)
			else:
				c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
					(thwart(username), thwart(password), thwart(email)))
				conn.commit()
				flash('Thanks for registering')
				c.close()
				conn.close()
				gc.collect()
				return redirect(url_for('login_page'))
		gc.collect()
		return render_template('register.html', form=form)
	except Exception as e:
		return(str(e))



if __name__ == "__main__":
	app.run()