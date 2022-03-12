setup:
# sudo apt -y install python3.8-venv
# python3 -m venv ~/.ncaa_mvp_env
	virtualenv -p python3 env
	# source env/bin/activate

install:
	python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt
	pip install --upgrade google-cloud
	pip install --upgrade google-cloud-bigquery
	pip install --upgrade google-cloud-storage
	pip install --upgrade google-api-python-client
test:
	python3 -m pytest tests/main_test.py
	# python3 -m pytest --nbval src/*.ipynb

# lint:

# 	pylint  *.py

flask:
	cd webapp && python3 main.py

docker:
	docker build -t webapp .
		docker run -p 0.0.0.0:8080:8080/tcp webapp

etl_teams_games:
	python3 main.py

gcloud:
	echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
		sudo apt-get update && sudo apt-get install google-cloud-sdk

deploy:
	# gcloud auth login --cred-file="/home/yunuo6/Deployment/key.json" --quiet
	export PROJECT_ID=prod-dev-env
	gcloud projects add-iam-policy-binding ${PROJECT_ID} \
	--member serviceAccount:testaccount@${PROJECT_ID}.iam.gserviceaccount.com \
	--role roles/owner
	
	gcloud iam service-accounts keys create ~/key.json \
	--iam-account testaccount@${PROJECT_ID}.iam.gserviceaccount.com

	gcloud app deploy --project=prod-dev-env --version=dev 



all: install deploy 
