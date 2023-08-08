import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, request, g, flash, session, redirect, abort
import sqlite3 as sq
import os
from FDataBase import FDataBase
from flask_login import  LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
# from aproxy import show_data

#configurations:
DATABASE = '/tmp/flsite.db'
DEBUG= True
SECRET_KEY = 'dsfdnjdfgdfgdsjjdn43438nnwj834n'

app=Flask(__name__, template_folder="public")
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager= LoginManager(app)

arrCoords ={}

@login_manager.user_loader
def load_user(user_id):
    print('load user')
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn =sqlite3.connect(app.config['DATABASE'])
    conn.row_factory =sqlite3.Row
    return conn

def create_db():
    db=connect_db()
    with app.open_resource('scripts.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase =None
@app.before_request
def before_request():
    global dbase
    db=get_db()
    dbase=FDataBase(db)

menu = [{"name":"Главная", "url": "login" }, {"name":"О проекте", "url": "about" }, {"name":"Авторизация", "url": "login" }]



@app.route("/" )
# @login_required
def index():
    return render_template('index.html', menu=dbase.getMenu())

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/login", methods=["POST", "GET"] )
def login():

    if request.method =='POST':
        user = dbase.getUserByEmail(request.form['userEmail'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))
        flash('incorrect pair log/pas ', 'error')

    return render_template('login.html', title ='Авторизация', menu=dbase.getMenu())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You exit your profile', 'success')
    return redirect(url_for('login'))

@app.route('/registration', methods=["POST", "GET"] )
def register():
    if request.method =='POST':
        if len(request.form['userName'])>2 and len(request.form['password'])>2:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['userName'], request.form['userEmail'], hash)
            if res:
                flash('yes', 'success')
                return redirect(url_for('login'))
            else:
                flash('no', 'error')
    return render_template('registration.html', title ='Авторизация', menu=dbase.getMenu())


@app.route("/about", methods=["POST", "GET"])
def about():
    print(dbase.getMenu())
    return render_template('about.html', menu=dbase.getMenu())

@app.route("/pushCoords", methods=["POST", "GET"] )
def pushCoords():
     if request.method =='POST':
        arrCoords = request.json
        g.coords = arrCoords['coords']
        print(g.coords)
     return render_template('index.html', menu=dbase.getMenu())
print(app.config['SERVER_NAME'])

if __name__ == "__main__":
    app.run(debug=True)


