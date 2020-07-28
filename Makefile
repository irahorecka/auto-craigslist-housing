black:
	black ./main.py ./ui_main.py ./craigslist_housing/clean_data.py ./utils/send_email.py ./craigslist_housing/scrape_posts.py ./utils/get_static_file.py ./craigslist_housing/model_db.py ./ui/craigslistUI.py;\
	rm -rf ./__pycache__ ./utils/__pycache__ ./craigslist_housing/__pycache__ ./ui/__pycache__;\
	rm ./DS_Store;

flake:
	flake8 ./main.py ./ui_main.py ./craigslist_housing/clean_data.py ./utils/send_email.py ./craigslist_housing/scrape_posts.py ./utils/get_static_file.py ./craigslist_housing/model_db.py;

pylint:
	pylint ./main.py ./ui_main.py ./craigslist_housing/clean_data.py ./utils/send_email.py ./craigslist_housing/scrape_posts.py ./utils/get_static_file.py ./craigslist_housing/model_db.py;

app:
	pyuic5 ./ui/craigslistUI.ui -o ./ui/craigslistUI.py