import sqlite3
import bcrypt

def createDatabase(path):
	a = sqlite3.connect(path)
	a.close()
	print("База данных создана или уже существует")


def createUserModel(path):
	b = "Пользователь"
	w = """
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT UNIQUE,
		password TEXT
			 """
	a = sqlite3.connect(path)
	c = a.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS {}({});".format(b, w))
	a.commit()
	a.close()
	print("Пользовательская таблица создана или уже существует")

def createToDoModel(path):
	b = "Делать"
	w = """
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_id INTEGER,
		description TEXT
			 """
	a = sqlite3.connect(path)
	c = a.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS {}({});".format(b, w))
	a.commit()
	a.close()
	print("Таблица задач создана или уже существует")


def loginUser(username, password, path):
	a = sqlite3.connect(path)
	c = a.cursor()
	q = c.execute("SELECT * FROM User")
	q = c.fetchall()
	a.close()
	for i in q:
		if i[1] == username:
			if bcrypt.checkpw(password.encode('utf8'), i[2]):
				return i
			break
	return False

def createUser(username,password,path):
	a = sqlite3.connect(path)
	c = a.cursor()
	i = c.execute("""INSERT INTO User(username,password)
						 VALUES (?,?);""", (username, password))
	a.commit()
	a.close()

def usernameExists(username, path):
	a = sqlite3.connect(path)
	c = a.cursor()
	q = c.execute("SELECT * FROM User")
	q = c.fetchall()
	a.close()
	for i in q:
		if i[1] == username:
			return True
	return False	

def createToDo(user_id, description, path):
	a = sqlite3.connect(path)
	c = a.cursor()
	c.execute("""INSERT INTO toDo(user_id,description) 
							VALUES(?,?)""",(user_id,description,))
	print("""INSERT INTO toDo(user_id,description) 
							VALUES({},{})""".format(user_id,description))
	a.commit()
	a.close()

def deleteToDo(user_id,todo_id,path):
	a = sqlite3.connect(path)
	c = a.cursor()
	c.execute("DELETE FROM toDo WHERE user_id=? and id=?",(user_id,todo_id,))
	a.commit()
	a.close()

def getToDos(user_id,path):
	a = sqlite3.connect(path)
	c = a.cursor()
	c.execute("SELECT * FROM toDo WHERE user_id=?",(user_id,))
	r = c.fetchall()
	a.close()
	return r