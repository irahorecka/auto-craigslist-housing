black:
	black ./main.py ./craigslist_housing/clean_posts.py ./utils/send_email.py ./craigslist_housing/search_posts.py ./utils/get_static_file.py ./craigslist_housing/model_posts.py;\
	rm -rf ./__pycache__ ./utils/__pycache__ ./craigslist_housing/__pycache__;\
	rm ./DS_Store;

flake:
	flake8 ./main.py ./craigslist_housing/clean_posts.py ./utils/send_email.py ./craigslist_housing/search_posts.py ./utils/get_static_file.py ./craigslist_housing/model_posts.py;