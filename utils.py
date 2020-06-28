import json
import pickle
import re
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_all_files(path, extension='json'):
    # retrieve all files from given path
    stock_files = (glob(path + "*." + extension))
    return stock_files


def filter_df(keywords, df):
    # filter relevant df by given keywords
    text_df = pd.DataFrame()
    for index, row in df.iterrows():
        match = [word for word in row.text.split() if word in keywords]
        if len(match) > 0:
            text_df = text_df.append(row, ignore_index=True)
    return text_df


def preprocess(df):
    cleaned_df = pd.DataFrame()
    for index, row in df.iterrows():
        row.text = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s", " ", row.text)
        row.text = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " ", row.text)
        row.text = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$", " ", row.text)
        row.text = row.text.lower()
        row.text = re.sub(r"that's", "that is", row.text)
        row.text = re.sub(r"there's", "there is", row.text)
        row.text = re.sub(r"what's", "what is", row.text)
        row.text = re.sub(r"where's", "where is", row.text)
        row.text = re.sub(r"it's", "it is", row.text)
        row.text = re.sub(r"who's", "who is", row.text)
        row.text = re.sub(r"i'm", "i am", row.text)
        row.text = re.sub(r"she's", "she is", row.text)
        row.text = re.sub(r"he's", "he is", row.text)
        row.text = re.sub(r"they're", "they are", row.text)
        row.text = re.sub(r"who're", "who are", row.text)
        row.text = re.sub(r"ain't", "am not", row.text)
        row.text = re.sub(r"wouldn't", "would not", row.text)
        row.text = re.sub(r"shouldn't", "should not", row.text)
        row.text = re.sub(r"can't", "can not", row.text)
        row.text = re.sub(r"couldn't", "could not", row.text)
        row.text = re.sub(r"won't", "will not", row.text)
        row.text = re.sub(r"\W", " ", row.text)
        row.text = re.sub(r"\d", " ", row.text)
        row.text = re.sub(r"\s+[a-z]\s+", " ", row.text)
        row.text = re.sub(r"\s+[a-z]$", " ", row.text)
        row.text = re.sub(r"^[a-z]\s+", " ", row.text)
        row.text = re.sub(r"\s+", " ", row.text)
        cleaned_df = cleaned_df.append(row, ignore_index=True)
    return cleaned_df


def get_vectorizer(vectorizer_path):
    # open the tf-idf model
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    return vectorizer


def get_classifier(classifier_path):
    # open the classifier
    with open(classifier_path, 'rb') as f:
        clf = pickle.load(f)
    return clf


def sentiment_calculation(text_df, clf, vectorizer):
    # read each tweet from text_df and using the classifier to predict the sentiment of each tweet
    total_pos = 0
    total_neg = 0
    for index, row in text_df.iterrows():
        sentiment = clf.predict(vectorizer.transform([row.text]).toarray())
        print(sentiment)
        if sentiment[0] == 1:
            total_pos += 1
        else:
            total_neg -= 1
    return total_pos, total_neg


def vader_sentiment(text_df):
    analyzer = SentimentIntensityAnalyzer()
    pos_count = 0
    pos_correct = 0
    neg_count = 0
    neg_correct = 0
    neu_count = 0
    for index, row in text_df.iterrows():
        polarity = analyzer.polarity_scores(row.text)
        print(row.text, polarity)
        if polarity['compound'] > 0.5:
            pos_count += 1
        elif polarity['compound'] < -0.5:
            neg_count += 1
        else:
            neu_count += 1
    return pos_count, neu_count, neg_count


def save_to_disk(data, path, filename):
    with open(path + filename, 'w') as f:
        json.dump(data, f)
    return None


def plot_sentiment(total_pos, total_neg):
    # sentiment report
    objects = ["Positive", "Negative"]
    y_pos = np.arange(len(objects))
    print(total_neg, total_pos)
    plt.bar(y_pos, [total_pos, total_neg], alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('number')
    plt.title('number of Positive and Negative Tweets')
    return plt.show()

    # vectorizer_path = '/MultitextAnalysis/model_Naive_bayes/NB_vectorizer.pickle'
    # classifier_path = '/MultitextAnalysis/model_Naive_bayes/NB_classifier.pickle'
    #
    # vectorizer = get_vectorizer(vectorizer_path)
    # classifier = get_classifier(classifier_path)
    #
    # text_df = cleaned_df
    # clf = classifier
    # vectorizer = vectorizer
    # total_pos, total_neg = sentiment_calculation(text_df, clf, vectorizer)
    # sentiment_report = plot_sentiment(total_neg, total_pos)
