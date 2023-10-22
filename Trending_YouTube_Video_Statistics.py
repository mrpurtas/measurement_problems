import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv('datasets/CAvideos.csv')

df.head()
df.columns
df["views_count_scale"] = MinMaxScaler(feature_range=(1, 5)).fit(df[["views"]]).transform(df[["views"]])
df["comment_count_scale"] = MinMaxScaler(feature_range=(1, 5)).fit(df[["comment_count"]]).transform(df[["comment_count"]])

def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)


def score_average_rating(row):
    up = row["likes"]
    down = row["dislikes"]

    if up + down == 0:
        return 0
    return up / (up + down)

df['like_score'] = df.apply(score_average_rating, axis=1)

df["like_score_scale"] = MinMaxScaler(feature_range=(1, 5)).fit(df[["like_score"]]).transform(df[["like_score"]])
df.head()

def weighted_sorting_score(dataframe, w1=50, w2=30, w3=20):
    return (dataframe["views_count_scale"] * w1 / 100 +
            dataframe["like_score_scale"] * w2 / 100 +
            dataframe["comment_count_scale"] * w3 / 100)


df["weighted_sorting_score"] = weighted_sorting_score(df)


df.sort_values(by="weighted_sorting_score", ascending=False).head(20)

