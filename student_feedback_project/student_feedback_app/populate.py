import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
			'student_feedback_app.settings')

import django
django.setup()
from student_feedback_app.models import Student, Class, Lecturer, Feedback

def populate():
	print 'Populating Database...'
	print'--------------------\n'
	
	maths_students = [
		{"username": "Link",
		"student_slug": "Link",
		"password": "Zelda",
		"email": "Link@sword.hy",
		"score":0,
		},
		{"username": "Harry Potter",
		"student_slug": "Harry-Potter",
		"password": "Ron",
		"email": "Harry@quidditch.hw",
		"score":0,
		},
		{"username": "Donkey Kong",
		"student_slug": "Donkey-Kong",
		"password": "Diddy",
		"email": "Donkey@kong.jng",
		"score":0,
		}]

	arthistory_students = [
		{"username": "Harry Potter",
		"student_slug": "Harry-Potter",
		"password": "Ron",
		"email": "Harry@quidditch.hw",
		"score":0,
		},
		{"username": "Sheik",
		"student_slug": "Sheik",
		"password": "teleport",
		"email": "Sheik@hookshot.hy",
		"score":0,
		},
		{"username": "Navi",
		"student_slug": "Navi",
		"password": "Listen!",
		"email": "Navi@listen.hy",
		"score":0,
		}]

	polish_students = [
		{"username": "Link",
		"student_slug": "Link",
		"password": "Zelda",
		"email": "Link@sword.hy",
		"score":0
		},
		{"username": "Navi",
		"student_slug": "Navi",
		"password": "Listen!",
		"email": "Navi@listen.hy",
		"score":0
		}]

	lecturers = [
		{"username": "Ganondorf",
		"lecturer_slug": "Ganondorf",
		"password": "Zelda",
		"email": "Ganon@power.hy"
		},
		{"username": "Voldemort",
		"lecturer_slug": "Voldemort",
		"password": "Riddle",
		"email": "Voldy@death.hw"
		}]
		
	classes = [
		{"subject": "Maths1Q",
		"students": maths_students,
		"lecturer": lecturers[0]},
		{"subject": "ArtHistory01",
		"students": arthistort_students,
		"lecturer": lecturers[1]},
		{"subject": "Polish01",
		"students": polish_students,
		"lecturer": lecturers[0]}
		]

	feedback = [
		{"category": "listening",
		"message": "Good listening today",
		"points": 4,
		"lecturer": lecturers[0],
		"student": maths_students[0]},
		{"category": "cooperation",
		"message": "You did a good job helping Sheik in class today",
		"points": 3,
		"lecturer": lecturers[1],
		"student": arthistory_students[0]},
		{"category": "participation",
		"message": "Excellent answer to my question today",
		"points": 5,
		"lecturer": lecturers[1],
		"student": polish_students[1]}
		]
		
#get_or_create instead of get might help for unique fields

	for student in maths_students:
		Student.objects.create(username=student.get("username"),
					student_slug= student.get("student_slug"),
					password=student.get("password"),
					email=student.get("email"),
					score=student.get("score"))

	for student in arthistory_students:
		Student.objects.create(username=student.get("username"),
					student_slug= student.get("student_slug"),
					password=student.get("password"),
					email=student.get("email"),
					score=student.get("score"))

	for student in polish_students:
		Student.objects.create(username=student.get("username"),
					student_slug= student.get("student_slug"),
					password=student.get("password"),
					email=student.get("email"),
					score=student.get("score"))
			

	for lecturer in lecturers:
		Lecturer.objects.create(username=lecturer.get("username"),
					lecturer_slug= lecturer.get("lecturer_slug"),
					password=lecturer.get("password"),
					email=lecturer.get("email"))

	for class in classes:
		subject=classes.get("subject")
		Class.objects.create(subject=classes.get("subject"),
				students=classes.get("students"),
				lecturer=classes.get("lecturer"))
		c = Class.objects.filter(
		#get classes from subject
		#get students from those classes
		for student in c.objects.get(students):
			student.classes.add(c)
		#get students from c
	

	for someFeedback in feedback:
		Feedback.objects.create(category=someFeedback.get("category"),
					message=someFeedback.get("message"),
					points=someFeedback.get("points"),
					lecturer=someFeedback.get("lecturer"),
					student=someFeedback.get("student"))



#way to add classes to students and lecturers once classes are created
#add profile_picture for students and lecturers?



		
	
	

    
