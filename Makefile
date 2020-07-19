black:
	black ./main.py ./utils/clean_data.py ./utils/send_email.py;\
	rm -rf ./__pycache__ ./utils/__pycache__;\
	rm ./DS_Store