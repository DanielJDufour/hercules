###Hercules Installation Guide
* Hercules = name of the repository
* Apodemus = name of the Django project
* Futurus = name of the Django app
* Horizon = name of the database
* Changemaker = name of the user that runs all this

###Python Packages Installed 
* Psycopg is a PostgreSQL database adapater for Python
* beautifulsoup4 is used for web scraping
* django is the framework that runs the site
* imagehash is used for image recognition and analysis
* psycopg2 connects the Django site to the database
* python-social-auth is used so people can login via Facebook, Google and other things


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

####Set Up Database
Create a changemaker user in the database
Create a database
Make changemaker owner of that database
```
sudo -u postgres psql -c "CREATE USER changemaker;";
sudo -u postgres psql -c "CREATE DATABASE horizon;"
sudo -u postgres psql -c "ALTER DATABASE horizon OWNER TO changemaker;"
```

####Change to changemaker user
It will ask for the password, which you gave after running passwd.
```
su changemaker -p;
```

####Download this repository of code
```
git clone http://github.com/danieljdufour/hercules.git ~/hercules
```

####Install Python Packages
The -r lets you install python packages to changemaker's directory and not the system directory.
```
pip install -r ~/hercules/requirements.txt
```

####Create Tables in Database
makemigrations creates the instructions for the database
migrate actually runs those instructions
```
python ~/apodemus/apodemus/manage.py makemigrations
python ~/apodemus/apodemus/manage.py migrate
```

####Run the Development Server
```
python ~/apodemus/apodemus/manage.py runserver
```

####Create Admin User
The following command will prompt you for a username and email address.
Enter ```admin``` as username and enter your email address.
And enter your password twice.
```
postgres python ~/apodemus/apodemus/manage.py createsuperuser;
