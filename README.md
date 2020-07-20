# autoCraigslistHousing

A personal project to search Craigslist and email users housing information in the SF Bay Area Peninsula.

![App logo](Documentation/craigslistApp.png)

## Purpose

My girlfriend and I are planning to move to the Peninsula from Berkeley in September 2020. Rather than constantly combing through Craigslist Housing for new posts, I decided to have some fun and write an app that emails me new housing posts that meet the location and desired specifications.

## Using the app

* Clone GitHub repository
* ```pip install -r requirements.txt```
* ```python main.py```

## For use by others

If you would like to run this application tailored to your needs, you must alter the ```peninsula``` variable in ```main.py```. Change this to meet the location you would like to search. You can find every possible Craigslist location under ```craigslist_regions.json```. Likewise, adjust the ```zip_code``` and ```search_distance``` parameters in ```search_filters.json```.

Go into ```clean_data.py``` and adjust certain parameters in various data cleaning functions to tailor bedrooms, price range, etc. to your needs. I apologize that this is hard-coded at the moment, and I may get around to making it more user friendly in the future.

Lastly, alter email recipient under ```EmailMetaData``` class in ```send_email.py```, and make sure to store your Gmail account and password information in your local environment under ```EMAIL_USER``` and ```EMAIL_PASS```, respectively. If desired, change the names of the generated CSV files to your liking, though this will not affect functionality.

## Issues

Please submit any questions or issues <a href="https://github.com/irahorecka/autoCraigslistHousing/issues">here</a>.