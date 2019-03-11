# Local Setup

This outlines the steps that need to be taken in order to setup the UniCom application for local deployment.

## 1. Cloning the Repository
The repository can be cloned into a local machine using:

```
git clone http://stgit.dcs.gla.ac.uk/tp3-2018-ese1/dissertation.git
```

The project structure can be analysed [here](docs/program-docs/project/Structure.md)

## 2. Requirements
Requirements to use this application include Python3, pip3 and the following:

```
Django==2.1.2
coverage==4.5.2
django-registration-redux==2.5
django-widget-tweaks==1.4.3
djangorestframework==3.9.0
Pillow==5.3.0
pytz==2018.6
selenium
```

It is recommended to set up a virtual environment before installing these requirements. This can be done by following the instructions at for [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

The requirements can then be easily installed using the command:

```
cd student_feedback_project
pip3 install -r requirements.txt
```

## 3. Setting up the database
At this stage, the final step is to setup the database.

Ensuring you are again in the directory dissertation/student_feedback_project execute the following:

```
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 populate.py
```

The final instruction here makes use of a script we have written to populate the database with some initial data.

It is highly recommended that you run this, even if you do not intend on using the data.

## 4. Running the Server
To run the server simply execute:

```
python3 manage.py runserver
```

and navigate to the displayed URL in a web browser.

It is then possible to login using one of the accounts created in our population script. For example:

Lecturer (Prof. Roy) - ID Number: 00001 Password: password

Student (James Smith) - ID Number: 1402001 Password: password

See [Application Guide](docs/program-docs/general/Guide.md) for more information about how to use the application.

## Email Account
In order to allow for approval of lecturer accounts and to send tokens to students, it was necessary to create an email account of the application.

The details are below:

```
login = "lect.acc.unicom@gmail.com"
password = '1234567890poiuytrewq'
```
