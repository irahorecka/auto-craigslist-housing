import sys
import time
import craigslist_housing
import utils


def main():
    """Main function to execute craigslist housing scraping
    for Peninsula region, processing existing and new housing
    information, and sending appropriate posts to users via
    email."""
    sys.stdout.write("\r%s" % "Gathering data...")

    posts = craigslist_housing.scrape(housing_category="apa", geotagged=False)
    filtered_posts = craigslist_housing.filter_posts(posts)
    new_posts = craigslist_housing.get_new_posts(filtered_posts)
    utils.write_email(new_posts)

    sys.stdout.write("\r%s" % "                 ")  # hacky way to clear screen
    sys.stdout.write("\r%s" % "Finished.")


if __name__ == "__main__":
    hours = lambda x: x * 3600
    while True:
        main()
        time.sleep(hours(3))  # sleep x hours
