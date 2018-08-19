# django_url_shorter
a django url service for shortening a url and also counting its clicks

# Objective
A url shortening service made in django. User can enter in the url and press OK, a new 
shortened url will be returned to him. Whenever the shortened url is used, we are going to 
increment our click counts.

# Django Models
At first we have just one field that is for the url, which can be a CharField but django now
supports URLField() which also has a max_length attribute of default 200.

```
url = models.URLField(max_length=220)
```

Then we expand our models to include a shortcode or the shortened url will be stored in 
here, we limit this field to a max of 15 chars.

```
shortcode = models.URLField(max_length=15)
```

*NOTE:* models.URLField is new in django2 and is a CharField for a URL, validated by 
URLValidator.

Then we have our timestamp and updated fields that keep track of the time when this model
object was created and updated, these both fields use DateTimeField which has some 
attributes for automatically handling saving of current date and time.

```
DateTimeField(auto_now=True)
# auto_now=True means this field will have the date edited and saved whenever the object is 
edited or updated

DateTimeField(auto_now_add=true)
# auto_now_add=True means that the date of creating the object will be saved here.
```

# Django shell
```
python manage.py shell
```

Running shell in django project and executing some model specific command will give you all
information about your django apps, database, fields, etc.

You can even create model objects from shell using the model API through the shell.
You just need to import your model from your app,

```
from shortener.models import KirrURL
KirrURL.objects.all()
KirrURL.objects.create(
	url='https://google.com',
	shortcode='http://go.gl')
```

The above command will actually create an KirrURL model object with the following values
But the flaw here is that you can pass in empty values and the shell won't raise any errors,
whereas if you do the same in the admin site, you will get many errors,

```
obj = KirrURL()
obj.save()
obj1 = KirrURL.objects.create()
obj1.url = 'https://udacity.com'
```

Try this and shell does not raise any errors.

```
obj3, created = KirrURL.objects.get_or_create(url='https://joincfe.com')
```

objects.get_or_create either gets the object if it exists by checking the field value or it 
creates one, you can check this by printing the values of each variable

```
print(obj3)			# https://joincfe.com
print(created)		# True
```

If the objects does not exist and it has been created now then created should be True

Or you can just use one variable and shell will print the values in a tuple

```
obj5 = KirrURL.objects.get_or_create(url='https://youtube.com')
print(obj5)

>>> ('https://youtube.com', True)		# url value and created or not boolean

obj6 = KirrURL.objects.get_or_create(url='https://youtube.com')
>>> ('https://youtube.com', False)		# False says this object existed and not created now
```

# Overiding save method
In order to create a shortcode automatically whenever we create a new url object we are 
going to overide the default save method in our KirrURL model.

Remember how we used the save method with the object in the django shell

```
...
obj.save()
```

Now for overiding it we need to define the save method in our model class ourselves like so

```
...
	def save(self, *args, **kwargs:
		super(KirrURL, self).save(*args, **kwargs)

```

The moment we define the save method in our class, it doesn't matter if we have done 
modified it or not, we have overided the save method and before us calling the super method
we can do whatever custom operation we want our save method to run before saving the model,

```
...
	def save(self, *args, **kwargs:
		print('saving our custom method...')
		super(KirrURL, self).save(*args, **kwargs)
```

Now if we try to save our object, it will print the line everytime.

# Random URL generator
Function code_generator creates a random code from all the alphabets using the random 
module in python and setting the range to 6 letters code.

```
def code_generator(size=6, chars='qwertyuioplkjhgfdsazxcvbnm'):
	return ''.join(random.choice(chars) for _ in range(size))
```

We have used python generators to create a random, this is a very basic function which is
not very powerful, but we will upgrade to a better url generator

```
import string

def code_generator(size=6, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
	return ''.join(random.choice(chars) for _ in range(size))
```

A modern approach in python for getting all the ascii letters and digits will be to use
string module.

# Custom model manager

Django allows all custom support that is we can change many default things with our models
in django, here we have put all our function in a seperate utils.py file and imported them
in our models.

KirrModelManager is a custom model manager which is through our class inheritance by the
models.Manager class

```
class KirrModelManager(models.Manager):
	def all():
		...
```

Overiding all method in here and telling our KirrURL model to use this manager instead of 
the default one will give us access to custom model manager,

```
class KirrModelManagar(models.Manager):
	def all(self, *args, **kwargs):
		queryset = super(KirrModelManagar, self).all(*args, **kwargs)
		qs = queryset.filter(active=True)
		return qs


class KirrURL(models.Model):
	...
	objects = KirrModelManagar()
	...
```

Don't forget to define our Model Manager in the model by replacing it with objects, remeber
we use 

```
model.*objects*.all()
```

What we have done here is very simple, we just call our super class to give us the all()
method that we use on model.objects.all() and we return all method with a filter, we filter
out all objects who have active field True, this means the command,

```
*django shell*
from shortener.models import KirrURL
KirrURL.objects.all().count()
KirrURL.objects.filter(active=False).count()
```

The custom model manager now has a new function that we can use directly with our objects
like so,

```
class KirrModelManagar(models.Manager):
	...
	def refresh_shortcodes(self):
			qs = KirrURL.objects.filter(id__gte=1)
			new_codes = 0
			for q in qs:
				q.shortcode = 'http://' + str(create_shortcode(q)) + '.co'
				print(q.shortcode)
				q.save()
				new_codes += 1
			return f"New codes made: {new_codes}"
```

```
KirrURL.objects.refresh_shortcodes()
```

Since we have our custom all() method with objects which does not return those objects with
active = False so we cannot use all method to access all the objects of our model so another
workaround will be to use the filter method and a attribute like 

```
queryset = KirrURL.objects.filter(id__gte=1)
```

What above command says is to filter our all objects who have their 'id' (auto generated 
field produced by django) __gte means greater than or equal to 1 which will cover all the 
objects since every id will be greater than or equal to 1.
