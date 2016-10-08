from django import forms

from models import Category, Page, UserProfile
from django.contrib.auth.models import User #django's own user class

class CategoryForm(forms.ModelForm):
    #the fields to be displayed on the form are redefined here (although not needed) inorder to add widgets and other controls to them
    name = forms.CharField(max_length=200, help_text = "Please enter the category name")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial =0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    slug = forms.CharField(widget = forms.HiddenInput(), initial=0)

    #link the form to the model using a meta class
    class Meta:
        model = Category
        #fields that should be displayed
        fields = ('name', )

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = 128, help_text = "Please enter the title of the page")
    url = forms.URLField(max_length=200 , help_text = "Please enter the url of the page")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    #link form to the model using the inline meta class
    class Meta:
        model = Page
        #fields that should be excluded
        exclude = ('category', )

    def clean(self):
        """
        used to clean the data entered into the form by the user.
        It overides the clean_data method of the modelForm class
        """
        cleaned_data = self.cleaned_data
        #get the url from the cleaned data dict
        url = cleaned_data.get('url')

        #if url is not empty and does not start with http://
        #add http to it.
        if url and not url.startswith('http://'):
            url = 'http://'+url 
            #update the cleaned data
            cleaned_data['url'] = url

class UserForm(forms.ModelForm):
    """form for the defualt django user model"""
    #although the User model already has a password field, we redefine it here in order to make use of the password input widget
    #password input widget is necessary for the password to be hidden when rendered. Otherwise, defualt password field will display the password during rendering
    password = forms.CharField(widget = forms.PasswordInput())
    #link the form to the model it should use
    class Meta:
        model = User
        #fields to be displayed by this form
        fields = ('username', 'email','password')


class UserProfileForm(forms.ModelForm):
    """form for the additional userprofile in our model"""
    #link the form to the model it should use
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')







    