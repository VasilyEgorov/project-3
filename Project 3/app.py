from flask import Flask, session, request, render_template, redirect, url_for
from database import createDatabase, createUserModel, loginUser, usernameExists, createUser, createToDoModel
from database import createToDo, getToDos, deleteToDo
import bcrypt
import os

dbPath = "db.sqlite3"
createDatabase(dbPath)
createUserModel(dbPath)
createToDoModel(dbPath)
app = Flask(__name__)

app.secret_key = os.urandom(12)

@app.route("/")
def title():
	return render_template("title.html")

@app.route("/index", methods=["GET", "POST"])
def index():
	try:
		session["logged_in"]
	except KeyError:
		session["logged_in"] = False
	if session["logged_in"]:
		if request.method == "POST":
			description = request.form["description"]
			createToDo(session["user_id"], description, dbPath)
			return redirect(url_for("index"))
		q = getToDos(session["user_id"], dbPath)
		print(q)
		return render_template("index.html", toDos=q)
	else:
		return redirect(url_for("login"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
	try:
		session["logged_in"]
	except KeyError:
		session["logged_in"] = False
	if session["logged_in"]:
		deleteToDo(session["user_id"], todo_id, dbPath)
		return redirect(url_for("index"))
	else:
		return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
	try:
		session["logged_in"]
	except KeyError:
		session["logged_in"] = False
	if not session["logged_in"]:
		if request.method == "GET":
			return render_template("auth/login.html")
		elif request.method == "POST":
			s = request.form["username"]
			t = request.form["password"]
			r = loginUser(s, t, dbPath)
			if r:
				session["logged_in"] = True
				session["user_id"] = r[0]
				return redirect(url_for("index"))
			else:
				return render_template("auth/login.html",invalid=True)
	else:
		return redirect(url_for("index"))

@app.route("/logout")
def logout():
	session["logged_in"] = False
	del session["user_id"]
	return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
	try:
		session["logged_in"]
	except KeyError:
		session["logged_in"] = False
	if not session["logged_in"]:

		if request.method == "GET":
			return render_template("auth/register.html")
		elif request.method == "POST":
			s = request.form["username"]
			t = request.form["password"]
			y = bcrypt.hashpw(t.encode('utf8'), bcrypt.gensalt())
			if not usernameExists(s, dbPath):
				createUser(s, y, dbPath)
				return redirect(url_for("login"))
			else:
				return render_template("auth/register.html", invalid=True)
	else:
		return redirect(url_for("index"))

if __name__ == "__main__":
	app.run(debug=True,port=8080)