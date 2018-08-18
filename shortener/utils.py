import random
import string

def code_generator(size=5, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
	return ''.join(random.choice(chars) for _ in range(size))


def create_shortcode(instance, size=5):
	new_code = code_generator(size=size)
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(shortcode=new_code).exists()
	
	if qs_exists:
		return code_generator(size=size)
	return new_code