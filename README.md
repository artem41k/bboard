# Bboard
*Django REST API project*

A practical project from a book "*Django 3.0. The practice of creating websites in Python*"

I can't agree with all book author's methods and structure of this website, but I didn't change everything.

The only things I did were change all **FBV** *(Function-based Views)* that were in the book to **CBV** *(Class-based Views)* and follow PEP8

Frontend (Angular): [bboard-front](https://github.com/artem41k/bboard-front)

There is also an interface on Django Templates, with Bootstrap

## Setup
```
pip install -r requirements.txt
python manage.py migrate
```

## Development Server
```
python manage.py runserver
```