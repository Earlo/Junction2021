import flask_login

login_manager = flask_login.LoginManager()

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
def users():
    cur = conn.cursor()
    return cur.execute("SELECT * FROM user;")

def checkPassword(username, password):
    cur = conn.cursor()
    result = cur.execute(f"SELECT * FROM user WHERE username = {username};")
    #plaintext password :D...
    return result.password == password

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
