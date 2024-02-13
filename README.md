# chatbot-base
Django chatbot web app baseline

## Installation

1. Clone the repository

2. Install the requirements
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add the following environment variables
```.env
SECRET_KEY="given_secret_key"
OPENAI_API_KEY="your_openai_api_key"
```

4. Create the database
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser
```bash
python manage.py createsuperuser
```

6. Run the server
```bash
python manage.py runserver
```

7. Create a chatbot profile
    - Go to `localhost:8000/admin`
    - Log in with the superuser credentials
    - Click Profiles -> ADD PROFILE
    - Fill the chatbot name and specify profile image (DO NOT select the User field)
    - Hit SAVE

8. Point created chatbot profile on bot configuration
    - Go to `localhost:8000/admin`
    - Log in with the superuser credentials
    - Click Bot configurations -> ADD BOT CONFIGURATION
    - Select the chatbot profile created in step 7 for Bot profile field
    - Hit SAVE

9. Enjoy



