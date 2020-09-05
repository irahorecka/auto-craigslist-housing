# autoCraigslistHousing

A project to search Craigslist and email users housing information in the SF Bay Area Peninsula.

<img src="Documentation/craigslist_app.png" alt="Logo" height="200">

## Purpose

My partner and I were planning to move to the Peninsula from Berkeley in August 2020. Rather than constantly combing through Craigslist Housing for new posts, I decided to have some fun and write an app that emails me new housing posts that meet the location and desired specifications. I've since refactored and made better of this code. Hopefully it will be of use to whomever uses it.

## Running the app

* Clone GitHub repository
* ```pip install -r requirements.txt```
* ```python main.py```

## Using the app

There are two windows in this application: main parameter window and subscription window.<br>

### Main window

In the main window, you will complete the Email form by completing the Email recipients along with a subject and message body, if desired. You may choose either apartments & housing or rooms & shares. The search distance criteria is set on miles from ZIP code. Select price range, area range (ft<sup>2</sup>), and number of bedrooms, if desired.<br>NOTE: bedrooms are not available for rooms and shares.<br><br>

<img src="Documentation/main_app.png" alt="Main" width="800"><br><br>

### Subscription window

Once you click "Subscribe" in the main application, a series of checks will be conducted to ensure that your input credentials are appropriate. If passed, a subscription window will pop up, asking you if you would like to receive continuous notifications (updates) on new Cragislist posts given the input parameters. If a numeric value from the drop-down menu is selected, the user will receive updates (if there are new posts) once every given hour. If "None" is selected, the user will receive the one-time notification.<br><br>

<img src="Documentation/dialog_app.png" alt="Main" width="800"><br><br>

## Important configuration notes

Make sure you have a Gmail account that is configured to send emails with Python. Watch this <a href="https://www.youtube.com/watch?v=D-NYmDWiFjU">video</a> to learn more.

To have Gmail and Password autopopulated, store your Gmail account and password information in your local environment under ```EMAIL_USER``` and ```EMAIL_PASS```, respectively. Not doing this is OK, as well - you will have to fill this portion out manually, that's all.

## Issues

Please submit any questions or issues <a href="https://github.com/irahorecka/autoCraigslistHousing/issues">here</a>.
