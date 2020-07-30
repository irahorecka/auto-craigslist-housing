import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def search_filters():
    """Get and load search filters JSON."""
    search_filters_path = os.path.join(BASE_DIR, "static", "search_filters.json")
    with open(search_filters_path) as json_path:
        return json.load(json_path)["search_filters"]


def housing_categories():
    """Get and load housing categories JSON."""
    housing_categories_path = os.path.join(
        BASE_DIR, "static", "housing_categories.json"
    )
    with open(housing_categories_path) as json_path:
        return json.load(json_path)["housing_categories"]


def qcombo_box():
    """Get and load QComboBox categories JSON."""
    housing_categories_path = os.path.join(BASE_DIR, "static", "qcombo_box.json")
    with open(housing_categories_path) as json_path:
        return json.load(json_path)["qcombo_box"]


def set_miles_and_zipcode(craigslist_param):
    """Set miles and zipcode from craigslist_param ported from main.py"""
    search_filters_path = os.path.join(BASE_DIR, "static", "search_filters.json")
    with open(search_filters_path) as json_path:
        search_filters_dict = json.load(json_path)
        search_filters_dict["search_filters"]["zip_code"] = str(
            craigslist_param.get("zipcode")
        )
        search_filters_dict["search_filters"]["search_distance"] = str(
            craigslist_param.get("miles")
        )
    with open(search_filters_path, "w") as json_path:
        json.dump(search_filters_dict, json_path, indent=4, sort_keys=True)
