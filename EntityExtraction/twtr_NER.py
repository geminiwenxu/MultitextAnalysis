from glob import glob

import pandas as pd
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

from config import Config
from utils import get_all_files, save_to_disk


def load_data(path):
    # retrieve all files from given path
    stock_files = (glob(path + "*.csv"))
    return stock_files


def build_df(colnames, stock_files, usecols_list):
    # build a Data frame from retrieved files
    df = pd.DataFrame()
    for filename in stock_files:
        file = pd.read_csv(filename, names=colnames, usecols=usecols_list)
        file.dropna(axis=0, how='any', inplace=True)
        df = df.append(file, ignore_index=True)
    return df


def filter_df(keywords, df):
    # filter relevant df by given keywords
    text_df = pd.DataFrame()
    for index, row in df.iterrows():
        match = [word for word in row.text.split() if word in keywords]
        if len(match) > 0:
            text_df = text_df.append(row, ignore_index=True)
    return text_df


def df_to_str(df):
    text_list = []
    for index, row in df.iterrows():
        text_list.append(row.text)
    return text_list


def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        if current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                continue
    return continuous_chunk


if __name__ == "__main__":
    tweets_data_path = 'tweets_by_country/'
    all_files = get_all_files(Config.base_path + tweets_data_path, extension='csv')
    out = {}
    for country in Config.country_prefix:
        df = pd.DataFrame()
        news_files = list(filter(lambda x: country in x, all_files))
        for file in news_files:
            data = pd.read_csv(file, names=Config.colnames, usecols=Config.usecols_list)
            data.dropna(axis=0, how='any', inplace=True)
            df = df.append(data, ignore_index=True)
        text_df = filter_df(Config.keywords, df)
        text_list = df_to_str(text_df)
        text_str = '. '.join(text_list)
        namedEntities = get_continuous_chunks(text_str)
        out[country.replace('_', '')] = namedEntities
    save_to_disk(data=out,
                 path=Config.base_path + 'report_named_entities/',
                 filename='entities_by_country.json')
