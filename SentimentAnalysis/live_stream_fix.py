import pandas as pd

from config import Config

if __name__ == '__main__':
    df_time = pd.read_json(Config.reports_path + 'live_sentiment_summary.json').transpose()
    # df.index = df.index.set_names(['time'])
    # df_time = df.reset_index().rename(columns={df.index.name: 'time'})
    df_time = df_time.reset_index()
    df_time['index'] = df_time['index'].apply(lambda x: x.date())
    df_time = df_time.groupby('index').sum()
    df_time['net_sentiment'] = df_time.num_pos - df_time.num_neg
    df_time.net_sentiment.plot()
    # final_json = df_time.to_json(Config.reports_path + 'normalized_live_sentiment_summary.json')
    print()
