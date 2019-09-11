#Script to run loop every 15 minutes
#Works, uncomment print(execute()) in execute_search.py if not using this script

import execute_search as es
import time

while True:
    print(es.execute())
    time.sleep(900)