import datetime
import os
import pandas as pd
from .paths import BASE_DIR, DATA_DIR


def filter_results():
    peninsula = pd.read_csv(
        os.path.join(DATA_DIR, "CraigslistHousing_california_pen.csv")
    )
    cleaning_funcs = (
        clean_headers,
        rm_repost,
        convert_price_to_int,
        get_price_range,
        select_bedrooms,
        convert_date_to_dttm,
        date_one_week_today,
    )
    for func in cleaning_funcs:
        peninsula = func(peninsula)

    peninsula.to_csv(os.path.join(DATA_DIR, "cleaned_peninsula_housing.csv"))


def clean_headers(dtfm):
    dtfm.columns = (
        dtfm.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    return dtfm


def rm_repost(dtfm):
    dtfm_no_repost = dtfm.loc[dtfm["repost_of_post_id"] == "None"]
    dtfm_unique = dtfm.loc[dtfm["repost_of_post_id"] != "None"].drop_duplicates(
        subset="repost_of_post_id"
    )

    return dtfm_no_repost.append(dtfm_unique)


def convert_price_to_int(dtfm):
    dtfm.price = dtfm.price.str.replace("$", "").replace(",", "").astype("int")
    return dtfm


def get_price_range(dtfm):
    return dtfm.loc[dtfm.price.between(1800, 2800, inclusive=True)]


def select_bedrooms(dtfm):
    return dtfm.loc[dtfm.bedrooms == "2"]


def convert_date_to_dttm(dtfm):
    dtfm.date_posted = pd.to_datetime(dtfm.date_posted)
    dtfm.time_posted = pd.to_datetime(dtfm.time_posted, format="%H:%M")
    return dtfm


def date_one_week_today(dtfm):
    return dtfm[dtfm.date_posted > datetime.datetime.now() - pd.to_timedelta("7day")]
