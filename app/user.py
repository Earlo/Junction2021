import flask_login

login_manager = flask_login.LoginManager()

import os
import psycopg2

DATABASE_URL =  os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
def users():
    with conn.cursor() as cur:
        cur.execute("SELECT username FROM chatUser;")
        result = cur.fetchall()
    print("found users", result, type(result))
    print("user 0", result[0][0], type(result[0][0]))
    return map(lambda x: x[0], result) 

def userNameExists(username):
    with conn.cursor() as cur:
        cur.execute(f"SELECT exists (SELECT 1 FROM chatUser WHERE username = '{username}' LIMIT 1);")
        #plaintext password :D...
        result = cur.fetchone()
    print("userNameExists", result)
    return result[0]

    
def checkPassword(username, password):
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM chatUser WHERE username = '{username}';")
        #plaintext password :D...
        user = cur.fetchone()
    if user is not None:
        print("found user", user)
        return user[1] == password
    return False

def createUser(username, password):
    with conn.cursor() as cur:
        cur.execute(f"insert into chatUser values('{username}','{password}');")
    conn.commit()
    return True

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if not userNameExists(username):
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if not userNameExists(username):
        return

    user = User()
    user.id = username
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
