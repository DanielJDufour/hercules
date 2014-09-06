###Apodemus Installation Guide

####Update
```
sudo apt-get update
```

####Install Required Packages
```
sudo apt-get install -y curl vim git postgresql libpq-dev postgresql-server-dev-all python python-dev python-pip
```
* curl: used to download from the internet
* vim: used to edit files in terminal
* git: used to download code from github repositories
* postgresql: the database that stores the information
* libpq-dev: needed to install psycopg2 database adapater
* postgresql-server-dev-all: includes all postgres stuff needed; includes postgresql-server-dev-X.Y, which is needed to install psycopg2 database adapater
* python: code language that django uses
* python-dev:
* python-pip: is used to install python packages

####Create Database
You will now create the databse that the Django app will use.  The database is called apodemus.
```
sudo -u postgres createdb apodemus;
```

###Install Psycopg
Psycopg is a PostgreSQL database adapater for Python
```
sudo pip install psycopg2;
```

####Download Django
The following code will download the django code into the current user's home directory. 
```
git clone http://github.com/django/django.git ~/django-trunk
```

####Make Django Code Importable
Make Django code importable into Python with the following
```
sudo pip install -e ~/django-trunk/
```

####Download This Repo
```
git clone http://github.com/danieljdufour/apodemus.git ~/apodemus
```
