import string
import random
from .models import Course

def course_code_generator(size = 7, chars= string.ascii_uppercase + string.digits):
    cT = ''.join(random.choice(chars) for _ in range(size))

    for course in Course.objects.all():

        if cT == course.course_token:
            cT = course_code_generator()

    return cT
