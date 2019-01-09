import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
			'student_feedback_project.settings')
import django
django.setup()
from student_feedback_app.models import StudentProfile, Course, LecturerProfile, Feedback, Category, Message
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
from django.db import connection


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
		{"name": "Link",
		"student_number": "1402789",
		"password": "Zelda",
		"email": "Link@sword.hy",
		"score":0,
		"courses":["MAT1Q", "POL01"]
		},
		{"name": "Harry Potter",
		"student_number": "1402001",
		"password": "Ron",
		"email": "Harry@quidditch.hw",
		"score":0,
		"courses":["MAT1Q", "ARH01"]
		},
		{"name": "Donkey Kong",
		"student_number": "1403389",
		"password": "Diddy",
		"email": "Donkey@kong.jng",
		"score":0,
		"courses":["MAT1Q"]
		},
		{"name": "Sheik",
		"student_number": "002489",
		"password": "teleport",
		"email": "Sheik@hookshot.hy",
		"score":0,
		"courses":["ARH01"]
		},
		{"name": "Navi",
		"student_number": "1402781",
		"password": "Listen!",
		"email": "Navi@listen.hy",
		"score":0,
		"courses":["ARH01", "POL01"]
		}]

	lecturers = [
		{"name": "Ganondorf",
		"lecturer_number": "00001",
		"password": "Zelda",
		"email": "Ganon@power.hy",
		"courses":["ARH01", "POL01"]
		},
		{"name": "Voldemort",
		"lecturer_number": "00002",
		"password": "Riddle",
		"email": "Voldy@death.hw",
		"courses":["MAT1Q"]
		}]

	feedback = [
		{"feedback_id": 1,
		"category": "Listening",
		"points": 4,
		"lecturer": "00001",
		"student": "1402789",
		"course_code" : "MAT1Q",
		"pre_defined_message": "Good job answering the question today!",
		"optional_message": ""},
		{"feedback_id": 2,
		"category": "Cooperation",
		"points": 3,
		"lecturer": "00002",
		"student": "1402001",
		"course_code" : "MAT1Q",
		"pre_defined_message": "Excellent team work today!",
		"optional_message": "I noticed how you helped Link complete his work."},
		{"feedback_id": 3,
		"message": "Great marks in todays quiz!",
		"category": "Participation",
		"points": 5,
		"lecturer": "00002",
		"student": "1402781",
		"course_code": "ARH01",
		"pre_defined_message": "Very good question today. I'm sure you helped a lot of students by asking it!",
		"optional_message": "If you require further clarification, feel free to drop by my office."}
		]

	categories = [
		{"name" : "Listening"},
		{"name" : "Cooperation"},
		{"name" : "Participation"}
		]

	saved_messages = [
		{"category" : "Listening",
		"text": "Good job answering the question today!"},
		{"category" : "Listening",
		"text": "I could tell that you were very attentive in class today!"},
		{"category" : "Listening",
		"text": "Thank you for noticing my error in today's class!"},
		{"category" : "Cooperation",
		"text": "Thank you for assisting your classmate in answering their question!"},
		{"category" : "Cooperation",
		"text": "Excellent team work today!"},
		{"category" : "Participation",
		"text": "Great marks in todays quiz!"},
		{"category" : "Participation",
		"text": "You made excellent points in todays discussion!"},
		{"category" : "Participation",
		"text": "Very good question today. I'm sure you helped a lot of students by asking it!"}
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
		mess = add_message(message.get('category'),message.get('text'))

	for someFeedback in feedback:
		feedback = add_feedback(someFeedback.get('feedback_id'),someFeedback.get('category'),someFeedback.get('points'),
                        someFeedback.get('lecturer'),someFeedback.get('student'),someFeedback.get('course_code'),
						someFeedback.get('pre_defined_message'), someFeedback.get('optional_message'))

	create_view_fb_cat()
	create_view_fb_stud()
	create_view_fb_class()

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
			print("\t\t" + str(fb.points) + " points for " + fb.category.name + " from " + fb.lecturer.lecturer.username)

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
		for fb in lecturer.feedback_set.all():
			print("\t\t" + str(fb.points) + " points given to " + fb.student.student.username + " for " + fb.category.name)


	print("-----------------")
	print("Feedback Added:")
	for fb in Feedback.objects.all():
		print("Feedback ID: " + str(fb.feedback_id))
		print("\tPre Defined Message: " + fb.pre_defined_message.text)
		print("\tOptional Message: " + fb.optional_message)
		print("\tCategory: " + fb.category.name)
		print("\tPoints Awarded: " + str(fb.points))
		print("\tLecturer: " + fb.lecturer.lecturer.username)
		print("\tStudent: " + fb.student.student.username)
		print("\tCourse: " + fb.which_course.subject)

	print("-----------------")
	print("Views Added:")
	print("Feedback_with_category")
	print("Feedback_with_student")
	print("Feedback_with_class")

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

# function to add the view feedback with class
def create_view_fb_class():
    with connection.cursor() as cursor:
        cursor.execute("CREATE VIEW student_feedback_app_feedback_with_class \
                        as select fb.*, cla.subject className from student_feedback_app_feedback fb \
                        INNER JOIN student_feedback_app_class cla ON fb.which_class_id = cla.class_code;")

#to add new view: make function and execute line, add model in models.py, test in DB browser SQLite

#for now you have to run populate.py after deleting the database so the views only generate once



# Helper function to add a new course
def add_course(subject,course_code, course_description):
	course = Course.objects.get_or_create(subject=subject,course_code=course_code, course_description=course_description)[0]
	course.save()
	return course


# Helper function to add a new student
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

# Helper function to add a new lecturer. Follows a similar pattern to add_student
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
		course.lecturer = lecturer_prof
		course.save()

	lecturer_prof.save()
	return lecturer_prof

# Helper function to add feedback
def add_feedback(feedback_id,category,points,lecturer,student,course_code,pre_defined_message,optional_message):
	fb = Feedback.objects.get_or_create(feedback_id=feedback_id)[0]
	fb.category = Category.objects.get(name=category)
	fb.pre_defined_message = Message.objects.get(text=pre_defined_message)
	fb.points = points
	fb.optional_message = optional_message
	fb.which_course = Course.objects.get(course_code=course_code)
	lect_user = User.objects.get(id_number=lecturer)
	fb.lecturer = LecturerProfile.objects.get(lecturer=lect_user)
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

# Helper function to add pre defined message
def add_message(category,text):
	cat = Category.objects.get(name=category)
	mess = Message.objects.get_or_create(category=cat,text=text)[0]
	mess.save()
	cat.save()
	return mess




if __name__ == '__main__':
	print('Populating Database...')
	print('--------------------\n')
	populate()
