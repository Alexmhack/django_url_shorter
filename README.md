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
