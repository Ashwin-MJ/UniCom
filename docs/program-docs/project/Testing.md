# Testing

This documents how to run the various test cases that have been written for this project.

## Requirements
The only additional requirement to run the tests is:

```
coverage==4.5.2
```

Note that this will have been installed if the instructions [here](Local-Setup.md) have been executed.

## Running the tests
The main tests can easily be run using the command:

```
python3 manage.py test student_feedback_app
```

All the tests should pass.

## Coverage
An additional option is to test the app using coverage (from the directory dissertation/student_feedback_app):

```
coverage run --source='.' manage.py test student_feedback_app
```

The coverage report can then be viewed using:

```
coverage report
```

## Continuous Integration
The above tests are executed using GitLab Runner on a virtual machine for every commit.

This ensures the applications functionality is not altered on each commit, and if it is the test suite will fail and the developer will be alerted.
