# Subscription Management System with Currency Exchange Tracker

This Django-based system allows users to subscribe to various plans and track currency exchange rates. It includes user authentication, subscription management, and daily exchange rate logging using third-party APIs.

---

## Features

- User registration, login, logout
- Subscription plan management
- Currency exchange tracking
- User Subscriptions List
- Currency exchange Logs Details
- Last 7 Days Currency exchange tracking Graphical Views
- Docker support for deployment (SQLite or MySQL)
- Environment variable-based configuration

## Access Information
Super User: admin
Password: root@dmin

---

## Project Setup Guide

1. create virtual environment
        python -m venv venv
        Windows use `venv\Scripts\activate`
        linux   use `source venv/bin/activate`
        pip install -r requirements.txt

2. Move to project directory
        cd tracker

3. django migration
        python manage.py makemigrations
        python manage.py migrate
        python manage.py createsuperuser
        python manage.py runserver

4. Install Docker Desktop (Recommended for Windows)
        Download Docker Desktop
        🔗 https://www.docker.com/products/docker-desktop/
        Install it → Restart your computer.
        Open PowerShell or CMD, and run:
        docker --version
        docker compose version

5 Build and Run
        docker-compose build
        docker-compose up
        <!-- First run? Then migrate and create superuser: -->
        docker-compose exec web python app/manage.py migrate
        docker-compose exec web python app/manage.py createsuperuser

6. settings.py

        Note: Please MYSQL_DATABASE setup your pc first. then this configuration wise configure docker-compose.yml files


        ******if you run sqlite db without docker

        ##  commit out normal settings
        SECRET_KEY = 'django-insecure-2+^3)n12$l*&ur7t@4@n(ohy6rkpb%^80o)!z=6^ja^7a(f+vh'
        DEBUG = True
        ALLOWED_HOSTS = []

        ## commit in sqlite docker
        # SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-key')
        # DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
        # ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

        ## commit in MYSQL_DATABASE docker
        # SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret')
        # DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
        # ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')



        ******if you run sqlite db with docker

        ## commit out sqlite docker
        SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-key')
        DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
        ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

        ##  commit in normal settings
        # SECRET_KEY = 'django-insecure-2+^3)n12$l*&ur7t@4@n(ohy6rkpb%^80o)!z=6^ja^7a(f+vh'
        # DEBUG = True
        # ALLOWED_HOSTS = []

        ## commit in MYSQL_DATABASE docker
        # SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret')
        # DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
        # ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')


        ******if you run MYSQL_DATABASE db with docker

        ## commit out MYSQL_DATABASE docker
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret')
        DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
        ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

        ##  commit in normal settings
        # SECRET_KEY = 'django-insecure-2+^3)n12$l*&ur7t@4@n(ohy6rkpb%^80o)!z=6^ja^7a(f+vh'
        # DEBUG = True
        # ALLOWED_HOSTS = []

        ## commit in sqlite docker
        # SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-key')
        # DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
        # ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')
