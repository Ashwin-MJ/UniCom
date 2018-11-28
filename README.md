# UniCom - The Student Feedback App

This project is being developed as part of the 3rd Year Team Project at the University of Glasgow.

## Project Details

### Why this project and who is it for?
The aim of the project is to develop an application that improves the student learning experience and create a new platform to give and receive feedback in the University of Glasgow Social and Public Policy undergraduate programme (SPP).

### What problem is it aiming to solve?
There is currently a lack of effective way for lecturers to communicate feedback to students regularly, particularly on their performance in seminars, tutorials, and small-group discussions. <br>
The client wishes to implement a new approach to give brief comments to students weekly and, in addition, offer for students to give comments to each other and to the lecturer through an app. <br>
Similar learning technology apps exist in the industry, however, appear to target to a younger audience, rather than in higher education. <br>
There is also limited flexibility for students to send customised feedback to each other or to the lecturer. This offers an opportunity to create a new app that would be suitable and flexible to the needs of lecturers and students in a university context.

## Using the Application

### Getting Started

As of now (28/11/18), the application is currently in development. The repository can be cloned locally using:

```
git clone http://stgit.dcs.gla.ac.uk/tp3-2018-ese1/dissertation.git
```

### Prerequisites

The application uses the Django Web Framework (Version 2.1.2) and Python3 (Python 3.70). All dependencies can be installed using the requirements.txt file inside the /student_feedback_project/ folder:

```
pip3 install -r requirements.txt
```

### Running the tests

The tests for this application have been broken down into separate files within the student_feedback_project/student_feedback_app/tests directory. These tests can be easily run using:

```
python3 manage.py test student_feedback_app
```

## Contributing

Please read [CONTRIBUTING.md](http://stgit.dcs.gla.ac.uk/tp3-2018-ese1/dissertation/blob/master/Contributing.md) for details about members of the team and the separation of tasks.

## License

This project is licensed under the following license [LICENSE.md](http://stgit.dcs.gla.ac.uk/tp3-2018-ese1/dissertation/blob/master/LICENSE) file for details
