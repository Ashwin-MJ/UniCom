import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
			'student_feedback_project.settings')

import django
django.setup()
from student_feedback_app.models import Student, Class, Lecturer, Feedback

def populate():
	print ('Populating Database...')
	print ('--------------------\n')

	
	classes = [
		{"subject": "Maths1Q",
		"unique_code": "MAT1Q"},
		{"subject": "ArtHistory01",
		"unique_code": "ARH01"},
		{"subject": "Polish01",
		"unique_code": "POL01"}
		]

	students = [
		{"username": "Link",
		"student_slug": "Link",
		"student_ID": "1402789",
		"password": "Zelda",
		"email": "Link@sword.hy",
		"score":0,
		"classes":[classes[0], classes[2]]
		},
		{"username": "Harry Potter",
		"student_slug": "Harry-Potter",
		"student_ID": "1402001",
		"password": "Ron",
		"email": "Harry@quidditch.hw",
		"score":0,
		"classes":[classes[0], classes[1]]
		},
		{"username": "Donkey Kong",
		"student_slug": "Donkey-Kong",
		"student_ID": "1403389",
		"password": "Diddy",
		"email": "Donkey@kong.jng",
		"score":0,
		"classes":[classes[0]]
		},
		{"username": "Sheik",
		"student_slug": "Sheik",
		"student_ID": "002489",
		"password": "teleport",
		"email": "Sheik@hookshot.hy",
		"score":0,
		"classes":[classes[1]]
		},
		{"username": "Navi",
		"student_slug": "Navi",
		"student_ID": "1402781",
		"password": "Listen!",
		"email": "Navi@listen.hy",
		"score":0,
		"classes":[classes[1], classes[2]]
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


	feedback = [
		{"category": "listening",
		"message": "Good listening today",
		"points": 4,
		"lecturer": lecturers[0],
		"student": students[4]},
		{"category": "cooperation",
		"message": "You did a good job helping Sheik in class today",
		"points": 3,
		"lecturer": lecturers[1],
		"student": students[0]},
		{"category": "participation",
		"message": "Excellent answer to my question today",
		"points": 5,
		"lecturer": lecturers[1],
		"student": students[1]}
		]
		
#get_or_create instead of get might help for unique fields
	
	for presentClass in classes:
		Class.objects.create(subject=presentClass.get("subject"),
				lecturer=presentClass.get("lecturer"),
				unique_code=presentClass.get("unique_code")
				)	

	for student in students:		
		stud = Student.objects.create(username=student.get("username"),
					student_slug=student.get("student_slug"),
					student_ID=student.get("student_ID"),
					password=student.get("password"),
					email=student.get("email"),
					score=student.get("score"),					
					)
		writtenClasses=student.get("classes")
		for presentClass in writtenClasses:
			stud.classes.add(Class.objects.filter(unique_code=presentClass.get("unique_code")))
			
	for lecturer in lecturers:		
		lect=Lecturer.objects.create(username=lecturer.get("username"),
					lecturer_slug=lecturer.get("lecturer_slug"),
					password=lecturer.get("password"),
					email=lecturer.get("email")
					)
		classes=student.get("classes")
		for presentClass in classes:
			lect.classes.add(Class.objects.filter(unique_code=presentClass.get("unique_code")))

	for presentClass in classes:
		lect = Lecturer.objects.filter(classes__in=presentClass).distinct()
		stud = Student.objects.filter(classes__in=presentClass).distinct()
		presentClass.student.add(stud)
		presentClass.student.add(lect)
	

	for someFeedback in feedback:
		Feedback.objects.create(category=someFeedback.get("category"),
					message=someFeedback.get("message"),
					points=someFeedback.get("points"),
					lecturer=Lecturer.objects.filter(username=someFeedback.get("lecturer").get("username")),
					student=Student.objects.filter(username=someFeedback.get("student").get("username"))
					)

populate()

#add profile_picture for students and lecturers?
