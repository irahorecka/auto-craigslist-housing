import sys
import time
import utils


def main(geotagged=False):
    """Main function to execute craigslist housing scraping
    for Peninsula region, processing existing and new housing
    information, and sending appropriate posts to users via
    email."""

    all_locations = utils.craigslist_regions()
    united_states = all_locations.get("united_states")
    peninsula = united_states[59]  # gather information for only sfbay peninsula
    peninsula.append(geotagged)

    sys.stdout.write("\r%s" % "Gathering data...")

    posts = utils.scrape_housing(peninsula, housing_category="apa")
    filtered_posts = utils.filter_posts(posts)
    new_posts = utils.get_new_posts(filtered_posts)
    utils.write_email(new_posts)

    sys.stdout.write("\r%s" % "                 ")  # hacky way to clear screen
    sys.stdout.write("\r%s" % "Finished.")


if __name__ == "__main__":
    hours = lambda x: x * 3600
    while True:
        main()
        time.sleep(hours(3))  # sleep x hours
