import sys
import utils


def main(geotagged=False):
    """Function to initialize scraping of Craigslist housing
    data. Uses static JSON files from /static dir and
    parallel + scraping functions from /utils dir."""

    all_locations = utils.craigslist_regions()
    united_states = all_locations.get("united_states")
    peninsula = united_states[59]  # gather information for only sfbay peninsula
    peninsula.append(geotagged)

    sys.stdout.write("\r%s" % "Gathering data...")
    utils.scrape_housing(peninsula)
    utils.filter_results()
    sys.stdout.write("\r%s" % "Finished.")


if __name__ == "__main__":
    main()
