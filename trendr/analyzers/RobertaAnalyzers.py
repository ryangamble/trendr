from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax

task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
labels = ['negative', 'neutral', 'positive']
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)

def roberta_analyzer(text):
    """
    Gets the sentiment of a text using roberta's sentiment analyzer

    :param text: The string to perform the analysis on
    :return: A float with the polarity(-1 for negative, and 1 for positive)
    """
    encoded_input = tokenizer(text, return_tensors='tf')
    output = model(encoded_input)
    scores = output[0][0].numpy()
    scores = softmax(scores)
    if scores[0] > scores[2]:
      return -1
    else:
      return 1

def roberta_analyzer_results(text):
    """
    Gets the sentiment of a text using the roberta sentiment analyzer

    :param text: The string to perform the analysis on
    :return: A float array with the probabilities ['negative', 'neutral', 'positive']
    """
    encoded_input = tokenizer(text, return_tensors='tf')
    output = model(encoded_input)
    scores = output[0][0].numpy()
    scores = softmax(scores)
    return scores

def roberta_analyzer_dataframe(df):
    """
    Gets the sentiment of a collection of texts in a pandas dataframe using the
    roberta sentiment analyzer.

    :param df: a pandas dataframe with column "text" that contains the text to analyze
    :return: The passed dataframe, with the added column "predicted" for the sentiment
    result as -1 for negative, and 1 for positive.
    """
    df['predicted'] = 0
    for i in range(len(df)):
        encoded_input = tokenizer(df.loc[i]['Text'], return_tensors='tf')
        output = model(encoded_input)
        scores = output[0][0].numpy()
        scores = softmax(scores)
        if scores[0] > scores[2]:
            df.at[i,'predicted'] = -1
        else:
            df.at[i,'predicted'] = 1
    return df