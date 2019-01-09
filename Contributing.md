# Contributing to UniCom

The project is hosted on a GitLab server hosted by the University of Glasgow.

## General Information

To find out more about the aim of the project please see the [README.md](http://stgit.dcs.gla.ac.uk/tp3-2018-ese1/dissertation/blob/master/README.md).

This file has details about the aims of the project, as well as installation instructions and how to run tests.

## How Can I Contribute?

### Styleguides

#### General Directory Structure

This is the state of the directory structure as of 28/11/18. This is likely to change over the course of the project.

```bash
 ├── Contributing.md
 ├── LICENSE
 ├── Procfile
 ├── README.md
 └── .gitlab/
 │  └──── issue_templates/
 │       └──── ...
 │  └──── merge_request_templates/
 │       └──── ...
 └── docs/
 │  └──── dissertation/
 │       └──── ...
 └── student_feedback_project/
 │  ├──── __init__.py
 │  ├──── db.sqlite3
 │  ├──── manage.py
 │  └──── media/
 │  │     └──── profile_pictures/
 │  │          └──── ...
 │  ├──── populate.py
 │  ├──── requirements.txt
 │  └──── static/
 │  │     └──── ...
 │  └──── student_feedback_app/
 │  │     ├──── additional.py
 │  │     ├──── admin.py
 │  │     ├──── apps.py
 │  │     ├──── forms.py
 │  │     ├──── migrations/
 │  │          └──── ...
 │  │     ├──── models.py
 │  │     └──── tests/
 │  │     │    └──── ...
 │  │     ├──── urls.py
 │  │     └──── views.py
 │  └──── student_feedback_project/
 │  │    ├──── __init__.py
 │  │    ├──── settings.py
 │  │    ├──── urls.py
 │  │    └──── wsgi.py
 │  └──── templates/
         └──── ...
```
#### New issues

Upon making a new issue, consider using one of the provided templates. If there is no template relevant to the issue you are making you can use the 'General' template.

However if you feel it would be useful to create a new template for the issue you are creating simply add a new markdown file within the .gitlab/issue_templates/ folder


#### Commits

Please include detailed commit messages. Commit regularly by doing the following:

```
git add *
git commit
```

This second instruction will open up a Vim terminal. In this terminal include a brief description of the commit in the first line (as this appears as the subject of the commit).<br>
Try and limit this first line to about 72 characters.

Add further information about the commit below this subject line. Keep this brief but include the main points.

Finally <em>**always**</em> make sure to include the issue number relevant to the commit message using:

```
Issue #X
```

#### Merge Requests

Upon completion of an issue, submit a merge request on GitLab for the required branch.

Again, templates have been made, however if none of these are relevant either:
* create a new template within the .gitlab/merge_request_templates/ folder **or**
* use the General template

Complete the chosen template completely and assign the merge request to another member of the team to perform a code review.

Using the template allows the assigned team member to clearly understand all the changes you have made and why you have made them.

If accepting a merge request, ensure that there are no merge conflicts. If there are conflicts, then a good option is to meet up with team member who submitted the merge request and complete 'pair-programming' to find and resolve all conflicts.

### Team Members

A list of all the team members is attached below, as well as contact details in the event you need to contact them:

* Adam Christie -- 2237628C@student.gla.ac.uk -- 07730035555
* Alice Ravier -- 2206245R@student.gla.ac.uk -- 07519449182
* Ashwin Maliampurakal -- 2249314M@student.gla.ac.uk -- 07462200055
* Jonas Sakalys -- 2270326S@student.gla.ac.uk -- 07397957502

The team coach assigned to the team is:

* David Southgate -- 2198207S@student.gla.ac.uk
