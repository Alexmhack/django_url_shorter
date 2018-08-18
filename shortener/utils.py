import random
import string

def code_generator(size=5, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
	return ''.join(random.choice(chars) for _ in range(size))
