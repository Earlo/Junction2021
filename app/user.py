import flask_login
from flask import redirect, url_for

login_manager = flask_login.LoginManager()

import os
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL']

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ShoutOut(metaclass=Singleton):
    current = None
    waiting = []

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
def users():
    with conn.cursor() as cur:
        cur.execute("SELECT username, socialcredit FROM chatUser;")
        result = cur.fetchall()
    return result

def comments():
    with conn.cursor() as cur:
        cur.execute("SELECT id, content, poster, score FROM comments;")
        result = cur.fetchall()
    print("found comments", result, type(result))
    return result


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

def getCredits(username: str) -> float:
    with conn.cursor() as cur:
        try:
            cur.execute(f"SELECT socialcredit FROM chatUser WHERE username = '{username}' LIMIT 1;")
            return cur.fetchone()[0]
        except psycopg2.ProgrammingError:
            print("User was not found")
            return 0.0


def getBoughtGithub(username: str) -> bool:
    with conn.cursor() as cur:
        try:
            cur.execute(f"SELECT bought_gh FROM chatUser WHERE username = '{username}' LIMIT 1;")
            return bool(cur.fetchone()[0])
        except psycopg2.ProgrammingError:
            print("User was not found")
            return False


def createUser(username, password):
    with conn.cursor() as cur:
        # TODO Should be unique?
        cur.execute(f"INSERT into chatUser values('{username}','{password}');")
    conn.commit()
    return True

def updateSocialCredit(username: str, socialCreditChange: float):

    with conn.cursor() as cur:
        cur.execute(f"SELECT username, socialcredit FROM chatUser WHERE username = '{username}' LIMIT 1;")

        try:
            user, socialcredit = cur.fetchone()
        except psycopg2.ProgrammingError:
            print(f"User with username {username} was not found in DB")
            return False

        cur.execute(f"UPDATE chatUser SET socialcredit = {socialcredit + socialCreditChange} WHERE username = '{user}';")
        conn.commit()
        return True


def saveComment(comment, user, score):
    with conn.cursor() as cur:
        cur.execute(f"""INSERT into comments(content, poster, score) values ('{comment.replace("'", "''")}', '{user}', '{score}');""")
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
    return redirect(url_for('login'))
