from flask import Flask, render_template, url_for, request, g, flash, session, redirect, abort
import sqlite3 as sq
import os
# from aproxy import show_data

#configurations:
DATABASE = '/tmp/flsite.db'
DEBUG= True



app=Flask(__name__, template_folder="public")
app.config['SECRET_KEY'] = 'dsfdnjsnjdsjjdn43438nnwj834n'

menu = [{"name":"Главная", "url": "login" }, {"name":"О проекте", "url": "about" }]
arrCoords ={}

# @app.route("/", methods=["POST", "GET"] )
# def index():
#     return render_template('index.html', menu=menu)

@app.route("/login", methods=["POST", "GET"] )
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', userName = session['userLogged']))
    elif request.method=='POST' and request.form['userName'] == 'iii' and request.form['password'] =='aaa':
        session['userLogged'] = request.form['userName']
        return redirect(url_for('profile', userName = session['userLogged']))

    return render_template('login.html', menu=menu)

@app.route("/profile/<userName>")
def profile(userName):
    if 'userLogged' not in session or session['userLogged'] != userName:
        abort(401)
    return render_template('index.html', menu=menu)
    # if request.method =='POST':
    #     print(request.form['userName'])
    #     if len(request.form['userName']) >2:
    #         flash('Регистрация завершена!', category='success')
    #     else:
    #         flash('Ошибка регистрации', category='error')

    # return render_template('index.html', menu=menu)


@app.route("/pushCoords", methods=["POST", "GET"] )
def pushCoords():
     if request.method =='POST':
        arrCoords = request.json
        g.coords = arrCoords['coords']
        print(g.coords)
     return render_template('index.html', menu=menu)





@app.route("/about")
def about():
    session.pop('userLogged', None)
    return render_template('about.html', title='О проекте', menu=menu)




if __name__ == "__main__":
    app.run(debug=True)

