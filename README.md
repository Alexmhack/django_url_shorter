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

# Django-admin commands
*Source*: [django-admin commands](https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/)
We don't need arguments and neither their handling, we just need to call our refresh_
shortcodes() from the handle function.

```
from shortener.models import KirrURL

	...
	def handle(self, *args, **options):
	        return KirrURL.objects.refresh_shortcodes()
```

*Run the refreshcodes command directly from root folder using manage.py file,*

```
python manage.py refreshcodes
```

**Using Arguments in Django-Admin commands**

**shortener/management/commands/refreshcodes.py**
```
	...
	def add_arguments(self, parser):
	        parser.add_argument('number', type=int)
```

**shortener/models.py**
```
	...
	def refresh_shortcodes(self, items):
		print(items)
		...
```

Model manager also has an property .order_by() which takes in the fields of the models.
This method orders the objects on the basis of the field, we can order by in decreasing order
by putting a '-' before our field name and pass in to order_by()

```
qs = KirrURL.objects.filter(id__gte=1).order_by('-id')
qs = KirrURL.objects.filter(id__gte=1).count()
```

.count() returns the number of objects returned from the query and order_by orders the
returned objects in decreasing order of id's of objects

# Views and Urls
There are two ways in which we can make our views > *function based views and class based 
views*, class based views need a model upon which they can display the page but we can
also use get method to just return what we want. After creating views, each view needs a url
for us to locate and look at the particular view, just import the view in urls.py file and
create a view using the function or class, class based views needs a .as_view() method
since they are not simple functions.

**class-based view**
```
from django.http import HttpResponse
from django.views import View

class KirrRedirectView(View):
	def get(self, request, *args, **kwargs):
		return HttpResponse("<h1>Kirr Url Shortener Again</h1>")
```

**NOTE:** Class based views need a model upon which they are based but here for starters we
are just using the get method in View class to return our response on webpage.

```
def kirr_redirect_view(request, *args, **kwargs):
	return HttpResponse('<h1>Kirr Url Shortener</h1>')
```

**NOTE:** Don't forget to return from our views or the view won't work.

# Using Setting Variable
A more robust way for getting a specified value and using it in our code is to define 
important and usable variables in our project settings.py file and then importing and using 
those variables in other files.

**kirr/settings.py**
```
...
SHORTCODE_MAX = 15
SHORTCODE_MIN = 5
...
```

Our functions in models.py has max_length attribute in shortcode field so we can specify a 
value from settings file to use in our max_length

**shortener/models.py**
```
from django.conf import settings

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class KirrURL(models.Model):
	...
	shortcode = models.URLField(max_length=SHORTCODE_MAX, unique=True, blank=True)
	...
```

Notice the getattr function, this function is very useful in these cases, if the getattr 
methods find the variable SHORTCODE_MAX in settings (which we import at top) then it will
assign SHORTCODE_MAX the value but if it doesn't then it will return 15 which is a default 
value.

**shortener/utils.py**
```
from django.conf import settings

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 5)

def create_shortcode(instance, size=SHORTCODE_MIN):
	...
```

Similarly we can import and use the variable in utils.py file

*WHAT WE DID ABOVE IS FOR THOSE CASES WHEN WE REUSE OUR APP IN SOME OTHER PROJECTS*

# Get object or 404
```
from django.shortcuts import render, get_object_or_404

def kirr_redirect_view(request, shortcode=None, *args, **kwargs):
	object = get_object_or_404(KirrURL, shortcode=shortcode)
	return HttpResponseRedirect(obj_url)
```

The simplest and two line solution for redirecting from our shortcoded url to the actual
url is using the get_object_or_404 method which will just get the object from the model
we provided and the parameter which here is the shortcode, if we get the object we return
Response Redirect to the actual url associated with the object

Then for testing purposes on our local computer we use the hosts of our WINDOWS which is 
located at *C:\WINDOWS\system32\drivers\etc* and set our localhost to any custom domain

```
127.0.0.1 			djgo.com
127.0.0.1 			www.djgo.com
```

One important thing left is to add our custom domain in allowed hosts of our project
settings...

**kirr/settings.py**
```
ALLOWED_HOSTS = ['djgo.com', '127.0.0.1', 'www.djgo.com']
```

Now accessing the url with our custom domain like *http://djgo.com:8000/func-view/asdgsd/*
This will redirect to the specified url of the object or return a 404 page

# Django-hosts
SOURCE: [django-hosts](https://django-hosts.readthedocs.io/en/latest/)

We are going to use django-hosts package for our project, just visit the link above
and follow the instructions there to install hosts and include in our project.

We need to set DEFAULT_HOST equal to the hosts pattern that we refer as the default 
pattern

SOURCE: [udemy lecture](https://www.udemy.com/try-django-1-10/learn/v4/t/lecture/5922406?start=465)

Basically what we did with django-hosts is that we made our website more advanced, you see
the websites with www.name.domain and this gets redirected to whatever the SSL the website
uses for e.g *http://* or *https://*, we did the same with the help of hosts, we made 
our website work even if the user enter in the browser > *www.djgo.com*, our website
will show the webpage, we also gave some custom urls to our website like the blog.djgo.com
which will render the same view from ROOT_URLCONFS which our *kirr/urls.py*

**On adding a host for our blog in hosts.py and the root urls as well as adding 
blog.djgo.com to our ALLOWED_HOSTS and hosts file in drivers\etc we have a new url ready
which will be blog.djgo.com:8000/shortcode/ which will show the view.**

**hostsconf/views.py** simply takes in the path from the url if exists and then redirects
it to the default url with or without path attached at end.

# Django Templates
**kirr/settings.py**

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        ...
```

When we look at this section inside our settings.py file, it has this 'DIRS' value of
an empty list, this setting is for the root templates folder for all our apps and project.

Either we can set this folder by creating a folder in our root project directory where 
manage.py file is located or we can just create templates folder inside each of our apps
where we want to render html files.

**Project directory tree** will look like this for root templates folder and we have to 
tell our settings to look for templates in here
```
+ kirr
+ shortener
+ templates
	+ shortener
		- home.html
- .gitignore
- db.sqlite3
- manage.py
- README.md
```

kirr/settings.py
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        ...
```

**If you choose to reuse the app then in that case we need to create templates for the app
inside the app folder itself and in that case we don't need to specify the templates 
folder location in settings file for our project** 

**Project directory tree** will look like this for templates inside the app itself
```
+ kirr
+ shortener
	+ templates
		+ shortener
			- home.html
+ templates
	+ shortener
		- home.html
- .gitignore
- db.sqlite3
- manage.py
- README.md
```

Now to use the templates using the render method in our views we will just use the path
in both the cases whether we want root or app templates

shortener/views.py
```
...
	return render(request, 'shortener/home.html', {})
...
```

# Django Forms
In our views we have the HomeView which has the method for handling the GET request 
through the get method, we import our form and pass it in to our context for get method

For handling POST requests we need a similar logic but we need to get the data that users
POSTED from the form, so for that the View class from django.views has a post method
just like the get method.

**shortener/views.py**
```
class HomeView(View):
	...
	def post(self, request, *args, **kwargs):
		form = ShortenURLForm(request.POST)
		context = {
			'form': form
		}

		if form.is_valid():
			print(form.cleaned_data)
		return render(request, 'shortener/home.html', context)
```

In our get method we check if the POST request with form has the valid data and not some
malicious, harmful, server-destroying data using the logic in if clause, *form.is_valid()*
, if yes we print the cleaned_data from form and return the same page with the same form and
data.

Inside our forms.py we have a more secure method that does those cleaning up and is_valid
process using the form validation for the seperate field, forms.Form has clean method 
which we call upon using *super().clean()*, and store that cleaned data in *cleaned_data*

*clean* is form validation method and cleaned_url is field validation method which checks
if the data in field is cleaned, we simply store url from *cleaned_data* from our other
method in *url* and return it.

**shortener/forms.py**
```
class ShortenURLForm(forms.Form):
	url = forms.URLField()

	def clean(self):
		cleaned_data = super().clean()
		url = cleaned_data['url']
		print(url)

	def cleaned_url(self):
		url = self.cleaned_data['url']
		print(url)
		return url
```

The above validation functions are not very safe so we use the in-built validatiors
from django.core.validators and raise error for validation from django.core.exceptions

```
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_url(value):
	url_validator = URLValidator()
	try:
		url_validator(url)
	except Exception as e:
		raise ValidationError(e)
	return value

class ShortenURLForm(forms.Form):
	url = forms.URLField(validators=[validate_url])
```

Once we create a validator we can specify this custom validator for our field by inserting
this function in the validators list of our field

**NOTE:**Since forms in django2 has URLField that has validation from URLValidators 
we don't need to write this extra code but we can have any other validator like checking i
if the url entered has a .com domain or not.

This is rather very simple logic but we create a separate file for our validators and then
import our validator in the forms file

**shortener/validators.py**
```
def validate_com_url(value):
	if 'com' not in value:
		raise ValidationError("Entered URL is not a valid .com url")
	return value
```

We use the same validator inside our model url field also using the same attribute

```
from .validators import validate_com_url

class KirrURL(models.Model):
	url = models.URLField(max_length=220, validators=[validate_com_url])
	...
```

Next time you try to save a model object with url field not having a .com in it then
it will raise errors. We actually will remove this validator since we want our shortener for 
all domain types.

In our models we are going to create a method for getting the shortened url for the object
and use the method in the template with our object, we first used the reverse method that
django.urls provied which takes in the view name from our urls and optionally any arguments,
we have shortcode argument with our shortcode-view here so we pass in the kwargs with our
shortcode.

**kirr/views.py**
```
from django.urls import reverse

class KirrURL(models.Model):
	...

	def get_short_url(self):
		shortcode = self.shortcode
		url_path = reverse('shortcode-view', kwargs={'shortcode': shortcode})
		return url_path
```

The django.urls reverse method is nice but since we are using django_hosts for our hosts
so we are going to use the reverse method from django_hosts.

```
from django_hosts import reverse

class KirrURL(models.Model):
...
	def get_short_url(self):
		shortcode = self.shortcode
		url_path = reverse(
			'shortcode-view',
			kwargs={'shortcode': shortcode},
			host='www',
			scheme='http',
			port='8000'
		)
		return url_path
```

The above method uses reverse method from django_hosts which works the same but gives more
robust way, it adds scheme, port, host for our url and rest is same as django reverse.

For using our method in template we just call our method without any brackets

**NOTE:** Any method is called in template using template tags withour the brackets unlike in 
our python code.

```
{{ obj.get_short_url }}
```

This is much more simpler than the previous one

# Click Analysis
After creating the shorten url that works we need to be able to track the clicks for each
shortened url and have it stored the count on every click, so for this we decide to create
a separate app named analytics.

```
python manage.py startapp anayltics
```

We are only going to use the models.py for this particular app since we got all our views 
ready in shortener app, we need a OneToOneField to store the KirrURL object and a interger
field for storing the count of the clicks, optionally we can use the timestamp and updated 
from the KirrURL model which automatically gets saved.

```
from shortener.models import KirrURL

class ClickAnalytic(models.Model):
	kirr_url = models.OneToOneField(KirrURL, on_delete=models.CASCADE)
	count = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.count}"
```

__str__() method gives us a way to print our object and show the count. Now We need a 
method for creating the object once our shortened url is clicked and also increment
the count (set 0 as default) by one on each click, we create a method in the model manager
of the model and name it click_analyse, which takes in a instance of the KirrURL object
and does some checking, tries to get or create ClickAnalytic object with the instance
as the kirrURL, increment count, save the object and return it.

**NOTE:** We create model manager using the class models.Manager and after creating manager
we need to define it as our custom in the model by manager to our model objects.

```
class ClickAnalyticManager(models.Manager):
	def click_analyse(self, instance):
		print(f'INSTANCE: {instance}')
		if isinstance(instance, KirrURL):
			try:
				obj, created = self.get_or_create(kirr_url=instance)
				obj.count += 1
				obj.save()
				return obj.count
			except Exception as e:
				print(e)
				
		return None


class ClickAnalytic(models.Model):
	...
	objects = ClickAnalyticManager()
```

*We are able to use get_or_create with self because we call manager and store it in objects
variable which gives it that functionality*

# Calling click_analyse
The only thing left is to call our method from shortener redirect view which is very simple

```
class KirrRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		object = get_object_or_404(KirrURL, shortcode=shortcode)
		obj_url = object.url
		ClickAnalytic.objects.click_analyse(object)
		return HttpResponseRedirect(obj_url)
```

We pass in the object(instance) to our method which does all the work, but remember *object
and count will only be created when the shortened url is clicked*

# Deploying with [heroku](https://www.heroku.com)
You can visit the site and follow their awesome docs to install and get started with heroku
deployment with django. To check heroku is installed and running run

```
> heroku

CLI to interact with Heroku

VERSION
  heroku/7.7.4 win32-x64 node-v10.6.0

USAGE
  $ heroku [COMMAND]

COMMANDS
  access          manage user access to apps
  addons          tools and services for developing, extending, and operating your
                  app
  apps            manage apps on Heroku
  auth            check 2fa status
  authorizations  OAuth authorizations
  .....
```

Running heroku in the command prompt should give you the heroku version, node version and
list of all commands

To get all the apps you have on heroku run

```
heroku apps --all
```

To get all the addons on heroku

```
heroku addons
```

We need to configure our project before deploying it on heroku, you can look at the whole
process of configuration for deploying our django app on heroku on [heroku documentation](
https://devcenter.heroku.com/categories/working-with-django)

We need requirements.txt file in which all our project dependencies will be reflected and 
there are some heroku deployment dependencies which you can look at in our 
requirements.txt file, we created everything in virtualenv so we just need to do

```
pip freeze > requirements.txt
git add requirements.txt
git commit -m "create requirements file for our project"
```

**requirements.txt**

```
Django==2.0.7
django-hosts==3.0
django-widget-tweaks==1.4.2
psycopg2==2.7.5
pytz==2018.5
dj-database-url==0.5.0
gunicorn==19.9.0
whitenoise==3.3.1
django-heroku==0.3.1
```

The file for our project should look like this, here whitenoise, gunicorn, dj-database-url,
psycopg2, django-heroku are the requirements for heroku, rest are our kirr project 
requirements.
