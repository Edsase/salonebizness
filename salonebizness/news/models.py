from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User #django's own user class

class Category(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, ) #to slugify category names and used unique to ensure unique names

    def save(self, *args, **kwargs):
        #to slugify category names (convert blank spaces to hyphens
        if not self.id:
            self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField(max_length = 200)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


#user model  to manage user.
class UserProfile(models.Model):
    #link this model to django's User model in order to take advantage of its defualt attributes line username, password, email, first name and surname
    #better to use one-to-one linking between the defualt user model and this user model that for this user model to inherit from the defualt user model
    user = models.OneToOneField(User) #will inherit all the attributes of default django User model
    #additional attributes we wish to include
    website = models.URLField(blank=True)
    # upload to specifies where the images will be loaded #make sure pillow has been installed to manage image files
    picture = models.ImageField(upload_to='profile_images', blank = True) 

    def __str__(self):
        return self.user.username
    #override the unicode method to return something meaningful
    def __unicode__(self):
        return self.user.username





