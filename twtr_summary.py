import glob
import json

import pandas as pd


def group_and_rename(data: pd.DataFrame, by: list, cols_to_keep: list, func: list):
    data = data.groupby(by=by)[cols_to_keep].aggregate(func)
    # 1. drop one count column
    data.columns = data.columns.map('-'.join)
    data.drop(labels=cols_to_keep[1] + '-count', axis=1, inplace=True)
    # 2. rename column names
    data.columns = ['total_tweets', 'avg_retweets', 'avg_length_tweets']
    if len(by) > 1:
        data.index = data.index.to_series().apply(lambda x: '{0}-{1}'.format(*x))
    return data


def convert_df_to_dict(data: pd.DataFrame, summary: bool = False):
    if summary:
        return {"Data": data.to_dict(orient='records')}
    else:
        return data.to_dict(orient='index')


def save_to_disk(data, path, filename):
    with open(path + filename, 'w') as f:
        json.dump(data, f)
    return None


if __name__ == '__main__':

    path = '/MultitextAnalysis/tweets_by_country/'  # use your path
    all_files = glob.glob(path + "*.csv")
    # create a dataframe strcture
    df = pd.DataFrame()
    colnames = ['author_id', 'author', 'source', 'retweet_count', 'tweet_length', 'tweet_language']

    for file in all_files:
        temp_df = pd.read_csv(file,
                              usecols=[1, 2, 3, 7, 8, 9],
                              names=colnames)
        temp_df.dropna(axis=0,
                       how='any',
                       inplace=True)
        temp_df['author_id'] = temp_df['author_id'].astype(dtype='int64', errors='ignore')
        temp_df['retweet_count'] = temp_df['retweet_count'].astype(dtype='int64', errors='ignore')
        temp_df['tweet_length'] = temp_df['tweet_length'].astype(dtype='int64', errors='ignore')
        # append the dataframe
        df = df.append(temp_df, ignore_index=True)

    for item in [('tweet_language',), ('author',), ('source',), ('author', "tweet_language"),
                 ('source', "tweet_language")]:
        df_stats = group_and_rename(data=df,
                                    by=list(item),
                                    cols_to_keep=['retweet_count', 'tweet_length'],
                                    func=['count', 'mean'])
        converted = convert_df_to_dict(data=df_stats)
        save_to_disk(data=converted,
                     path=path,
                     filename="_".join(list(item)) + '.json')

    converted_summery = convert_df_to_dict(data=df, summary=True)
    save_to_disk(data=converted_summery,
                 path=path,
                 filename='summary.json')


