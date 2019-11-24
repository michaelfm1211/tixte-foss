from hashlib import sha3_256
from os import environ, path

import psycopg2 as sql
from flask import render_template, request, redirect, url_for
from psycopg2.extras import DictCursor
from werkzeug.utils import secure_filename

from tixte_foss import app

admin_hash = ""

def get_admin_hash():
    global admin_hash

    con = sql.connect(environ['DATABASE_URL'])
    cur = con.cursor(cursor_factory=DictCursor)

    cur.execute("SELECT * FROM config WHERE setting_name='admin_password'")
    rows = cur.fetchall()

    if len(rows) == 1:
        for row in rows:
            admin_hash = row['setting_value']
    else:
        print("FATAL ERROR: Multiple or No Administrator Passwords")
        quit(1)


get_admin_hash()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hub')
def hub():
    con = sql.connect(environ['DATABASE_URL'])
    cur = con.cursor(cursor_factory=DictCursor)

    cur.execute("SELECT * FROM config WHERE setting_name='hub_message'")
    rows = cur.fetchall()

    msg = "Tixte FOSS"
    if len(rows) == 1:
        for row in rows:
            msg = row['setting_value']
    else:
        print("FATAL ERROR: Multiple or No Hub Message\nResorting to Default Hub Message")

    cur.execute("SELECT * FROM games")
    old_new_games = cur.fetchall()

    new_old_games = []
    for game in old_new_games:
        new_old_games.insert(0, game)

    cur.execute("SELECT * FROM config WHERE setting_name='sidebar_links';")
    sidebar_links_dict = cur.fetchone()
    sidebar_links = sidebar_links_dict[2]
    links_comb = sidebar_links.split(",,,")
    links = []
    for link in links_comb:
        links.append(link.split(","))

    return render_template('hub.html', msg=msg, games=new_old_games, links=links)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/all_games')
def all_games():
    con = sql.connect(environ['DATABASE_URL'])
    cur = con.cursor(cursor_factory=DictCursor)

    cur.execute("SELECT * FROM games")
    rows = cur.fetchall()

    return render_template('all_games.html', rows=rows, query="")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "GET":
        return render_template("admin/login.html")
    elif request.method == "POST":
        password = request.form['password'].encode()
        hashed_password = sha3_256(password).hexdigest()

        if hashed_password == admin_hash:
            return render_template("admin/index.html", admin_key=hashed_password)
        else:
            return render_template("admin/login.html", loginfailed=True)


@app.route('/admin/add_game', methods=['GET', 'POST'])
def add_game():
    if request.method == "GET":
        return render_template('admin/add_game.html', title="Add Game")
    elif request.method == "POST":
        if request.form['admin_key'] != admin_hash:
            redirect(url_for('admin'))
        game = request.form['game']
        releasedate = request.form['releasedate']
        author = request.form['author']
        category = request.form['category']
        file = request.files['file']

        filename = secure_filename(game)
        filepath = path.join("static/tixte-games", filename) + ".html"

        file.save(path.join("tixte_foss", filepath))

        con = sql.connect(environ['DATABASE_URL'])
        cur = con.cursor(cursor_factory=DictCursor)

        # NOTE: SQL Injection is not possible due to this being an Admin-Only page
        cur.execute("INSERT INTO games (game,releasedate,author,category,filepath) VALUES(%s, %s, %s, %s, %s)",
                    (game, releasedate, author, category, filepath))
        con.commit()
        con.close()

        msg = "Game Added"
        return render_template("result.html", msg=msg)


@app.route('/admin/delete_game', methods=['GET', 'POST'])
def delete_game():
    if request.method == "GET":
        return render_template('admin/delete_game.html', title="Delete Game")
    elif request.method == "POST":
        if request.form['admin_key'] != admin_hash:
            redirect(url_for('admin'))

        game = request.form['game']

        con = sql.connect(environ['DATABASE_URL'])
        cur = con.cursor(cursor_factory=DictCursor)

        cur.execute("DELETE FROM games WHERE game=%s", (game,))
        con.commit()
        con.close()

        msg = "Game Deleted"
        return render_template("result.html", msg=msg)


@app.route('/admin/change_message', methods=['GET', 'POST'])
def change_message():
    if request.method == "GET":
        return render_template('admin/change_message.html', title='Change Hub Message')
    elif request.method == "POST":
        if request.form['admin_key'] != admin_hash:
            redirect(url_for('admin'))

        message = request.form['message']

        con = sql.connect(environ['DATABASE_URL'])
        cur = con.cursor(cursor_factory=DictCursor)

        cur.execute(
            "UPDATE config SET setting_value=%s WHERE setting_name='hub_message'", (message,))
        con.commit()
        con.close()

        msg = "Message Changed"
        return render_template("result.html", msg=msg)


@app.route('/admin/add_sidebar_link', methods=['GET', 'POST'])
def add_sidebar_link():
    if request.method == "GET":
        return render_template('admin/add_sidebar_link.html', title='Add Sidebar Link')
    elif request.method == "POST":
        if request.form['admin_key'] != admin_hash:
            redirect(url_for('admin'))

        url = request.form['url']
        text = request.form['text']

        con = sql.connect(environ['DATABASE_URL'])
        cur = con.cursor(cursor_factory=DictCursor)

        cur.execute("SELECT * FROM config WHERE setting_name='sidebar_links';")
        sidebar_links_dict = cur.fetchone()
        sidebar_links = sidebar_links_dict[2]
        links_comb = sidebar_links.split(",,,")

        links_comb.append(url + "," + text)
        sidebar_links_str = ""
        i = 0
        while i < len(links_comb):
            sidebar_links_str = sidebar_links_str + links_comb[i]
            if i != len(links_comb) - 1:
                sidebar_links_str = sidebar_links_str + ",,,"
            i = i + 1
        cur.execute(
            "UPDATE config SET setting_value=%s WHERE setting_name='sidebar_links'", (sidebar_links_str,))
        con.commit()
        con.close()

        msg = "Link Added"
        return render_template("result.html", msg=msg)


@app.route('/admin/remove_sidebar_link', methods=['GET', 'POST'])
def remove_sidebar_link():
    if request.method == "GET":
        return render_template('admin/remove_sidebar_link.html', title='Remove Sidebar Link')
    elif request.method == "POST":
        if request.form['admin_key'] != admin_hash:
            redirect(url_for('admin'))

        text = request.form['text']

        con = sql.connect(environ['DATABASE_URL'])
        cur = con.cursor(cursor_factory=DictCursor)

        cur.execute("SELECT * FROM config WHERE setting_name='sidebar_links';")
        sidebar_links_dict = cur.fetchone()
        sidebar_links = sidebar_links_dict[2]
        links_comb = sidebar_links.split(",,,")

        i = 0
        while i < len(links_comb):
            link_str = links_comb[i]
            link = link_str.split(',')

            if link[1] == text:
                links_comb.pop(i)

            i = i + 1

        sidebar_links_str = ""
        i = 0
        while i < len(links_comb):
            sidebar_links_str = sidebar_links_str + links_comb[i]
            if i != len(links_comb) - 1:
                sidebar_links_str = sidebar_links_str + ",,,"
            i = i + 1
        cur.execute(
            "UPDATE config SET setting_value=%s WHERE setting_name='sidebar_links'", (sidebar_links_str,))
        con.commit()
        con.close()

        msg = "Link Removed"
        return render_template("result.html", msg=msg)


@app.route('/admin/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == "GET":
        return render_template('admin/change_password.html', title='Change Admin Password')
    elif request.method == "POST":
        if request.form['admin_key'] != admin_hash:
            redirect(url_for('admin'))

        message = request.form['new_password']
        hashed_pass = sha3_256(message.encode()).hexdigest()

        con = sql.connect(environ['DATABASE_URL'])
        cur = con.cursor(cursor_factory=DictCursor)

        cur.execute(
            "UPDATE config SET setting_value=%s WHERE setting_name='admin_password'", (hashed_pass,))
        con.commit()
        con.close()

        get_admin_hash()

        msg = "Password Changed"

        return render_template("result.html", msg=msg)
