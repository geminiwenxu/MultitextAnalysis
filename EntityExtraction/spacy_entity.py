import pandas as pd
import spacy

from config import Config
from utils import get_all_files, filter_df, save_to_disk


def tag(df, c_prefix):
    entities = []
    nlp = spacy.load('en')
    for index, row in df.iterrows():
        line = nlp(row.text).ents
        raw = list((map(lambda word: {'entity': word.text, 'label': word.label_, 'country': c_prefix}, line)))
        entities.extend(raw)
    return pd.DataFrame(entities)


if __name__ == "__main__":
    tweets_data_path = '../Data/tweets_by_country/'
    out = pd.DataFrame()
    out_count = {}
    all_files = get_all_files(Config.filepath + tweets_data_path, extension='csv')
    for country in Config.country_prefix:
        df = pd.DataFrame()
        news_files = list(filter(lambda x: country in x, all_files))
        for file in news_files:
            data = pd.read_csv(file, names=Config.colnames, usecols=Config.usecols_list)
            data.dropna(axis=0, how='any', inplace=True)
            df = df.append(data, ignore_index=True)
        text_df = filter_df(Config.keywords, df)
        extracted = tag(text_df, country)
        out_count.update({country: extracted.entity.value_counts().head(20).to_dict()})
        out = out.append(extracted)
    save_to_disk(out_count, Config.reports_path + 'report_named_entities/', 'spacy_entity_country.json')
    save_to_disk({'all': out.entity.value_counts().head(20).to_dict()}, Config.reports_path + 'report_named_entities/',
                 'spacy_entity_all.json')
