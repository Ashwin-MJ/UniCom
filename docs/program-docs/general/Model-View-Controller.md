# The MVC Pattern

## Separation of Concerns

The key benefit of this pattern, is that it allows an elegant method to separate different aspects of the code base.
The data presentation is separated from the actual logic of the application.

To do this, Django uses:

### 1. Models

This is where the database itself is created and handled. Different models can be used to represent different entities required in the project.

In this project, models include StudentProfile, LecturerProfile, Course, Feedback etc.

See [models.py](../../../student_feedback_project/student_feedback_app/models.py) to view the various models used in this project.

### 2. Templates

This corresponds to the 'View' of the MVC pattern.

It is the presentation layer which handles exactly how each page of the web application is displayed (i.e. the front end)

An example is any template such as student_home.html, which has the html presentation information about exactly what is shown on that page. It uses fields passed from a view which is explained further below.

See the directory [templates](../../../student_feedback_project/templates) to analyse the various templates used in this project.


### 3. Views

Despite the name, this plays the role of the Controller in the MVC pattern.

This is what is used to handle what information is passed to a template.

For each template, there is a corresponding view which uses a context dictionary to pass information from the database to that template.

For example, in this project, the view 'student_home' retrieves various information from the database about the signed in student (including feedback, courses etc.) and passes it to the template which displays this.

See [views.py](../../../student_feedback_project/student_feedback_app/views.py) to analyse the views associated with the html templates mentioned above.

## Summary

Despite have the basis the MVC pattern, Django is often said to use a Model Template View (MTV) pattern.
