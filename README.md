# Junction 2021 hack - Karma forum

| <img src="https://user-images.githubusercontent.com/3153681/142894250-de0b41f2-d4f2-48f4-8c06-8410dc27e203.jpg" width="400" height="200"> | <img src="https://user-images.githubusercontent.com/3153681/142895492-2d2f6b6b-bb90-42ba-8b07-7a59dea02e36.jpg" alt="Earlo's profile picture" width="400" height="200"> |
| :-------------: | :-------------: |


This is **[Karma forum](https://junction2021.herokuapp.com/login)**. A Junction 2021 hackathon submission to challenges:
* [Loupedeck](https://www.junction2021.com/challenges/loupdeck) - Creative hack for Loupedeck console. Solution won **#1 place** 🥇
* [Supercell](https://www.junction2021.com/challenges/supercell) - Fighting online hate speech.

## Problem and solution

Online communities have a lot of hateful comments. Instead of fighting individual offences, we created a solution that would incentivise positive communication.

We created a [forum](https://junction2021.herokuapp.com/login) that rewards positive communication with *Karma coins*. Comments that generate Karma coins are more likely to be displayed; users with most Karma coins are displayed on leaderboards; and users are able to trade Karma coins for a Github follower or a shoutout.

For the shoutouts, we used the [Loupedeck console](https://loupedeck.com/products/). The console has dynamically changing buttons, that allow the wielder of the console to give shoutouts (or leaderboard highlights) to users. These, we would imagine, could have interesting uses in the domain of online streaming.

## Tech stack

* **Python + Flask + Gunicorn** serverside rendering deployed to **[Heroku](https://www.heroku.com/)**
* **PostgreSQL** database deployed on **Heroku** 
* **PyTorch + [Huggingface](https://huggingface.co/transformers/index.html)** distilBERT for sentiment analysis

## Team members

| <img src="https://avatars.githubusercontent.com/u/3153681?v=3" alt="Manezki's profile picture" width="50" height="50"> | <img src="https://avatars.githubusercontent.com/u/12685733?v=4" alt="Earlo's profile picture" width="50" height="50"> |
| :-------------: | :-------------: |
| [Manezki](https://github.com/Manezki)  | [Earlo](https://github.com/Earlo/)  |
| Sentiment analysis & Karma development  | Loupedeck integration & Karma development  |
