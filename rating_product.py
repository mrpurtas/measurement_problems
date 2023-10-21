import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv('datasets/course_reviews.csv')


df.head()

df.groupby("Questions Answered").agg({"Questions Answered": "count", "Rating": "mean"})
df.dtypes

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df["Timestamp"].max()
current_date = pd.to_datetime('2021-02-10 0:00:00')


df["days"] = (current_date - df["Timestamp"]).dt.days

df.loc[df["days"] <= 30, "Rating"].mean() * 28 / 100 + \
df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean() * 26 / 100 + \
df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean() * 24 / 100 + \
df.loc[(df["days"] > 180), "Rating"].mean() * 22 / 100

def time_based_weigthed_average(dataframe, w1:28, w2:26, w3:24, w4:22):
    return  dataframe.loc[dataframe["days"] <= 30, "Rating"].mean() * w1 / 100 + \
            dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
            dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
            dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100


time_based_weigthed_average(df, 30, 26, 22, 22),


def user_based_weighted_average(dataframe, w1:22, w2:24, w3:26, w4:28):
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1 / 100 + \
            dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
            dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
            dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100

df.head()

def course_weighted_rating(dataframe, time_w=50, user_w=50):
    return time_based_weighted_average(dataframe) * time_w/100 + user_based_weighted_average(dataframe)*user_w/100

course_weighted_rating(df)

course_weighted_rating(df, time_w=40, user_w=60)