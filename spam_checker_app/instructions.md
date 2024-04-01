venv is the virtual environment for the project(haven't included it)
manage.py file is the main file which is executed first whenever the application is started.
requirements.txt contains all the dependencies of the project.

Create the virtual environment
$ python3 -m venv venv

Activate the virtual environment
$ source venv/bin/activate

Install all packages using requirements.txt
$ pip install -r requirements.txt

To see the project working, execute these 3 commands while being in the virtual environment:
$ python manage.py makemigrations   
$ python manage.py migrate 
$ python manage.py runserver

Registration and Profile:
● A user has to register with at least name, phone number, along with a password, before using. He can optionally add an email address.
● Only one user can register on the app with a particular phone number.
● A user needs to be logged in to do anything; there is no public access to anything.

Every time a user registers and then logs-in, a unique JWTToken is generated for the session which is shown to the user with a message saying "You are logged in successfully" along with an access and refresh token. 
The user must remember/save it. 
Once logged in we have to pass this access token for each Request method(be it GET, PATCH, POST) for all the endpoints in our API.

How to pass the Token:
● We give the access_token through the Authorization section in the Postman App before sending any request for any Endpoint.
● Select Bearer Token from the dropdown menu and paste the token in Token field
● Choose request method -> enter request URL -> choose Headers from the section below the URL field
● Hit Send


 