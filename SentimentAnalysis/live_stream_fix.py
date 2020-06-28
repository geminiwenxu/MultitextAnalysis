from datetime import datetime

import pandas as pd


def time_stamp(df):
    df = df.transpose()
    for index, row in df.iterrows():
        dtime = row.time_stamp
        new_datetime = datetime.strftime(datetime.strptime(dtime, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
        row.time_stamp = new_datetime
    df = df[::-1]
    df = df.sort_values(by=['time_stamp'])
    return df


def normalization(df):
    pos_max = df.num_pos.max(axis=0)
    pos_min = df.num_pos.min(axis=0)
    df['normal_pos'] = (df.num_pos - pos_min) / (pos_max - pos_min)
    neu_max = df.num_pos.max(axis=0)
    neu_min = df.num_pos.min(axis=0)
    df['normal_neu'] = (df.num_neu - neu_min) / (neu_max - neu_min)
    neg_max = df.num_neg.max(axis=0)
    neg_min = df.num_neg.min(axis=0)
    df['normal_neg'] = (df.num_neg - neg_min) / (neg_max - neg_min)
    return df


if __name__ == '__main__':
    base_path = '//MultitextAnalysis/report_sentiment/'
    df = pd.read_json(base_path + 'live_sentiment_summary.json')
    df = time_stamp(df)

    df = normalization(df)
    df = df.transpose()

    final_json = df.to_json(
        '/Users/geminiwenxu/PycharmProjects/MultitextAnalysis/MultitextAnalysis/report_sentiment/normalized_live_sentiment_summary.json')
