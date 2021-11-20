from typing import Dict, List
import transformers

def process_comment(comment: str, classifier: transformers.Pipeline) -> Dict:
  """
  Evaluate sentiment score for a comment.
  """

  # Model limit should be 512 characters
  comment = comment[:512]

  sentiment_scores: List = classifier(comment)

  try:
      sentiment_scores = {
          str(scorecard["label"]).lower(): float(scorecard["score"]) for scorecard in sentiment_scores[0]
      }
  
      return sentiment_scores
  except (KeyError, IndexError):
      return {
          "positive": 0.0,
          "negative": 0.0
      }


def score_sentiment(sentiment_scores: Dict) -> float:
  """
  Evaluate empathy scoring for sentiment score.
  """

  try:
      if float(sentiment_scores["negative"]) >= 0.5:
          return -5 * (float(sentiment_scores["negative"]) - 0.5) + float(sentiment_scores["positive"])
      else:
          return 1 * float(sentiment_scores["positive"])
  except KeyError:
      return 0.0
