from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

def pattern_analyzer(text):
	"""
	Gets the sentiment of a text using TextBlob's pattern analyzer

	:param text: The string to perform the analysis on
	:return: A namedtuple in the form Sentiment(polarity, subjectivity)
	"""
	tb = TextBlob(text)
	return tb.sentiment

def naive_bayes(text):
	"""
	Gets the sentiment of a text using TextBlob's Naive Bayes analyzer

	:param text: The string to perform the analysis on
	:return: A namedtuple in the form Sentiment(classification, p_pos, p_neg)
	"""
	tb = Blobber(analyzer=NaiveBayesAnalyzer())
	return tb(text).sentiment

def vader(text):
	"""
	Gets the sentiment of a text using the NLTK's VADER

	:param text: The string to perform the analysis on
	:return: A dictionary with the keys {'neg', 'neu', 'pos', 'compound'}
	"""
	sia = SentimentIntensityAnalyzer()
	return sia.polarity_scores(text)

def pattern_analyzer_texts(texts):
	"""
	Gets the sentiment of multiple texts using TextBlob's pattern analyzer

	:param texts: The array of texts to perform analyses on
	:return: An array of namedtuples in the form Sentiment(polarity, subjectivity)
	"""
	scores = []

	for text in texts:
		tb = TextBlob(text)
		scores.append(tb.sentiment)
	
	return scores

def naive_bayes_texts(texts):
	"""
	Gets the sentiment of multiple texts using TextBlob's Naive Bayes analyzer

	:param text: The array of texts to perform analyses on
	:return: An array of namedtuples in the form Sentiment(classification, p_pos, p_neg)
	"""
	scores = []
	tb = Blobber(analyzer=NaiveBayesAnalyzer())

	for text in texts:
		scores.append(tb(text).sentiment)
	
	return scores

def naive_bayes_texts(texts):
	"""
	Gets the sentiment of multiple texts using NLTK's VADER

	:param text: The array of texts to perform analyses on
	:return: An array of dictionaries with the keys {'neg', 'neu', 'pos', 'compound'}
	"""
	scores = []
	sia = SentimentIntensityAnalyzer()

	for text in texts:
		scores.append(sia.polarity_scores(text))
	
	return scores