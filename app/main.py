from flask import Flask

from transformers import pipeline

app= Flask(__name__)

classifier = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    return_all_scores=True,
                    function_to_apply="sigmoid",
                    framework="pt"
                    )

@app.route('/')
def index():
  return "<h1>Junction 2021</h1>"

