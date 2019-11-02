import psycopg2 as sql
from psycopg2.extras import DictCursor
from hashlib import sha3_256
from os import environ

print("Welcome to Tixte FOSS(beta 1.0.0) Setup Utility")

try:
    con = sql.connect(environ['DATABASE_URL'])
    cur = con.cursor(cursor_factory=DictCursor)

    cur.execute("SELECT * FROM config WHERE setting_name='admin_password'")
    rows = cur.fetchall()

    notworked = False
except:
    notworked = True
finally:
    if not notworked:
        print("Tixte FOSS is already set up on the specified database. Quiting now.")
        quit()

print("Connecting to PostgreSQL Database")
conn = sql.connect(environ['DATABASE_URL'])
cur = conn.cursor()
print("Connected to Database")

print("Creating Configuration Table")
cur.execute(
    'CREATE TABLE config (id SERIAL PRIMARY KEY, setting_name TEXT NOT NULL UNIQUE, setting_value TEXT NOT NULL)')
conn.commit()

print("Creating Games Table")
cur.execute(
    'CREATE TABLE games (id SERIAL PRIMARY KEY, game TEXT NOT NULL UNIQUE, releasedate TEXT NOT NULL, author TEXT '
    'NOT NULL, category TEXT NOT NULL, filepath TEXT NOT NULL)')
conn.commit()

print("Creating Administrator Password")
# password = input("Enter Administrator Password: ")
password = "password"
hashed_password = sha3_256(password.encode()).hexdigest()
cur.execute(
    "INSERT INTO config (setting_name, setting_value) VALUES ('admin_password', %s)", (hashed_password,))
conn.commit()
print("Default Administrator Password is: password")

print("Creating Default Hub Message")
cur.execute(
    "INSERT INTO config (setting_name, setting_value) VALUES('hub_message', 'Tixte FOSS')")
conn.commit()

print("Closing Database")
conn.close()

print("Setup is Complete!")
print("You Can Log In As Admin at /admin")
print("\nCustomize Your Homepage at templates/index.html")
