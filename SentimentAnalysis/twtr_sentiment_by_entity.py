import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from config import Config
from utils import get_all_files, filter_df, save_to_disk


def check_entity(text_df, entities=Config.entities):
    analyzer = SentimentIntensityAnalyzer()
    pos_count = 0
    neg_count = 0
    neu_count = 0
    per_entity = {}
    per_country = {}
    for entity in entities:
        for index, row in text_df.iterrows():
            if entity in row.text:
                polarity = analyzer.polarity_scores(row.text)
                if polarity['compound'] > 0.5:
                    pos_count += 1
                elif polarity['compound'] < -0.5:
                    neg_count += 1
                else:
                    neu_count += 1
        per_entity.update({entity: {'num_pos': pos_count, 'num_neu': neu_count, 'num_neg': neg_count}})
    per_country.update(per_entity)
    return per_country


if __name__ == "__main__":
    tweets_data_path = 'tweets_by_country/'
    out = {}
    all_files = get_all_files(Config.data_path + tweets_data_path, extension='csv')
    for country in Config.country_prefix:
        df = pd.DataFrame()
        news_files = list(filter(lambda x: country in x, all_files))
        for file in news_files:
            data = pd.read_csv(file, names=Config.colnames, usecols=Config.usecols_list)
            data.dropna(axis=0, how='any', inplace=True)
            df = df.append(data, ignore_index=True)
        text_df = filter_df(Config.keywords, df)
        entity_sa = check_entity(text_df, entities=Config.entities)

        out[country.replace('_', '')] = entity_sa

    save_to_disk(data=out,
                 path=Config.reports_path,
                 filename='sentiment_summary_entity.json')
