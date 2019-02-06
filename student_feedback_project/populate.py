import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
			'student_feedback_project.settings')
import django
django.setup()
from student_feedback_app.models import StudentProfile, Course, LecturerProfile, Feedback, Category, Message
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()


def populate():

	courses = [
		{"subject": "Maths1Q",
		"course_code": "MAT1Q",
		"course_description":"A base look at mathematical functions in the real world"},
		{"subject": "ArtHistory01",
		"course_code": "ARH01",
		"course_description":"A history of art between Middle Ages and High Renaissance periods"},
		{"subject": "Polish01",
		"course_code": "POL01",
		"course_description":"An introductory class on the polish language"},
		]

	students = [
		{"name": "Sarah Fields",
		"student_number": "1402789",
		"password": "password",
		"email": "sarah_fields@student.gla.ac.uk",
		"score":0,
		"courses":["MAT1Q", "POL01", "ARH01"]
		},
		{"name": "James Smith",
		"student_number": "1402001",
		"password": "password",
		"email": "james_smith@student.gla.ac.uk",
		"score":0,
		"courses":["MAT1Q", "ARH01"]
		},
		{"name": "Sophie Clover",
		"student_number": "1403389",
		"password": "password",
		"email": "sophie_clover@student.gla.ac.uk",
		"score":0,
		"courses":["MAT1Q"]
		},
		{"name": "Jake White",
		"student_number": "002489",
		"password": "password",
		"email": "jake_white@student.gla.ac.uk",
		"score":0,
		"courses":["ARH01"]
		},
		{"name": "Jane Mitchell",
		"student_number": "1402781",
		"password": "password",
		"email": "jane_mitchell@student.gla.ac.uk",
		"score":0,
		"courses":["ARH01", "POL01"]
		},
        {"name": "Wulfric Gwenda",
		"student_number": "14021382",
		"password": "password",
		"email": "wulfric_gwenda@student.gla.ac.uk",
		"score":40,
		"courses":["POL01"]
		},
        {"name": "Ralph Merthin",
		"student_number": "8352781",
		"password": "password",
		"email": "ralph_merthin@student.gla.ac.uk",
		"score":4,
		"courses":["MAT1Q", "POL01"]
		},
        {"name": "Thomas Langley",
		"student_number": "1439181",
		"password": "password",
		"email": "thomas_langley@student.gla.ac.uk",
		"score":16,
		"courses":["ARH01", "MAT1Q"]
		}
        ]

	lecturers = [
		{"name": "Prof. Roy",
		"lecturer_number": "00001",
		"password": "password",
		"email": "scott_roy@glasgow.ac.uk",
		"courses":["ARH01", "POL01"]
		},
		{"name": "Dr. Cossar",
		"lecturer_number": "00002",
		"password": "password",
		"email": "callum_cossar@glasgow.ac.uk",
		"courses":["MAT1Q"]
		}]

	feedback = [
		{"feedback_id": 1,
		"category": "Active Participation",
		"points": 4,
		"from_user": "00002",
		"student": "1402789",
		"course_code" : "MAT1Q",
		"pre_defined_message": "Great participation in class",
		"optional_message": ""},
		{"feedback_id": 2,
		"category": "Co-operation & Communication",
		"points": 3,
		"from_user": "00002",
		"student": "1402001",
		"course_code" : "MAT1Q",
		"pre_defined_message": "Outstanding teamwork!",
		"optional_message": "I noticed how you helped Jane complete her work."},
		{"feedback_id": 3,
		 "category": "Critical Thinking & Analysis",
		 "points": 5,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "Brilliant analytical skills!",
		 "optional_message": ""},
		{"feedback_id": 4,
		 "category": "Active Participation",
		 "points": 3,
		 "from_user": "00002",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "You were really engaged in the discussion",
		 "optional_message": ""},
		{"feedback_id": 5,
		"category": "Active Participation",
		"points": 5,
		"from_user": "00001",
		"student": "1402781",
		"course_code": "ARH01",
		"pre_defined_message": "Would love to hear your ideas more",
		"optional_message": "Feel free to drop by my office."},
		{"feedback_id": 6,
		"category": "General",
		"points": 5,
		"from_user": "1402789",
		"student": "002489",
		"course_code": "ARH01",
		"pre_defined_message": "Thank you for your help!",
		"optional_message": ""},
		{"feedback_id": 7,
		 "category": "Intellectual Curiosity",
		 "points": 5,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "You were very open to new ideas",
		 "optional_message": ""},
		{"feedback_id": 8,
		 "category": "Understanding & Competence",
		 "points": 1,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "Basic understanding of concepts",
		 "optional_message": ""},
		{"feedback_id": 9,
		 "category": "Co-operation & Communication",
		 "points": 4,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "Try to include others’ views in your discussions",
		 "optional_message": ""},
		{"feedback_id": 10,
		 "category": "Co-operation & Communication",
		 "points": 4,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "You communicate really well",
		 "optional_message": ""},
		{"feedback_id": 11,
		 "category": "Co-operation & Communication",
		 "points": 4,
		 "from_user": "1402001",
		 "student": "1402789",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "Kindly helped others",
		 "optional_message": ""},
		{"feedback_id": 12,
		 "category": "Quality of Contribution",
		 "points": 3,
		 "from_user": "1402001",
		 "student": "1402781",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "Try to dig deeper into the issue in your discussion",
		 "optional_message": ""},
		{"feedback_id": 13,
		 "category": "Quality of Contribution",
		 "points": 2,
		 "from_user": "1402001",
		 "student": "1439181",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "You made an excellent point that showed deep thinking",
		 "optional_message": ""},
		{"feedback_id": 14,
		 "category": "Quality of Contribution",
		 "points": 3,
		 "from_user": "1402001",
		 "student": "8352781",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "What a great idea!",
		 "optional_message": ""},
		{"feedback_id": 15,
		 "category": "Intellectual Curiosity",
		 "points": 5,
		 "from_user": "1402001",
		 "student": "1402781",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "You asked a really good question",
		 "optional_message": ""},
		{"feedback_id": 16,
		 "category": "Intellectual Curiosity",
		 "points": 2,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "You are not afraid to challenge and question others’ ideas",
		 "optional_message": ""},
		{"feedback_id": 17,
		 "category": "Intellectual Curiosity",
		 "points": 4,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "You really challenged the status quo",
		 "optional_message": ""},
		{"feedback_id": 18,
		 "category": "Intellectual Curiosity",
		 "points": 2,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "It’s good to think out of the box sometimes",
		 "optional_message": ""},
		{"feedback_id": 19,
		 "category": "General",
		 "points": 1,
		 "from_user": "00001",
		 "student": "1402001",
		 "course_code": "MAT1Q",
		 "pre_defined_message": "Welcome to the class!",
		 "optional_message": ""},
		]

	categories = [
		{"name": "Active Participation"},
		{"name": "Quality of Contribution"},
		{"name": "Co-operation & Communication"},
		{"name": "Critical Thinking & Analysis"},
		{"name": "Understanding & Competence"},
		{"name": "Hard Work"},
		{"name": "Intellectual Curiosity"},
		{"name": "General"}
	]

	saved_messages = [
		{"category" : "Active Participation",
		 "messages" : ["Great participation in class",
		 				"You were really engaged in the discussion",
						"You gave lots of ideas!",
						"You did lots of listening",
						"Would love to hear your ideas more"
						]
		},

		{"category" : "Quality of Contribution",
		 "messages" : ["Marvellous work in discussion!",
		 				"Great quality contribution",
						"You made an excellent point that showed deep thinking",
						"What a great idea!",
						"You were very reflective",
						"Try to dig deeper into the issue in your discussion"
						]
		},

		{"category" : "Co-operation & Communication",
		 "messages" : ["Outstanding teamwork!",
		 				"You really listened to your classmates!",
						"Kindly helped others",
						"Great leadership in discussions",
						"You communicate really well",
						"Brilliant in expressing your ideas",
						"You bring out the best in others",
						"What a great team!",
						"Make sure you listen to other people",
						"Try to include others’ views in your discussions"
						]
		},

		{"category" : "Critical Thinking & Analysis",
		 "messages" : ["You showed great critical reflections",
		 				"Excellent application of concepts to the real-world!",
						"Good awareness of different perspectives of the topic",
						"Outstanding analysis of the topic",
						"Brilliant analytical skills!",
						"Good use of evidence to inform your thinking",
						"Great synthesis of the literature",
						"Try to engage with wider perspectives on the topic"
						]
		},

		{"category" : "Understanding & Competence",
		 "messages" : ["Impressive understanding of concepts and theories",
		 				"Excellent understanding of the literature",
						"Very good grasp of key materials",
						"Basic understanding of concepts",
						"Remember to do more readings next class",
						"Make sure you understand the readings better"
						]
		},

		{"category" : "Hard Work",
		 "messages" : ["Always trying your best",
		 				"Great attitude in class",
						"Awesome improvements and glad to hear more!",
						"Lots of preparation for class",
						"You did lots of readings!",
						"Remember to complete your work next class"
						]
		},

		{"category" : "Intellectual Curiosity",
		 "messages" : ["You asked a really good question",
		 				"You are not afraid to challenge and question others’ ideas",
						"You really challenged the status quo",
						"Highly innovative way of thinking",
						"You were very open to new ideas",
						"A very reflective thinker",
						"It’s good to think out of the box sometimes"
						]
		},

		{"category" : "General",
		 "messages" : ["Welcome to the class!",
		 				"Remember to give feedback to other students and lecturers!",
						"Thank you for your feedback",
						"Thank you for your help!"
						]
		},
		]


	for presentCourse in courses:
		course = add_course(presentCourse.get('subject'),presentCourse.get('course_code'), presentCourse.get('course_description'))

	for student in students:
		stud = add_student(student.get('name'),student.get('student_number'),student.get('email'),
							student.get('password'),student.get('score'),student.get('courses'))

	for lecturer in lecturers:
		lect = add_lecturer(lecturer.get('name'),lecturer.get('lecturer_number'),
							lecturer.get('password'),lecturer.get('email'),lecturer.get('courses'))

	for category in categories:
		cat = add_category(category.get("name"))

	for message in saved_messages:
		mess = add_message(message.get('category'),message.get('messages'))

	for someFeedback in feedback:
		feedback = add_feedback(someFeedback.get('feedback_id'),someFeedback.get('category'),someFeedback.get('points'),
								someFeedback.get('from_user'),someFeedback.get('student'),someFeedback.get('course_code'),
								someFeedback.get('pre_defined_message'), someFeedback.get('optional_message'))

	create_view_fb_cat()
	create_view_fb_stud()
	create_view_fb_course()
	create_view_fb_from_user()

# function to add the view feedback with category
def create_view_fb_cat():
    with connection.cursor() as cursor:
        cursor.execute("CREATE VIEW student_feedback_app_feedback_with_category \
                        as select fb.*, ca.name categoryName from student_feedback_app_feedback fb \
                        INNER JOIN student_feedback_app_category ca ON fb.category_id = ca.id;")

# function to add the view feedback with student
def create_view_fb_stud():
    with connection.cursor() as cursor:
        cursor.execute("CREATE VIEW student_feedback_app_feedback_with_student \
                        as select fb.*, stud.username studentName from student_feedback_app_feedback fb \
                        INNER JOIN student_feedback_app_user stud ON fb.student_id = stud.id;")

# function to add the view feedback with giving user
def create_view_fb_from_user():
    with connection.cursor() as cursor:
        cursor.execute("CREATE VIEW student_feedback_app_feedback_with_from_user \
                        as select fb.*, from_user.username fromUserName from student_feedback_app_feedback fb \
                        INNER JOIN student_feedback_app_user from_user ON fb.from_user_id = from_user.id;")

# function to add the view feedback with course
def create_view_fb_course():
    with connection.cursor() as cursor:
        cursor.execute("CREATE VIEW student_feedback_app_feedback_with_course \
                        as select fb.*, course.subject courseName from student_feedback_app_feedback fb \
                        INNER JOIN student_feedback_app_course course ON fb.which_course_id = course.course_code;")

#to add new view: make function and execute line, add model in models.py, test in DB browser SQLite

#for now you have to run populate.py after deleting the database so the views only generate once


# Helper function to add a new course
def add_course(subject,course_code, course_description):
	course = Course.objects.get_or_create(subject=subject,course_code=course_code, course_description=course_description)[0]
	course.save()
	return course

# Helper function to add a new student #needs courses in db
def add_student(name,student_number,email,password,score,courses):
	# First get the User model associated with the student
	student = User.objects.get_or_create(username=name,email=email)[0]
	student.set_password(password)
	student.id_number = student_number
	student.is_student = True
	student.save()

	# Get the StudentProfile for the student
	student_prof = StudentProfile.objects.get_or_create(student=student)[0]
	student_prof.score = score

	for each_course in courses:
		# For each of the student's courses, add that course to their list of courses
		# But also add the student to the list of students for that course
		course = Course.objects.get(course_code=each_course)
		student_prof.courses.add(course)
		course.students.add(student_prof)
		course.save()

	student_prof.save()
	return student_prof

# Helper function to add a new lecturer. Follows a similar pattern to add_student #needs courses in db
def add_lecturer(name,lecturer_number,password,email,courses):
	lecturer = User.objects.get_or_create(username=name,email=email)[0]
	lecturer.set_password(password)
	lecturer.id_number = lecturer_number
	lecturer.is_lecturer = True
	lecturer.is_student = False
	lecturer.save()

	lecturer_prof = LecturerProfile.objects.get_or_create(lecturer=lecturer)[0]

	for each_course in courses:
		course = Course.objects.get(course_code=each_course)
		lecturer_prof.courses.add(course)
		course.lecturers.add (lecturer_prof)
		course.save()

	lecturer_prof.save()
	return lecturer_prof

# Helper function to add feedback #needs categories, (pre defined) messages, courses, users in db
def add_feedback(feedback_id,category,points,from_user,student,course_code,pre_defined_message,optional_message):
	fb = Feedback.objects.get_or_create(feedback_id=feedback_id)[0]
	fb.category = Category.objects.get(name=category)
	fb.pre_defined_message = Message.objects.get(text=pre_defined_message)
	fb.points = points
	fb.optional_message = optional_message
	fb.which_course = Course.objects.get(course_code=course_code)
	from_user_model = User.objects.get(id_number=from_user)
	fb.from_user = from_user_model
	# fb.lecturer = LecturerProfile.objects.get(lecturer=lect_user)
	student_user = User.objects.get(id_number=student)
	stud = StudentProfile.objects.get(student=student_user)
	fb.student = stud
	stud.score += points
	stud.save()
	fb.save()
	return fb

# Helper function to add Category
def add_category(name):
	cat = Category.objects.get_or_create(name=name)[0]
	cat.save()

# Helper function to add pre defined message #needs categories in db
def add_message(category,messages):
	cat = Category.objects.get(name=category)
	for text in messages:
		mess = Message.objects.get_or_create(category=cat,text=text)[0]
		mess.save()
		cat.save()
	return messages

def print_database():
	print("Courses Added")
	for each_course in Course.objects.all():
		print("Subject: " + each_course.subject)
		print("\tCourse Description: "+ each_course.course_description)
		print("\tSubject_Slug: " + each_course.subject_slug)
		print("\tCourse_Code: " + each_course.course_code)
		print("\tCourse_token: "+ each_course.course_token)
		print("\tLecturer: " + each_course.lecturer.lecturer.username)
		print("\tStudents: ")
		for student in each_course.students.all():
			print("\t\t" + student.student.id_number + " " + student.student.username)

	print("-----------------")
	print("Students Added:")
	for student in StudentProfile.objects.all():
		print("Student Number: " + student.student.id_number)
		print("\tStudent Email: " + student.student.email)
		print("\tStudent Name: " + student.student.username)
		print("\tStudent Slug: " + student.student.slug)
		print("\tScore: " + str(student.score))
		print("\tCourses: ")
		for each_course in student.courses.all():
			print("\t\t" + each_course.subject)
		print("\tFeedback: ")
		for fb in student.feedback_set.all():
			print("\t\t" + str(fb.points) + " points for " + fb.category.name + " from " + fb.from_user.username)

	print("-----------------")
	print("Lecturers Added:")
	for lecturer in LecturerProfile.objects.all():
		print("Lecturer Number: " + lecturer.lecturer.id_number)
		print("\tLecturer Email: " + lecturer.lecturer.email)
		print("\tLecturer Name: " + lecturer.lecturer.username)
		print("\tLecturer Slug: " + lecturer.lecturer.slug)
		print("\tCourseses: ")
		for each_course in lecturer.course_set.all():
			print("\t\t" + each_course.subject)
		print("\tFeedback Given:")
		for fb in lecturer.lecturer.feedback_set.all():
			print("\t\t" + str(fb.points) + " points given to " + fb.student.student.username + " for " + fb.category.name)


	print("-----------------")
	print("Feedback Added:")
	for fb in Feedback.objects.all():
		print("Feedback ID: " + str(fb.feedback_id))
		print("\tPre Defined Message: " + fb.pre_defined_message.text)
		print("\tOptional Message: " + fb.optional_message)
		print("\tCategory: " + fb.category.name)
		print("\tPoints Awarded: " + str(fb.points))
		print("\tFrom User: " + fb.from_user.username)
		print("\tStudent: " + fb.student.student.username)
		print("\tCourse: " + fb.which_course.subject)

	print("-----------------")
	print("Views Added:")
	print("Feedback_with_category")
	print("Feedback_with_student")
	print("Feedback_with_course")
	print("Feedback_with_from_user")


if __name__ == '__main__':
	print('Populating Database...')
	populate()
	print('...Population Complete!')
	# print_database()
