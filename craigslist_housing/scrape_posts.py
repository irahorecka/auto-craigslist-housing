import sys
import requests

try:
    from craigslist import CraigslistHousing
except requests.exceptions.ConnectionError:
    print("Connection error encountered... Try again.")
    sys.exit(1)
import pandas as pd
import utils

CODE_BREAK = ";n@nih;"


def scrape(housing_category, geotagged=False):
    """Function to scrape and write Craigslist housing
    information using specified housing categories and filters."""
    posts = query_data(housing_category, geotagged)
    if not posts:
        return None  # catch in main.py

    posts = [post.split(CODE_BREAK) for post in posts]
    posts_column = posts.pop(0)

    return pd.DataFrame(posts, columns=posts_column)


def query_data(housing_category, geotag):
    """Function to apply housing filters and instantiate
    craigslist.CraigslistHousing object with appropriate data."""

    search_filters = utils.search_filters()
    try:
        housing_object = CraigslistHousing(
            category=housing_category, filters=search_filters
        )
        return mine_data(housing_object, housing_category, geotag)
    except requests.exceptions.ConnectionError:
        return None


def mine_data(housing_obj, housing_category, geotagged):
    """Function to appropritely concatenate information sourced from
    the Craigslist housing object to a header list for downstream CSV
    export."""

    header = [
        f"Housing Category{CODE_BREAK}"
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
                f"{utils.housing_categories().get(housing_category)}{CODE_BREAK}"
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
        return None
