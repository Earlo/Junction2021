import os
import jinja2

from flask import Flask, request, redirect, url_for
import flask_login

import json
from transformers import pipeline

from .user import User, login_manager, userNameExists, checkPassword, createUser, updateSocialCredit, users, comments, saveComment

from .sentiment_scoring import process_comment, score_sentiment

app = Flask(__name__)
app.secret_key = os.environ['SECRET']

classifier = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    return_all_scores=True,
                    function_to_apply="sigmoid",
                    framework="pt"
                    )

template_dir = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__), "templates"
    )
)
templateLoader = jinja2.FileSystemLoader(searchpath=template_dir)
templateEnv = jinja2.Environment(loader=templateLoader)

login_manager.init_app(app)

def loginAs(username):
    user = User()
    user.id = username
    flask_login.login_user(user)
    return redirect(url_for('protected'))

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == 'GET':
        try:
            if flask_login.current_user.id is not None:
                return redirect(url_for('protected'))
        except AttributeError:
            pass

        template = templateEnv.get_template("login.jinja")

        return template.render()

    username = request.form['username']
    password = request.form['password']

    if userNameExists(username):
        if checkPassword(username, password):
            print("logging in as", username)
            return loginAs(username)
        else:
            print("wrong password")
    else:
        print('creating user', username)
        createUser(username, password)
        return loginAs(username)
    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():

    template = templateEnv.get_template("protected.jinja")

    user = flask_login.current_user.id

    stored_users = {
        user: sc for (user, sc) in users()
    }

    comment_items = list(map(lambda c : {'id': c[0], 'content': c[1], 'poster': c[2], 'score': c[3]}, comments()))
    print("comm", comment_items)
    return template.render(
        username = user,
        users = stored_users,
        comments = comment_items
    )


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route("/comment", methods=["POST", "GET"])
def receive_comment():
    if request.method == 'GET':
        return ''
    if request.method == 'POST':
        data = request.form    
        user, comment = (data["user"], data["comment"])

        social_credit_change = score_sentiment(process_comment(str(comment), classifier))

        if updateSocialCredit(user, social_credit_change):
            saveComment(comment, user, social_credit_change)
        return redirect(url_for('protected'))

@app.route("/gh-purchase", methods=["GET", "POST"])
def buy_gh_follower():
    if request.method == 'GET':

        template = templateEnv.get_template("gh-purchase.jinja")

        return template.render()

    if request.method == 'POST':

        return "Not implemented"
