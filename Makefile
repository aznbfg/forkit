
uwsgi_run:
	uwsgi --mount /app=app.py --socket /tmp/forkit.sock --plugin python3 --callable app --pyargv="-c my_settings.yaml"

flask_run:
	python app.py -c my_settings.yaml

vm_create:
	virtualenv vm --python=3.7
	$(MAKE) vm_activate

pip_install:
	pip install -r requirements.txt
