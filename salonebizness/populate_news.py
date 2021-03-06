#module to populate the models in the news app

import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salonebizness.settings')

import django

django.setup()

from news.models import Category, Page

def populate():
    # First, we will create lists of dictionaries containing the pages we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate through each data structure, and add the data to our models.

    python_pages = [
        {"title": "Official Python Tutorial", "url":"http://docs.python.org/2/tutorial/"},
        {"title":"How to Think like a Computer Scientist", "url":"http://www.greenteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes", "url":"http://www.korokithakis.net/tutorials/python/"} ]
    
    django_pages = [
     {"title":"Official Django Tutorial","url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
     {"title":"Django Rocks","url":"http://www.djangorocks.com/"},
     {"title":"How to Tango with Django","url":"http://www.tangowithdjango.com/"} ]

    other_pages = [
     {"title":"Bottle", "url":"http://bottlepy.org/docs/dev/"},
     {"title":"Flask", "url":"http://flask.pocoo.org"} ]

    cats = {"Python": {"pages": python_pages},
     "Django": {"pages": django_pages},
     "Other Frameworks": {"pages": other_pages} }
    #go through the cats dictionary
    for cat, cat_data in cats.iteritems():
        #add associated pages for each category
        c = add_cat(cat)
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"])

    #print out the categories we have added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "-{0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title = title)[0] #good way to create objects and check for duplication at the same time
    p.url = url
    p.views = random.randint(23,342)
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    if c.name=="Python":
        c.views = 128
        c.likes = 64
    elif c.name=="Django":
        c.views = 64
        c.likes = 32
    else:
        c.views = 32
        c.likes = 16
    c.save()
    return c

#start execution here
if __name__=="__main__":
    print "Start news population script"
    populate()












