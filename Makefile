black:
	black ./main.py ./craigslist_housing/clean_data.py ./utils/send_email.py ./craigslist_housing/craigslist_search.py ./utils/get_static_file.py ./craigslist_housing/db_models.py;\
	rm -rf ./__pycache__ ./utils/__pycache__ ./craigslist_housing/__pycache__;\
	rm ./DS_Store

flake:
	flake8 ./main.py ./craigslist_housing/clean_data.py ./utils/send_email.py ./craigslist_housing/craigslist_search.py ./utils/get_static_file.py ./craigslist_housing/db_models.py;