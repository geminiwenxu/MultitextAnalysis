import pandas as pd
from config import Config
from utils import get_all_files, filter_df, preprocess, save_to_disk, vader_sentiment


def result(total_pos, total_neu, total_neg):
    each_country_result = dict(num_pos=total_pos, num_neu=total_neu, num_neg=total_neg)
    return each_country_result


if __name__ == "__main__":
    base_path = '//MultitextAnalysis/'
    tweets_data_path = 'tweets_by_country/'
    out = {}
    all_files = get_all_files(base_path + tweets_data_path, extension='csv')
    for country in Config.country_prefix:
        df = pd.DataFrame()
        news_files = list(filter(lambda x: country in x, all_files))
        for file in news_files:
            data = pd.read_csv(file, names=Config.colnames, usecols=Config.usecols_list)
            data.dropna(axis=0, how='any', inplace=True)
            df = df.append(data, ignore_index=True)
        text_df = filter_df(Config.keywords, df)
        cleaned_df = preprocess(df=text_df)

        total_pos, total_neu, total_neg = vader_sentiment(text_df)

        out[country.replace('_', '')] = result(total_pos, total_neu, total_neg)

    save_to_disk(data=out,
                 path=base_path + 'report_sentiment/',
                 filename='sentiment_summary_country.json')
