from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

def pattern_analyzer(text):
  tb = TextBlob(text)
  return tb.sentiment

def naive_bayes(text):
  tb = Blobber(analyzer=NaiveBayesAnalyzer())
  return tb(text).sentiment

def vader(text):
  sia = SentimentIntensityAnalyzer()
  return sia.polarity_scores(text)