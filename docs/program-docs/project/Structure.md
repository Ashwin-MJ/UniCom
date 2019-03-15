# Project Structure

This is the state of the project structure as of 14/03/2019:

```
 ├── Contributing.md
 ├── LICENSE
 ├── Procfile
 ├── README.md
 └── .gitlab/
 │  └──── issue_templates/
 │       └──── ... [Used to create templates for making issues on GitLab]
 │  └──── merge_request_templates/
 │       └──── ... [Used to create templates for merge requests on GitLab]
 └── docs/
 │  ├──── dissertation/
 │  │    └──── ... [Includes files related to the dissertation required for this project]
 │  └──── program-docs/
 │       └──── ... [The documentation for this project]
 └── student_feedback_project/
 │  ├──── __init__.py
 │  ├──── db.sqlite3
 │  ├──── manage.py
 │  └──── media/
 │  │     └──── profile_pictures/
 │  │          └──── ... [Directory to store profile pictures]
 │  ├──── populate.py [Population script to initialise database]
 │  ├──── requirements.txt [pip3 installation requirements for the project]
 │  └──── static/
 │  │     └──── ... [Stores static data such as CSS, JS and images]
 │  └──── student_feedback_app/
 │  │     ├──── additional.py
 │  │     ├──── admin.py
 │  │     ├──── apps.py
 │  │     ├──── forms.py [The forms used in the project]
 │  │     ├──── migrations/
 │  │     │    └──── ...
 │  │     ├──── models.py [The models used in the project]
 │  │     └──── tests/
 │  │     │    └──── ... [A directory to separate the various unit tests]
 │  │     ├──── urls.py [All URLs used in addition to which view they relate to]
 │  │     └──── views.py [All the views used in the project - the main logic of the application]
 │  └──── student_feedback_project/
 │  │    ├──── __init__.py
 │  │    ├──── settings.py
 │  │    ├──── urls.py
 │  │    └──── wsgi.py
 │  └──── templates/
 │       ├──── emails
 │       │    └──── ... [This has the templates used in sending out emails]
 │       ├──── registration
 │       └──── student_feedback_app
 │            ├──── general/
 │            │    └──── ... [Templates which belong to neither lecturer or student]
 │            ├──── lecturer/
 │            │    └──── ... [Lecturer templates]
 │            └──── student/
 │                 └──── ... [Student templates]
```

Note that where possible, the team has attempted to maintain a separation of concerns (tests, templates). It is acknowledged that the main logic of the application being in a single file [views.py](student_feedback_project/student_feedback_app/views.py) is not ideal, and it is recommended that in future development, this is separated into a few files if possible.
