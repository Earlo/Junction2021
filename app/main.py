from flask import Flask, request
from transformers import pipeline

from sentiment_scoring import process_comment, score_sentiment

app= Flask(__name__)

classifier = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    return_all_scores=True,
                    function_to_apply="sigmoid",
                    framework="pt"
                    )

@app.route("/")
def index():
  return "<h1>Junction 2021</h1>"


@app.route("/comment", methods=["POST"])
def receive_comment():
  data = request.get_json()

  user, comment = (data["user"], data["comment"])

  social_credit_change = score_sentiment(process_comment(str(comment), classifier))

  # Add comment & update the credit of the user

  return ("", 200)
