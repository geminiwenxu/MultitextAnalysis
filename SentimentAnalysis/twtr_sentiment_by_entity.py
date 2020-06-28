import pandas as pd

from utils import get_all_files, filter_df, preprocess, save_to_disk, vader_sentiment


def result(total_pos, total_neu, total_neg):
    each_country_result = dict(num_pos=total_pos, num_neu=total_neu, num_neg=total_neg)
    return each_country_result


if __name__ == "__main__":
    base_path = '//MultitextAnalysis/'
    tweets_data_path = 'tweets_by_country/'
    keywords = ['covid-19', 'corona', 'coronavirus', 'socialdistance', 'socialdistancing', 'globalpandemic',
                'stayathome', 'FightCOVID19', 'covid', 'outbreak', 'crisis', 'virus', '#conronavirus', '#covid',
                'Coronavirus', 'Covid-19', 'Corona']
    out = {}
    all_files = get_all_files(base_path + tweets_data_path, extension='csv')
    country_prefix = ['aus_', 'cn_', 'de_', 'fr_', 'jp_', 'kr_', 'nl_', 'se_', 'sg_', 'uk_', 'usa_']
    for country in country_prefix:
        df = pd.DataFrame()
        news_files = list(filter(lambda x: country in x, all_files))
        colnames = ['author', 'text']
        usecols_list = [2, 10]
        for file in news_files:
            data = pd.read_csv(file, names=colnames, usecols=usecols_list)
            data.dropna(axis=0, how='any', inplace=True)
            df = df.append(data, ignore_index=True)
        text_df = filter_df(keywords, df)
        entities =[]
        cleaned_df = preprocess(df=text_df)

        total_pos, total_neu, total_neg = vader_sentiment(text_df)

        out[country.replace('_', '')] = result(total_pos, total_neu, total_neg)

    # save_to_disk(Data=out,
    #              path=base_path + 'report_sentiment/',
    #              filename='sentiment_summary_country.json')
