import sqlite3
conn = sqlite3.connect('users.db')
c = conn.cursor()
users = {row[0]:{"password":row[1],"loggedIn":False,  "randStr":"", "lastSeen":0} for row in c.execute("SELECT email, password FROM users")}
conn.close()
