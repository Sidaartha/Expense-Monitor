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

@app.route('/Contact/', methods=["GET","POST"])
def contact():
	try:
		c,conn = connection()		
		error = None
		if request.method == "POST":
			q_text = request.form['que']
			q_text = q_text.replace('\r', ';').replace('\n', ';')
			c.execute("INSERT INTO queries (uid, username, query) VALUES (%s, %s, %s)",(session.get('uid'),session.get('username'),q_text))
			conn.commit()
			c.close()
			conn.close()
			flash("Your query has been submitted successfully")
			return redirect(url_for('dashboard'))
		gc.collect()
		return render_template("contact.html")
	except Exception as e:
		return(str(e))

@app.route('/DarkMode/')
def dark_mode():
	session['mode'] = 'dark'
	return redirect(url_for('dashboard'))

@app.route('/LightMode/')
def light_mode():
	session['mode'] = 'light'
	return redirect(url_for('dashboard'))

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
			flash('Your already logged in.')
			return redirect(url_for('dashboard'))
		else:
			return f(*args, **kwargs)
	return wrap

@app.route('/dashboard/', methods=["GET","POST"])
@login_required
def dashboard():

	try:
		c,conn = connection()		
		error = None

		c.execute("SELECT cash, bank, paytm, amazon, owe_in, owe_out FROM users WHERE username = (%s)", (thwart(session.get('username')),))
		wallets = c.fetchone()

		c.execute("SELECT date, amount, name, oid FROM passbook_owe WHERE uid = (%s) ORDER BY date DESC", (session.get('uid'),))
		passbook_o = c.fetchall()

		if session.get('passbook_limit') :
			c.execute("SELECT date, amount, val, mode, activity, total, pid FROM passbook WHERE uid = (%s) ORDER BY pid DESC LIMIT %s", (session.get('uid'),session.get('passbook_limit')))
			passbook = c.fetchall()
			session['passbook_limit'] = ''
		else:
			c.execute("SELECT date, amount, val, mode, activity, total, pid FROM passbook WHERE uid = (%s) ORDER BY pid DESC LIMIT 10", (session.get('uid'),))
			passbook = c.fetchall()

		# c.execute("SELECT date, amount, val, mode, activity, total, pid FROM passbook WHERE uid = (%s) ORDER BY pid DESC LIMIT 10", (session.get('uid'),))
		# passbook = c.fetchall()

		if request.method == "POST":
			def val_validator(input_amount):
				if input_amount[0] == '-':
					value = 1
					amount_val = input_amount[1:]
				elif input_amount[0] == '+':
					value = 0
					amount_val = input_amount[1:]
				else:
					value = 0
					amount_val = input_amount
				return value, amount_val

			wallets_dic = {'cash': 0, 'bank': 1, 'paytm': 2, 'amazon': 3}

			if 'bills' in request.form:
				_, amount_val = val_validator(request.form['bills'])
				wallet_type = request.form.get('comp_select')
				comments = request.form['bills_dis']
				value = 1
				cmd_users = 'UPDATE users SET ' + wallet_type + '=' + wallet_type + ' - %s WHERE username = %s'
				c.execute(cmd_users, (amount_val, thwart(session.get('username'))))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), amount_val, value, wallet_type.capitalize(), comments.capitalize(), wallets[wallets_dic[wallet_type]]))
			elif 'cash' in request.form:
				value, amount_val = val_validator(request.form['cash'])
				c.execute("""UPDATE users SET cash = cash + %s WHERE username = %s""",(request.form['cash'], thwart(session.get('username'))))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), amount_val, value, 'Cash', 'updated', wallets[0]))
			elif 'bank' in request.form:
				value, amount_val = val_validator(request.form['bank'])
				c.execute("""UPDATE users SET bank = bank + %s WHERE username = %s""",(request.form['bank'], thwart(session.get('username'))))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), amount_val, value, 'Bank', 'updated', wallets[1]))
			elif 'paytm' in request.form:
				value, amount_val = val_validator(request.form['paytm'])
				c.execute("""UPDATE users SET paytm = paytm + %s WHERE username = %s""",(request.form['paytm'], thwart(session.get('username'))))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), amount_val, value, 'Paytm', 'updated', wallets[2]))
			elif 'amazon' in request.form:
				value, amount_val = val_validator(request.form['amazon'])
				c.execute("""UPDATE users SET amazon = amazon + %s WHERE username = %s""",(request.form['amazon'], thwart(session.get('username'))))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), amount_val, value, 'Amazon', 'updated', wallets[3]))
			elif 'filter' in request.form:
				value = int(request.form['filter'])
				if value < 0 : value = 10
				session['passbook_limit'] = value
			elif 'passbook_del' in request.form:
				del_row = int(request.form['passbook_del'])
				c.execute("DELETE FROM passbook WHERE pid = '%s'", (del_row,))
			elif 'owe_in' in request.form:
				_, amount_val = val_validator(request.form['owe_in_amount'])
				person_name = request.form['owe_in_person']
				wallet_type = request.form.get('comp_select_in')
				value = 1
				ver_in = c.execute("SELECT * FROM passbook_owe WHERE name = %s AND uid = %s", (person_name.capitalize(), session.get('uid')))
				if int(ver_in) >0 :
					c.execute("UPDATE passbook_owe SET amount = amount + %s WHERE name = %s AND uid = %s", (amount_val, person_name.capitalize(), session.get('uid')))
				else :
					c.execute("INSERT INTO passbook_owe (uid, amount, name) VALUES (%s, %s, %s)", (session.get('uid'), amount_val, person_name.capitalize()))
				c.execute("SELECT amount FROM passbook_owe WHERE uid = %s", (session.get('uid'),))
				am_list = c.fetchall()
				owe_out_val = 0
				owe_in_val = 0
				for i in am_list:
					if i[0] < 0 : owe_out_val = owe_out_val + int(abs(i[0]))
					if i[0] > 0 : owe_in_val = owe_in_val + i[0]
					else: pass
				c.execute("""UPDATE users SET owe_out = %s, owe_in = %s WHERE username = %s""",(owe_out_val, owe_in_val, thwart(session.get('username'))))
				cmd_users = 'UPDATE users SET ' + wallet_type + '=' + wallet_type + ' - %s WHERE username = %s'
				c.execute(cmd_users, (amount_val, thwart(session.get('username'))))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), amount_val, value, 'Person', person_name.capitalize(), wallets[4]))
			elif 'owe_out' in request.form:
				_, amount_val = val_validator(request.form['owe_out_amount'])
				person_name = request.form['owe_out_person']
				wallet_type = request.form.get('comp_select_out')
				value = 0
				ver_out = c.execute("SELECT * FROM passbook_owe WHERE name = %s AND uid = %s", (person_name.capitalize(), session.get('uid')))
				if int(ver_out) >0 :
					c.execute("UPDATE passbook_owe SET amount = amount - %s WHERE name = %s AND uid = %s", (amount_val, person_name.capitalize(), session.get('uid')))
				else :
					c.execute("INSERT INTO passbook_owe (uid, amount, name) VALUES (%s, -%s, %s)", (session.get('uid'), amount_val, person_name.capitalize()))
				c.execute("SELECT amount FROM passbook_owe WHERE uid = %s", (session.get('uid'),))
				am_list = c.fetchall()
				owe_out_val = 0
				owe_in_val = 0
				for i in am_list:
					if i[0] < 0 : owe_out_val = owe_out_val + int(abs(i[0]))
					if i[0] > 0 : owe_in_val = owe_in_val + i[0]
					else: pass
				c.execute("""UPDATE users SET owe_out = %s, owe_in = %s WHERE username = %s""",(owe_out_val, owe_in_val, thwart(session.get('username'))))
				cmd_users = 'UPDATE users SET ' + wallet_type + '=' + wallet_type + ' + %s WHERE username = %s'
				c.execute(cmd_users, (amount_val, thwart(session.get('username'))))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), amount_val, value, 'Person', person_name.capitalize(), wallets[5]))
			elif 'owe_in_del' in request.form:
				del_am = request.form['owe_in_del']
				wallet_type = request.form.get('comp_select_in_del')
				c.execute("SELECT amount, name FROM passbook_owe WHERE oid = %s", (del_am,))
				an_tup = c.fetchall()
				am_to_del = int(an_tup[0][0])
				person_name = an_tup[0][1]
				value = 0
				c.execute("""UPDATE passbook_owe SET amount = 0 WHERE oid = %s""",(del_am,))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), am_to_del, value, 'Person', person_name.capitalize(), wallets[4]))
				c.execute("UPDATE users SET owe_in = owe_in - %s WHERE username = %s", (am_to_del, thwart(session.get('username'))))
				cmd_users = 'UPDATE users SET ' + wallet_type + '=' + wallet_type + ' + %s WHERE username = %s'
				c.execute(cmd_users, (am_to_del, thwart(session.get('username'))))
			elif 'owe_out_del' in request.form:
				del_am = request.form['owe_out_del']
				wallet_type = request.form.get('comp_select_out_del')
				c.execute("SELECT amount, name FROM passbook_owe WHERE oid = %s", (del_am,))
				an_tup = c.fetchall()
				am_to_del = int(str(an_tup[0][0])[1:])
				person_name = an_tup[0][1]
				value = 1
				c.execute("""UPDATE passbook_owe SET amount = 0 WHERE oid = %s""",(del_am,))
				c.execute("INSERT INTO passbook (uid, amount, val, mode, activity, total) VALUES (%s, %s, %s, %s, %s, %s)",(session.get('uid'), am_to_del, value, 'Person', person_name.capitalize(), wallets[5]))
				c.execute("UPDATE users SET owe_out = owe_out - %s WHERE username = %s", (am_to_del, thwart(session.get('username'))))
				cmd_users = 'UPDATE users SET ' + wallet_type + '=' + wallet_type + ' - %s WHERE username = %s'
				c.execute(cmd_users, (am_to_del, thwart(session.get('username'))))
			else:
				pass
			conn.commit()
			c.close()
			conn.close()
			return redirect(url_for('dashboard'))

		gc.collect()
		return render_template("dashboard.html", wallets = wallets, passbook = passbook, passbook_o = passbook_o)
	except Exception as e:
		return(str(e))

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

@app.route('/user/switch/')
@login_required
def switch():
	session.pop('logged_in', None)
	session.clear()
	flash('You have been logged out.')
	gc.collect()
	return redirect(url_for('login_page'))

@app.route('/login/', methods=["GET","POST"])
@logout_required
def login_page():
	error = ''
	try:
		c, conn = connection()
		if request.method == "POST":

			data = c.execute("SELECT * FROM users WHERE username = (%s)",
							 (thwart(request.form['username']),))
			
			data_all = c.fetchone()
			data_uid = data_all[0]
			data = data_all[2]

			if sha256_crypt.verify(request.form['password'], data):
				session['logged_in'] = True
				session['username'] = request.form['username']
				session['uid'] = data_uid

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

@app.route('/user/change-password/', methods=['GET', 'POST'])
@login_required
def change_password():
	try:
		c,conn = connection()
		
		error = None
		if request.method == 'POST':

			data = c.execute("SELECT * FROM users WHERE username = (%s)",
					(thwart(session.get('username')),))
			data = c.fetchone()[2]


			if sha256_crypt.verify(request.form['password'], data):
				# flash('Authentication Successful.')
				if len(request.form['npassword']) > 0:
					#flash("You wanted to change password")

					if request.form.get('npassword') == request.form.get('rpassword'):
						try:
							# flash("new passwords matched")
							print("hello")
							password = sha256_crypt.encrypt((str(request.form['npassword'])))
							
							c,conn = connection()
							
							data = c.execute("UPDATE users SET password = %s where username = %s",
							(thwart(password), thwart(session.get('username'))))

							conn.commit()
							c.close()
							conn.close()
							flash("Password changed")
						except Exception as e:
							return(str(e))
					else:
						flash("Passwords do not match!")

				return redirect(url_for('dashboard'))

			else:
				flash('Invalid credentials. Try again')
				error = 'Invalid credentials. Try again'
		gc.collect()          
		return render_template('change_pass.html', error=error)
	except Exception as e:
		return(str(e))

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
				c.execute("INSERT INTO users (username, password, email, cash, bank, paytm, amazon, owe_in, owe_out) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
					(thwart(username), thwart(password), thwart(email), 0, 0, 0, 0, 0, 0))
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

@app.template_filter('INR')
def currency(val):
	return "₹{:,.2f}".format(val)
@app.template_filter('INR_s')
def currency(val):
	return "{:,.2f}".format(val)
@app.template_filter('INR_f')
def currency(val):
	return "₹{:,}".format(val)
@app.template_filter('ABS')
def abs(val):
	return str(val)[1:]
@app.template_filter('CAP')
def cap(val):
	return val.capitalize()
@app.template_filter('timestamp_f')
def ts(val):
	return val.strftime("%d %b %y, %I:%M %p")

if __name__ == "__main__":
	app.run()
	# app.run(debug=True,host='0.0.0.0')