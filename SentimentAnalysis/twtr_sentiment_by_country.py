import pandas as pd

from config import Config
from utils import get_all_files, filter_df, preprocess, save_to_disk, extreme_vader_sentiment


def result(total_pos, total_neu, total_neg):
    each_country_result = dict(num_pos=total_pos, num_neu=total_neu, num_neg=total_neg)
    return each_country_result


def extreme_result(extreme_pos_count, pos_count, neu_count, neg_count, extreme_neg_count):
    each_country_result = dict(num_extreme_pos=extreme_pos_count, num_pos=pos_count, num_neu=neu_count,
                               num_neg=neg_count, num_extreme_neg=extreme_neg_count)
    return each_country_result


if __name__ == "__main__":
    tweets_data_path = 'tweets_by_country/'  # _translation
    out = {}
    all_files = get_all_files(Config.data_path + tweets_data_path, extension='csv')
    for country in Config.country_prefix:  # ['de_', 'fr_', 'nl_']:
        df = pd.DataFrame()
        news_files = list(filter(lambda x: country in x, all_files))
        for file in news_files:
            data = pd.read_csv(file, names=Config.colnames, usecols=Config.usecols_list)
            data.dropna(axis=0, how='any', inplace=True)
            df = df.append(data, ignore_index=True)

        text_df = filter_df(Config.keywords, df)
        # translated_df = translation(text_df)
        cleaned_df = preprocess(df=text_df)  # df= translated_df

        extreme_pos_count, total_pos, total_neu, total_neg, extreme_neg_count = extreme_vader_sentiment(text_df)

        out[country.replace('_', '')] = extreme_result(extreme_pos_count, total_pos, total_neu, total_neg,
                                                       extreme_neg_count)

    save_to_disk(data=out,
                 path=Config.reports_path,
                 filename='all_extreme_sentiment_summary_country.json')
