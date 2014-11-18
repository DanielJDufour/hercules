###Archimedes Installation Guide
* Archimedes = name of the repository
* Apodemus = name of the Django project
* Futurus = name of the Django app
* Horizon = name of the database
* Changemaker = name of the user that runs all this

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

####Create Local User
Create the user named changemaker, who will actually run the Django app.
The -m at the end tells it to create a home directory for the changemaker user.
```
sudo useradd changemaker -m && sudo passwd changemaker;
```

Create changemaker user to Postgres
```
sudo -u postgres psql -c "CREATE USER changemaker;";
```

####Create Database
You will now create the database named horizon that the Django app will use.
After that, you change the owner of the database to changemaker
```
sudo -u postgres -c "CREATE DATABASE horizon; ALTER DATABASE horizon OWNER TO changemaker;"
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

####Create Database (db) Tables
The following command creates the tables needed by the INSTALLED_APPS found in ~/apodemus/apodemus/apodemus/settings.py.  ```sudo -u postgres``` makes it so you run the command as the postgres user, which has a role to access the database. 
```
sudo python ~/apodemus/apodemus/manage.py makemigrations
sudo -u postgres python ~/apodemus/apodemus/manage.py migrate

####Run the Development Server
```
sudo -u postgres python ~/apodemus/apodemus/manage.py runserver
```

####Create Admin User
The following command will prompt you for a username and email address.
Enter ```admin``` as username and enter your email address.
And enter your password twice.
```
sudo -u postgres python ~/apodemus/apodemus/manage.py createsuperuser;
