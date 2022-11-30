from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route("/")
def index():
	return redirect("/login_page")



@app.route("/login_page")
def login_page():
	return render_template("login.html")


@app.route("/login_attempt", methods=["POST"])
def login_handler():

	data = {
		"email": request.form['email']
	}

	user = User.get_by_email(data)


	if not user:
		flash("Invalid email/password", "login")
		return redirect("/")
	if not bcrypt.check_password_hash(user.password, request.form['password']):
		flash("Invalid password", "login")
		return redirect("/")
	session['user_id'] = user.id
	#session['first_name'] = user.first_name
	#session['last_name'] = user.last_name
	#session['email'] = user.email
	return redirect("/dashboard")



@app.route("/logout")
def logout():
	session.clear()
	return redirect("/login_page")



@app.route("/register")
def register():
	return render_template("register.html")



# For some reason I cannot get the validator to work as needed. It's always erroring out on me
@app.route("/register_attempt", methods=["POST"])
def registration_handler():
	print("++++++++++++++++++++++++++++")
	print(request.form['first_name'])
	if not User.validator(request.form):
		return redirect("/register")


	new_user = {
		"first_name": request.form['first_name'],
		"last_name": request.form['last_name'],
		"email": request.form['email'],
		"password": bcrypt.generate_password_hash(request.form['password'])
	}
	id = User.save(new_user)
	#if not id:
	#	flash("Email already taken", "register")
	#	return redirect("/register")
	print("==================================")
	session['user_id'] = id
	#session['first_name'] = user.first_name
	#session['last_name'] = user.last_name
	#session['email'] = user.email

	return redirect("/dashboard")