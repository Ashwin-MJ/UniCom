import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
			'student_feedback_project.settings')
from student_feedback_app.additional import *
import django
django.setup()
from student_feedback_app.models import StudentProfile, Class, LecturerProfile, Feedback, Category
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


def populate():

	classes = [
		{"subject": "Maths1Q",
		"class_code": "MAT1Q",
		"class_description":"A base look at mathematical functions in the real world"},
		{"subject": "ArtHistory01",
		"class_code": "ARH01",
		"class_description":"A history of art between Middle Ages and High Renaissance periods"},
		{"subject": "Polish01",
		"class_code": "POL01",
		"class_description":"An introductory class on the polish language"},
		]

	students = [
		{"name": "Link",
		"student_number": "1402789",
		"password": "Zelda",
		"email": "Link@sword.hy",
		"score":0,
		"classes":["MAT1Q", "POL01"]
		},
		{"name": "Harry Potter",
		"student_number": "1402001",
		"password": "Ron",
		"email": "Harry@quidditch.hw",
		"score":0,
		"classes":["MAT1Q", "ARH01"]
		},
		{"name": "Donkey Kong",
		"student_number": "1403389",
		"password": "Diddy",
		"email": "Donkey@kong.jng",
		"score":0,
		"classes":["MAT1Q"]
		},
		{"name": "Sheik",
		"student_number": "002489",
		"password": "teleport",
		"email": "Sheik@hookshot.hy",
		"score":0,
		"classes":["ARH01"]
		},
		{"name": "Navi",
		"student_number": "1402781",
		"password": "Listen!",
		"email": "Navi@listen.hy",
		"score":0,
		"classes":["ARH01", "POL01"]
		}]

	lecturers = [
		{"name": "Ganondorf",
		"lecturer_number": "00001",
		"password": "Zelda",
		"email": "Ganon@power.hy",
		"classes":["ARH01", "POL01"]
		},
		{"name": "Voldemort",
		"lecturer_number": "00002",
		"password": "Riddle",
		"email": "Voldy@death.hw",
		"classes":["MAT1Q"]
		}]

	feedback = [
		{"feedback_id": 1,
		"message": "Good job answering the question today!",
		"category": "Listening",
		"points": 4,
		"lecturer": "00001",
		"student": "1402789",
		"class_code" : "MAT1Q"},
		{"feedback_id": 2,
		"message": "You were very active in today's lesson!",
		"category": "Cooperation",
		"points": 3,
		"lecturer": "00002",
		"student": "1402001",
		"class_code" : "MAT1Q"},
		{"feedback_id": 3,
		"message": "Great marks in todays quiz!",
		"category": "Participation",
		"points": 5,
		"lecturer": "00002",
		"student": "1402781",
		"class_code": "ARH01"}
		]


	for presentClass in classes:
		cla = add_class(presentClass.get('subject'),presentClass.get('class_code'), presentClass.get('class_description'))

	for student in students:
		stud = add_student(student.get('name'),student.get('student_number'),student.get('email'),
							student.get('password'),student.get('score'),student.get('classes'))

	for lecturer in lecturers:
		lect = add_lecturer(lecturer.get('name'),lecturer.get('lecturer_number'),
							lecturer.get('password'),lecturer.get('email'),lecturer.get('classes'))

	for someFeedback in feedback:
		feedback = add_feedback(someFeedback.get('feedback_id'),someFeedback.get('category'),someFeedback.get('points'),
								someFeedback.get('lecturer'),someFeedback.get('student'),someFeedback.get('class_code'),
								someFeedback.get('message'))


	print("Classes Added")
	for each_class in Class.objects.all():
		print("Subject: " + each_class.subject)
		print("\tClass Description: "+ each_class.class_description)
		print("\tSubject_Slug: " + each_class.subject_slug)
		print("\tClass_Code: " + each_class.class_code)
		print("\tClass_token: "+ each_class.class_token)
		print("\tLecturer: " + each_class.lecturer.lecturer.username)
		print("\tStudents: ")
		for student in each_class.students.all():
			print("\t\t" + student.student.id_number + " " + student.student.username)

	print("-----------------")
	print("Students Added:")
	for student in StudentProfile.objects.all():
		print("Student Number: " + student.student.id_number)
		print("\tStudent Email: " + student.student.email)
		print("\tStudent Name: " + student.student.username)
		print("\tStudent Slug: " + student.student.slug)
		print("\tScore: " + str(student.score))
		print("\tClasses: ")
		for each_class in student.classes.all():
			print("\t\t" + each_class.subject)
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
		print("\tClasses: ")
		for each_class in lecturer.class_set.all():
			print("\t\t" + each_class.subject)
		print("\tFeedback Given:")
		for fb in lecturer.feedback_set.all():
			print("\t\t" + str(fb.points) + " points given to " + fb.student.student.username + " for " + fb.category.name)


	print("-----------------")
	print("Feedback Added:")
	for fb in Feedback.objects.all():
		print("Feedback ID: " + str(fb.feedback_id))
		print("\tMessage: " + fb.message)
		print("\tCategory: " + fb.category.name)
		print("\tPoints Awarded: " + str(fb.points))
		print("\tLecturer: " + fb.lecturer.lecturer.username)
		print("\tStudent: " + fb.student.student.username)
		print("\tClass: " + fb.which_class.subject)

# Helper function to add a new class
def add_class(subject,class_code, class_description):
	cla = Class.objects.get_or_create(subject=subject,class_code=class_code, class_description=class_description)[0]
	cla.class_token = class_code_generator()
	cla.save()
	return cla

# Helper function to add a new student
def add_student(name,student_number,email,password,score,classes):
	# First get the User model associated with the student
	student = User.objects.get_or_create(username=name,email=email)[0]
	student.set_password(password)
	student.id_number = student_number
	student.is_student = True
	student.save()

	# Get the StudentProfile for the student
	student_prof = StudentProfile.objects.get_or_create(student=student)[0]
	student_prof.score = score

	for each_class in classes:
		# For each of the student's classes, add that class to their list of classes
		# But also add the student to the list of students for that class
		cla = Class.objects.get(class_code=each_class)
		student_prof.classes.add(cla)
		cla.students.add(student_prof)
		cla.save()

	student_prof.save()
	return student_prof

# Helper function to add a new lecturer. Follows a similar pattern to add_student
def add_lecturer(name,lecturer_number,password,email,classes):
	lecturer = User.objects.get_or_create(username=name,email=email)[0]
	lecturer.set_password(password)
	lecturer.id_number = lecturer_number
	lecturer.is_lecturer = True
	lecturer.save()

	lecturer_prof = LecturerProfile.objects.get_or_create(lecturer=lecturer)[0]

	for each_class in classes:
		cla = Class.objects.get(class_code=each_class)
		cla.lecturer = lecturer_prof
		cla.save()
		#print(lecturer_prof.lecturer_number)

	lecturer_prof.save()
	return lecturer_prof

# Helper function to add feedback
def add_feedback(feedback_id,category,points,lecturer,student,class_code,message):
	fb = Feedback.objects.get_or_create(feedback_id=feedback_id)[0]
	fb.category = Category.objects.get_or_create(name=category)[0]
	fb.points = points
	fb.message = message
	fb.which_class = Class.objects.get(class_code=class_code)
	lect_user = User.objects.get(id_number=lecturer)
	fb.lecturer = LecturerProfile.objects.get(lecturer=lect_user)
	student_user = User.objects.get(id_number=student)
	stud = StudentProfile.objects.get(student=student_user)
	fb.student = stud
	stud.score += points
	stud.save()
	fb.save()
	return fb




if __name__ == '__main__':
	print('Populating Database...')
	print('--------------------\n')
	populate()
