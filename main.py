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
    utils.scrape_housing(peninsula)
    utils.filter_results()
    utils.write_email()
    sys.stdout.write("\r%s" % "                 ")  # hacky way to clear screen
    sys.stdout.write("\r%s" % "Finished.")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(3600)  # sleep 1hr
