black:
	black ./main.py ./utils/clean_data.py ./utils/send_email.py ./utils/craigslist_search.py ./utils/get_static_file.py ./utils/paths.py;\
	rm -rf ./__pycache__ ./utils/__pycache__;\
	rm ./DS_Store

flake:
	flake8 ./main.py ./utils/clean_data.py ./utils/send_email.py ./utils/craigslist_search.py ./utils/get_static_file.py ./utils/paths.py;