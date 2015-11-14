## Django Powered Bucketlist Application [![Build Status](https://travis-ci.org/andela-ooshodi/django-bucketlist-application.svg?branch=master)](https://travis-ci.org/andela-ooshodi/django-bucketlist-application) [![Coverage Status](https://coveralls.io/repos/andela-ooshodi/django-bucketlist-application/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-ooshodi/django-bucketlist-application?branch=master)

### Challenge
Design a bucketlist APP with Django and PostgreSQL and it's API with django REST framework

### Description
The bucketlist app tagged **myBucketlist** is designed to be the simple solution for organizing everything you ever wish to do in life. 

It's simple design and friendly interactions makes it the app of choice to get you on your adventure as you mark off wishes from your wish list.

## Sample Screenshots
![Index](screenshots/index.jpg)

![Login](screenshots/login.jpg)

![Bucketlist](screenshots/bucketlist.jpg)

### Getting Started
## Structure of the project
This project is divided into two apps

1. bucketlist - which house the complete standalone bucketlist app
2. apiv1 - version 1 of the api which exposes the bucketlist app

## Installation
1. Clone the repository into a Virtual Environment. 
- Run `virtualenv <virtualenvname>` or `mkvirtualenv <virtualenvname>` if using virtualenv wrapper to create the virtual environment.
2. Install all the necessary requirements by running `pip install -r requirements.txt` within the virtual environment.
3. Configure your configurations in a config.py and save in the same level as manage.py
4. Run `python manage.py makemigrations` and `python manage.py migrate` to create the necessary tables and everything required to run the application.
5. Run `python manage.py runserver` to run the app.
6. Run coverage `coverage run manage.py test`.
7. View the report of the coverage on your terminal `coverage report`.
8. Produce the html of coverage result `coverage html`.


## API Documentation
Django rest framework with swagger was used to document the API which can be viewed [here](http://127.0.0.1:8000/docs/api-docs/)


## myBucketlist
Need to see the app for yourself?
[myBucketlist](http://...)

