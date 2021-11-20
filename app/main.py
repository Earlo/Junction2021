import os

from flask import Flask, request, redirect, url_for
import flask_login

import json 
from transformers import pipeline

from .user import User, login_manager, users, checkPassword

app = Flask(__name__)
app.secret_key = os.environ['SECRET']

classifier = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    return_all_scores=True,
                    function_to_apply="sigmoid",
                    framework="pt"
                    )


login_manager.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = request.form['username']
    if username in users():
      if checkPassword(request.form['password']):
          print("logged in")
          user = User()
          user.id = username
          flask_login.login_user(user)
          return redirect(url_for('protected'))
    else:
      print('creating user')
      #TODO create user
      pass

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    #TODO message prompt here
    #TODO logout button
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'
