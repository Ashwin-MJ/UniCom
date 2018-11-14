import string
import random


def course_code_generator(size = 7, chars= string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
