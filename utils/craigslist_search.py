import csv
import datetime
import os
import requests
from craigslist import CraigslistHousing
import pandas as pd
from . import get_static_file

CODE_BREAK = ";n@nih;"


def scrape_housing(craigslist_region, housing_category="apa"):
    """Module function to appropriately scrape and write Craigslist
    housing information using specified housing categories and filters."""
    if len(craigslist_region) == 4:
        state, region, sub_region, geotag_bool = craigslist_region
    else:
        state, region, geotag_bool = craigslist_region
        sub_region = ""

    posts = query_housing_data(state, region, sub_region, housing_category, geotag_bool)
    posts = [post.split(CODE_BREAK) for post in posts]
    posts_column = posts.pop(0)
    print(posts[1])
    return pd.DataFrame(posts, columns=posts_column)


def query_housing_data(state, reg, sub_reg, housing_category, geotag):
    """A function to apply housing filters and instantiate
    craigslist.CraigslistHousing object with appropriate data."""

    search_filters = get_static_file.search_filters()
    try:
        if sub_reg:
            housing_object = CraigslistHousing(
                site=reg,
                area=sub_reg,
                category=housing_category,
                filters=search_filters,
            )
            return mine_housing_data(
                housing_object, state, reg, housing_category, geotag, sub_reg=sub_reg
            )
        else:
            housing_object = CraigslistHousing(
                site=reg, category=housing_category, filters=search_filters
            )
            return mine_housing_data(
                housing_object, state, reg, housing_category, geotag
            )
    except requests.exceptions.ConnectionError as error:
        # PATCH THIS FOR BETTER HANDLING
        print(error)
        return


def mine_housing_data(
    housing_obj, state, region, housing_category, geotagged, sub_reg="",
):
    """A function to appropritely concatenate information sourced from
    the Craigslist housing object to a header list for downstream CSV
    export."""

    header = [
        f"State or Country{CODE_BREAK}Region{CODE_BREAK}"
        f"Subregion{CODE_BREAK}Housing Category{CODE_BREAK}"
        f"Post ID{CODE_BREAK}Repost of (Post ID){CODE_BREAK}"
        f"Title{CODE_BREAK}URL{CODE_BREAK}"
        f"Date Posted{CODE_BREAK}Time Posted{CODE_BREAK}"
        f"Price{CODE_BREAK}Location{CODE_BREAK}"
        f"Post has Image{CODE_BREAK}Post has Geotag{CODE_BREAK}"
        f"Bedrooms{CODE_BREAK}Area"
    ]
    try:
        header.extend(
            [
                f"{state}{CODE_BREAK}{region}{CODE_BREAK}"
                f"{sub_reg if sub_reg else region}{CODE_BREAK}"
                f"{get_static_file.housing_categories().get(housing_category)}{CODE_BREAK}"
                f"{post['id']}{CODE_BREAK}{post['repost_of']}{CODE_BREAK}"
                f"{post['name']}{CODE_BREAK}{post['url']}{CODE_BREAK}"
                f"{post['datetime'][0:10]}{CODE_BREAK}{post['datetime'][11:]}{CODE_BREAK}"
                f"{post['price']}{CODE_BREAK}{post['where']}{CODE_BREAK}"
                f"{post['has_image']}{CODE_BREAK}{post['geotag']}{CODE_BREAK}"
                f"{post['bedrooms']}{CODE_BREAK}{post['area']}"
                for post in housing_obj.get_results(
                    sort_by=None, geotagged=geotagged, limit=None
                )
            ]
        )
        return header
    except (AttributeError, OSError) as error:
        print(error)
        return
