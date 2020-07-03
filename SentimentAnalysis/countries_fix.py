import pandas as pd

from config import Config


def normalization(df):
    df = df.transpose()
    # pos_max = df.num_pos.max(axis=0)
    # pos_min = df.num_pos.min(axis=0)
    # df['normal_pos'] = (df.num_pos - pos_min) / (pos_max - pos_min)
    # neu_max = df.num_neu.max(axis=0)
    # neu_min = df.num_neu.min(axis=0)
    # df['normal_neu'] = (df.num_neu - neu_min) / (neu_max - neu_min)
    # neg_max = df.num_neg.max(axis=0)
    # neg_min = df.num_neg.min(axis=0)
    # df['normal_neg'] = (df.num_neg - neg_min) / (neg_max - neg_min)
    df['normal_ex_pos'] = 100 * df.num_extreme_pos / (
            df.num_extreme_pos + df.num_pos + df.num_neu + df.num_neg + df.num_extreme_neg)
    df['normal_pos'] = 100 * df.num_pos / (
            df.num_extreme_pos + df.num_pos + df.num_neu + df.num_neg + df.num_extreme_neg)
    df['normal_neu'] = 100 * df.num_neu / (
            df.num_extreme_pos + df.num_pos + df.num_neu + df.num_neg + df.num_extreme_neg)
    df['normal_neg'] = 100 * df.num_neg / (
            df.num_extreme_pos + df.num_pos + df.num_neu + df.num_neg + df.num_extreme_neg)
    df['normal_ex_neg'] = 100 * df.num_extreme_neg / (
            df.num_extreme_pos + df.num_pos + df.num_neu + df.num_neg + df.num_extreme_neg)
    return df


if __name__ == '__main__':
    df = pd.read_json(Config.reports_path + '/all_extreme_sentiment_summary_country.json')
    df = normalization(df)
    print(df)
    df = df.transpose()
    final_json = df.to_json(Config.reports_path + '/normalized_all_extreme_sentiment_country_summary.json')
