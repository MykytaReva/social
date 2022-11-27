SHELL := /bin/bash

run:
	python app/manage.py runserver

shell_plus:
	python app/manage.py shell_plus --print-sql

show_urls:
	python app/manage.py show_urls

makemigrations:
	python app/manage.py makemigrations

migrate1:
	python app/manage.py migrate

celery_beat:
	cd app && celery -A settings beat --loglevel=INFO

celery_worker:
	cd app && celery -A settings worker --loglevel=INFO

migrate: makemigrations \
	migrate1

pytest:
	pytest app/tests/

coverage:
	pytest --cov=app app/tests/ --cov-report html && coverage report --fail-under=79.0000

show-coverage:  ## open coverage HTML report in default browser
	python3 -c "import webbrowser; webbrowser.open('.pytest_cache/coverage/index.html')"

gunicorn:
	cd app && gunicorn settings.wsgi:application --bind 0.0.0.0:8000 --workers 17 --threads 4 --log-level debug --max-requests 1000 --timeout 10

uwsgi_1:
	cd app && uwsgi --http-socket :8001 --module settings.wsgi --master --processes 17 --threads 4

uwsgi_2:
	cd app && uwsgi --http-socket :8002 --module settings.wsgi --master --processes 17 --threads 4 --stats 127.0.0.1:9192

good_uwsgi_1:
	cd app && uwsgi --ini uwsgi_1.ini

good_uwsgi_2:
	cd app && uwsgi --ini uwsgi_2.ini


rest_nginx:
	sudo /etc/init.d/nginx restart