import datetime
import pandas as pd

# TODO: turn off warnings


def filter_posts(posts, param):
    """Main function to read, clean, process, and generate
    craigslist housing posts within the range and specifications
    desired by the user."""
    data_cleaning_funcs = [
        clean_headers,
        rm_repost,
        convert_price_to_int,
        get_price_range,
        convert_date_to_dttm,
        date_one_week_today,
        sort_time_date,
    ]
    if param.get("housing_type") == "apa":
        data_cleaning_funcs.extend(
            [select_bedrooms, convert_area_to_int, get_area_range]
        )
    for func in data_cleaning_funcs:
        posts = func(posts, param=param)
    return posts


def clean_headers(dtfm, **kwargs):
    """Clean header names for simple downstream handling."""
    dtfm.columns = (
        dtfm.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    return dtfm


def rm_repost(dtfm, **kwargs):
    """Remove repost ids."""
    dtfm_no_repost = dtfm.loc[dtfm["repost_of_post_id"] == "None"]
    dtfm_unique = dtfm.loc[dtfm["repost_of_post_id"] != "None"].drop_duplicates(
        subset="repost_of_post_id"
    )

    return dtfm_no_repost.append(dtfm_unique)


def convert_price_to_int(dtfm, **kwargs):
    """Convert price values to integers."""
    dtfm.price = dtfm.price.str.replace("$", "").str.replace(",", "").astype("int")
    return dtfm


def convert_area_to_int(dtfm, **kwargs):
    """Convert area values to integers."""
    dtfm = dtfm.loc[dtfm.area != "None"]
    dtfm.area = dtfm.area.str.replace("ft2", "").astype("int")
    return dtfm


def get_price_range(dtfm, **kwargs):
    """Select posts within a price range."""
    min_price = kwargs["param"].get("min_price")
    max_price = kwargs["param"].get("max_price")
    if not min_price and not max_price:
        return dtfm
    if not min_price:
        return dtfm.loc[dtfm.price <= max_price]
    if not max_price:
        return dtfm.loc[dtfm.price >= min_price]
    return dtfm.loc[dtfm.price.between(min_price, max_price, inclusive=True)]


def get_area_range(dtfm, **kwargs):
    """Select posts within a area (sqft) range."""
    min_sqft = kwargs["param"].get("min_sqft")
    max_sqft = kwargs["param"].get("max_sqft")
    if not min_sqft and not max_sqft:
        return dtfm
    if not min_sqft:
        return dtfm.loc[dtfm.area <= max_sqft]
    if not max_sqft:
        return dtfm.loc[dtfm.area >= min_sqft]
    return dtfm.loc[dtfm.area.between(min_sqft, max_sqft, inclusive=True)]


def select_bedrooms(dtfm, **kwargs):
    """Select posts within a bedrooms range."""
    dtfm = convert_bedrooms_to_int(dtfm)
    min_bedrooms = kwargs["param"].get("min_bedrooms")
    max_bedrooms = kwargs["param"].get("max_bedrooms")
    if not min_bedrooms and not max_bedrooms:
        return dtfm
    if not min_bedrooms:
        return dtfm.loc[dtfm.bedrooms <= max_bedrooms]
    if not max_bedrooms:
        return dtfm.loc[dtfm.bedrooms >= min_bedrooms]
    return dtfm.loc[dtfm.bedrooms.between(min_bedrooms, max_bedrooms, inclusive=True)]


def convert_date_to_dttm(dtfm, **kwargs):
    """Convert date string to datetime object."""
    dtfm.date_posted = pd.to_datetime(dtfm.date_posted)
    dtfm.time_posted = pd.to_datetime(dtfm.time_posted, format="%H:%M")
    return dtfm


def date_one_week_today(dtfm, **kwargs):
    """Select craigslist posts posted within one week of today."""
    return dtfm[dtfm.date_posted > datetime.datetime.now() - pd.to_timedelta("7day")]


def sort_time_date(dtfm, **kwargs):
    """Sort posts by time then date - newest posts first."""
    dtfm = dtfm.sort_values(by="time_posted", ascending=False)
    dtfm = dtfm.sort_values(by="date_posted", ascending=False)

    return dtfm


def convert_bedrooms_to_int(dtfm):
    """Convert bedroom values to integers."""
    dtfm = dtfm.loc[dtfm.bedrooms != "None"]
    dtfm.bedrooms = dtfm.bedrooms.astype("int")
    return dtfm
