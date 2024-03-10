# !/bin/bash

eval chmod +x init.sh

SECRET_KEY="given_secret_key"
OPENAI_API_KEY="your_openai_api_key"

# package install
eval pip install -r requirements.txt

# .env setting
eval cat .env
echo "SECRET_KEY=${SECRET_KEY}" >> .env
echo "OPENAI_API_KEY=${OPENAI_API_KEY}" >> .env

# Create the database
python manage.py makemigrations 
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver

