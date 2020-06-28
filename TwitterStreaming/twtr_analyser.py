import numpy as np
import pandas as pd
from textblob import TextBlob
import re


class TweetAnalyzer:
    """
    Functionality for analyzing and categorizing content from tweets_by_country.
    """
    @staticmethod
    def tweets_to_data_frame(tweets):  # Convert the tweets_by_country to dataframe
        # DataFrame allows us to make dataFrame out what we feed in
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])  # df = Data fre
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['location'] = np.array([tweet.geo for tweet in tweets])

        return df

    @staticmethod
    def filter_convert_pd(tweets):
        return pd.DataFrame.from_dict({'author_id': [tweets.author.id],
                                       'author_name': [tweets.author.name],
                                       'source': [tweets.source],
                                       'id': [tweets.id],
                                       'created_at': [tweets.created_at],
                                       'retweeted': [tweets.retweeted],
                                       'retweet_count': [tweets.retweet_count],
                                       'length': [len(tweets.text)],
                                       'language': [tweets.lang],
                                       'text': [tweets.text]})
