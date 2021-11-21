import os
import jinja2
import numpy
import requests

from flask import Flask, request, redirect, url_for
import flask_login

from transformers import pipeline

from .user import User, login_manager, userNameExists, checkPassword, createUser, updateSocialCredit, users, comments, saveComment, getCredits, getBoughtGithub

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

DISPLAY_COMMENT_LIMIT = 10

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

    platform_comments = comments()

    # Sample DISPLAY_COMMENT_LIMIT comments with weighting on the score
    if len(platform_comments) > DISPLAY_COMMENT_LIMIT:

        scores = [float(c[3]) for c in platform_comments]

        softmaxes = numpy.exp(scores) / numpy.sum(numpy.exp(scores))

        platform_comment_indexes = numpy.random.choice(len(softmaxes), size=DISPLAY_COMMENT_LIMIT, replace=False, p=softmaxes)

        platform_comments = numpy.array(platform_comments)[platform_comment_indexes]

    comment_items = [{'content': str(c[1]), 'poster': str(c[2]), 'score': float(c[3])} for c in platform_comments]

    return template.render(
        username = user,
        users = stored_users,
        comments = comment_items,
        gh_available = not getBoughtGithub(user)
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

@flask_login.login_required
@app.route("/gh-purchase", methods=["GET", "POST"])
def buy_gh_follower():

    print(request.form)
    print(request)

    if request.method == 'GET':

        template = templateEnv.get_template("gh-purchase.jinja")
        return template.render()

    elif request.method == "POST":

        gh_profile_url = request.form["github_profile_url"]
        gh_profile_name = gh_profile_url.removeprefix("https://github.com/")

        user = flask_login.current_user.id

        if getBoughtGithub(user):
            return "No more followers available for sale. Sorry"

        if getCredits(user) < 25:
            return "Insufficient credits. Need 25 karma coins for Github follower."

        response = requests.put(
            f"https://api.github.com/user/following/{gh_profile_name}",
            headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"token {os.environ['GH_JANNE']}"
            }
        )

        if response.status_code == 204:
            updateSocialCredit(user, -25)
            return "Congratulations on your new follower: https://github.com/Manezki"
        else:
            return "Something went wrong with the purchase, did you supply Github profile link in the form https://github.com/USERNAME?"
