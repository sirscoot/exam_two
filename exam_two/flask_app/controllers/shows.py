from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.show import tvShow


# I cannont get this function to work with 'get_shows_with_creator' method. It feels like I've tried every way to get this to work and I cannot think of any others. Please help....
@app.route("/dashboard")
def dashboard():
	if 'user_id' not in session:
		flash("you must be logged in to view this page", "login")
		return redirect("/login")
	print(session['user_id'])
	data = {
		"id": session['user_id']
	}

	user = User.get_one(data)
	users_shows = tvShow.get_shows_with_creator()
	return render_template("dashboard.html", user=user, shows=users_shows)


# this one seems to work as inteded. do not touch
@app.route("/show/<int:show_id>")
def show(show_id):
	if 'user_id' not in session:
		flash("you must be logged in to view this page", "login")
		return redirect("/login")
	data = {
		"id": show_id
	}
	users = User.get_one(data)
	shows = tvShow.get_shows_with_creator()
	return render_template("show.html", shows=shows, users=users)



@app.route("/delete/<int:show_id>")
def delete(show_id):
	if 'user_id' not in session:
		flash("you must be logged in to view this page", "login")
		return redirect("/login")
	data = {
		"id": show_id
	}

	tvShow.delete(data)
	return redirect("/dashboard")


# can create the show properly from what it looks like. don't touch these functions
@app.route("/create")
def create():
	if 'user_id' not in session:
		flash("you must be logged in to view this page", "login")
		return redirect("/login")
	return render_template("create.html")


@app.route("/add_show", methods=['POST'])
def add_show():
	if 'user_id' not in session:
		flash("you must be logged in to view this page", "login")
		return redirect("/login")
	print(session['user_id'])
	data = {
		"title": request.form['title'],
		"network": request.form['network'],
		"release_date": request.form['release_date'],
		"description": request.form['description'],
		"user_id": session['user_id']
	}
	tvShow.save(data)

	return redirect("/dashboard")





@app.route("/edit/<int:show_id>")
def edit_show(show_id):
	data = {
		"id": show_id
	}
	edit_show = tvShow.get_shows_with_creator()
	return render_template("edit.html", edits=edit_show)




@app.route("/save_edit/<int:show_id>", methods=["POST"])
def update_show(show_id):
	data = {
		"id": show_id,
		"title": request.form['title'],
		"network": request.form['network'],
		"release_date": request.form['release_date'],
		"description": request.form['description'],
		"user_id": session['user_id']
	}
	tvShow.update(data)
	return redirect('/dashboard')


@app.route("/like/<int:show_id>", methods=["POST"])
def likes(show_id):
	counter += 1
	data = {
		"id": show_id,
		"likes": counter
	}
	tvShow.like(data)
	return redirect("/dashboard")
