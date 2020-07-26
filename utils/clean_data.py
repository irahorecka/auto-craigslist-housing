import datetime
import os
import pandas as pd


def filter_posts(posts):
    """Main function to read, clean, process, and generate
    craigslist housing posts within the range and specifications
    desired by the user."""
    data_cleaning_funcs = (
        clean_headers,
        rm_repost,
        convert_price_to_int,
        get_price_range,
        select_bedrooms,
        convert_date_to_dttm,
        date_one_week_today,
        sort_time_date,
    )
    for func in data_cleaning_funcs:
        posts = func(posts)

    return posts


def clean_headers(dtfm):
    """Clean header names for simple downstream handling."""
    dtfm.columns = (
        dtfm.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    return dtfm


def rm_repost(dtfm):
    """Remove repost ids."""
    dtfm_no_repost = dtfm.loc[dtfm["repost_of_post_id"] == "None"]
    dtfm_unique = dtfm.loc[dtfm["repost_of_post_id"] != "None"].drop_duplicates(
        subset="repost_of_post_id"
    )

    return dtfm_no_repost.append(dtfm_unique)


def convert_price_to_int(dtfm):
    """Convert price values to integers."""
    dtfm.price = dtfm.price.str.replace("$", "").replace(",", "").astype("int")
    return dtfm


def get_price_range(dtfm):
    """Select posts within a price range."""
    return dtfm.loc[dtfm.price.between(1800, 2800, inclusive=True)]


def select_bedrooms(dtfm):
    """Select desired bedrooms."""
    return dtfm.loc[dtfm.bedrooms == "2"]


def convert_date_to_dttm(dtfm):
    """Convert date string to datetime object."""
    dtfm.date_posted = pd.to_datetime(dtfm.date_posted)
    dtfm.time_posted = pd.to_datetime(dtfm.time_posted, format="%H:%M")
    return dtfm


def date_one_week_today(dtfm):
    """Select craigslist posts posted within one week of today."""
    return dtfm[dtfm.date_posted > datetime.datetime.now() - pd.to_timedelta("7day")]


def sort_time_date(dtfm):
    """Sort posts by time then date - newest posts first."""
    dtfm = dtfm.sort_values(by="time_posted", ascending=False)
    dtfm = dtfm.sort_values(by="date_posted", ascending=False)

    return dtfm
