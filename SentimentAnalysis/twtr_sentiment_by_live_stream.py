import json

import pandas as pd

from config import Config
from utils import save_to_disk, preprocess, get_all_files, vader_sentiment


def load_live_tweets(tweets_data_path):
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append({'Timestamp': tweet['created_at'],
                                'text': tweet['text'],
                                'Username': tweet['user']['screen_name']})
        except:
            continue
    tweets = pd.DataFrame(tweets_data)
    return tweets


def result(total_pos, total_neu, total_neg):
    each_live_result = dict( num_pos=total_pos, num_neu=total_neu, num_neg=total_neg)
    return each_live_result


if __name__ == '__main__':
    tweets_data_path = 'tweets_stream/'
    out = {}
    files = get_all_files(Config.data_path + tweets_data_path, extension='json')
    for file in files:
        tweets = load_live_tweets(file)
        cleaned_tweets = preprocess(tweets)

        total_pos, total_neu, total_neg = vader_sentiment(cleaned_tweets)
        time_stamp = cleaned_tweets.iat[1, 0]  # get the time stamp of each live stream file
        each_live_result = result(total_pos, total_neu, total_neg)
        out.update({time_stamp: each_live_result})

    save_to_disk(data=out,
                 path=Config.reports_path,
                 filename='live_sentiment_summary.json')
