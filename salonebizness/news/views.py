from django.shortcuts import render

from django.http import HttpResponse

from django.contrib import humanize

#import authentication functions
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse

from datetime import datetime

from models import Category, Page, User, UserProfile
from forms import CategoryForm, PageForm, UserForm, UserProfileForm


def index(request):
    """view that will render the index.html template"""
    #create a context dictionary
    context_dict = {}
    #query the database for list of all stored categories
    #order the queryset in descending order of number of likes
    #retrieve only the top 5 categories
    category_list = Category.objects.order_by('-likes')[:5]
    #retrieve the top 5 mot viewed pages
    pages_list = Page.objects.order_by('-views')[:5]
    #obtain the number of visits of the user from the visits cookie
    #use the visitor cookie handle
    visitor_cookie_handler(request)
    visits = request.session['visits']
    #update context dictionary to pass to template engine as context
    context_dict = {'categories': category_list, 'pages':pages_list, 'visits': visits}
    #render the html index.html
    return render(request, 'news/index.html', context = context_dict)

def about(request):
    """view to render the about template"""
    #obtain the number of visits of the user from the visits cookie
    #use the visitor cookie handle
    visitor_cookie_handler(request)
    visits = request.session['visits']
    #construct context dictionary to pass to template engine as context
    context_dict = {"owner": "salonebizness community", "date": datetime.today(), 'visits': visits}
    return render(request, 'news/about.html', context=context_dict)

def show_category(request, category_name_slug):
    #create context dictionary for template rendering
    context_dict = {}
    #get the requested category based on the slug name if it exists
    
    try:
        category = Category.objects.get(slug = category_name_slug)
        #get the pages associated with this category
        pages = Page.objects.filter(category = category)
        #update the context_dict
        context_dict ['category'] =category
        context_dict ['pages'] = pages
    #abouve will raise a category does not exist exception 
    except Category.DoesNotExist:
        #update context dict with none
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'news/category.html', context=context_dict)

def add_category(request):
    """form to enable user add new categories"""
    #ensure that only registered users can add categories
    if request.user.is_authenticated():
        form = CategoryForm()

        if request.method=="POST":
            form = CategoryForm(request.POST)
            #check if form is valid
            if form.is_valid():
                #save the new category to the database
                cat = form.save(commit=True)
                #print cat on console to confirm that it has been save
                #print cat.slug
                #return to the success page, in this case the index page which shows top 5 categories
                return index(request)
            else:
                #form contains invalid data, so print errors
                print form.errors
        #render the form with error messages if any
        return render(request, 'news/add_category.html', {'form': form})
    #since user is not authenticated, redirect to login page
    else:
        return HttpResponseRedirect(reverse('news:login'))

def add_page(request, category_name_slug):
    """
    view for adding news pages
    -it displays the form
    - validates the form
    - updates the database
    -return to success or failure page
    """
    try:
        category = Category.objects.get(slug= category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method=="POST":
        form = PageForm(request.POST)
        #check if form is valid
        if form.is_valid():
            if category:
                #create a page object by saving the form           
                page = form.save(commit=False) #don't save the page object yet into the database
                page.category = category
                page.views = 0
                #no save the page object into the database
                page.save()
                #return to the succes page, in this case the index page which also shows the top 5 pages
                return show_category(request, category_name_slug)
        else:
            #form contain invalid date, so print errors
            print form.errors
    context_dict = {'category':category, 'form':form}
    #render the form with error messages if any
    return render(request, 'news/add_page.html', context_dict)

#Below function was decommisioned. We use instead the django auth app
#def register(request):
#    """
#    view to register users
#    """
#    #variable that tracks if form registration is successful
#    #initially set a boolean value to not registered
#    registered = False

#    #process the data submitted in the forms  if its a http post
#    if request.method=="POST":
#        #attempt to grab the information from the raw form inputs
#        #we use the two forms Userform and UserProfileForm
#        user_form = UserForm(data = request.POST)
#        profile_form = UserProfileForm(data = request.POST)

        ##check if the two forms are valid and process them accordingly
        #if user_form.is_valid() and profile_form.is_valid():
        #    #save the users form data to the database
        #    user = user_form.save()

        #    #hash the users password with the set password method
        #    user.set_password(user.password)
        #    #update the user object
        #    user.save()

        #    #handle the profile form
        #    #dont commit to saving until after setting the user attribute
        #    profile = profile_form.save(commit=False)
        #    #set the user attribute
        #    profile.user=user
        #    #check if user provided picture and save it if so
        #    if 'picture' in request.FILES:
        #        #set the profile picture attribute
        #        profile.picture = request.FILES['picture']

        #    #now save the user profile instance
        #    profile.save()

        #    #update form registration success variable
        #    registered = True

    #    #show errows if any of the forms is invalid
    #    else:
    #        #print errors to the terminal
    #        print profile_form.errors, user_form.errors

    ##display the forms to the user
    #else: 
    #    user_form = UserForm()
    #    profile_form = UserProfileForm()

    ##render the template depending on the context
    #return render(request, 'news/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})


#def user_login(request):
#    """code to log-in the user through a form and authenticate him"""
#    #get the relevant information from the form when the use clicks the login buttom
#    # only process this form if the request to this view is a post request
#    if request.method == "POST":
#        #gather the username and password from the form
#        username= request.POST.get('username')
#        password = request.POST.get('password')

#        #use django machinery to authenticate.
#        #the authenticate method returns a user object if authenticated
#        user = authenticate(username=username, password=password)

#        #allow login of user if authenticated
#        if user:
#            #check if the account is still active
#            if user.is_active:
#                #login in the user
#                login(request, user)
#                #redirect user to the home page
#                return HttpResponseRedirect(reverse('news:index'))
#            else:
#                #inform user that he has been disabled
#                return HttpResponse("Your news account has been disabled")
#        else: #bad login details were provided so we cant login the user
#            message= "Invalid login details: {0}, {1}".format(username, 'x'*len(password))
    #        return HttpResponse(message)
    #else: #form is been accessed via the get method so display the form
    #    return render(request, 'news/login.html', {})

##wrapper function for login_required function
#@login_required
#def restricted(request):
#    return HttpResponse("You are seeing this text because you're not logged in")


##wrapper for log-out
##ensure that only user who are already logged in can log out by using the restricted function above
#@login_required
#def user_logout(request):
#    #since we know that the user is logged in, we can log-out the user
#    logout(request)
#    #redirect the user to the homepage
#    return HttpResponseRedirect(reverse('news:index'))


#def visitor_cookie_handler(request, response):
#    """
#    this function gets the number of visitors to our site
#    uses cookies stored on the clients side
#    """
#    #use cookies.get function to obtain the cookie that tracks the number of visits
#    #if the cookie exists, the value returned is cast to an integer
#    #if the cookie does not exists, return 1
#    visits = int(request.COOKIES.get('visits', 1)) #cookie that counts the number of visits to our site...all cookies are returned as strings
#    #get the cookie that tracks the last time of visit from the request
#    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now())) 
#    #strip the last visit cookie to get out the time of visit
#    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S') 
#    #check last visit time if it is more than one day old
#    if (datetime.now()-last_visit_time).days>1:
#        #increase the visits counter cookie
#        visits = visits + 1
#        #update the last visit cookie now that we've updated the last visit counter cookie
#        #use the set cookie method of the response
#        response.set_cookie('last_visit', str(datetime.now()))
#    #if last visit cookie is less than one day
#    else:
#        #update and set the last visit cookie in the response to the last visit cookie in the request
#        last_visit_cookie = response.set_cookie('last_visit', last_visit_cookie)
#    #update and set the visits cookie in the response to the visit cookie counter
#    response.set_cookie('visits',visits)


def get_server_side_cookie(request, cookie, defualt_value = None):
    """ Helper function to get cookie value from the server side session"""
    val = request.session.get(cookie)
    if not val:
        val = defualt_value
    return val

def visitor_cookie_handler(request):
    """
    this function gets the number of visitors to our site
    uses the get server side cookies to obtain session cookies stored on the server side
    """
    #use cookies.get function to obtain the cookie that tracks the number of visits
    #if the cookie exists, the value returned is cast to an integer
    #if the cookie does not exists, return 1
    visits = int(get_server_side_cookie(request, 'visits', '1'))#cookie that counts the number of visits to our site...all cookies are returned as strings
    #get the server side cookie that tracks the last time of visit from the request
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    #strip the last visit cookie to get out the time of visit
    last_visit_time = datetime.strptime(last_visit_cookie[:], '%Y-%m-%d %H:%M:%S.%f') 
    #check last visit time if it is more than one day old--changed to seconds for testing
    if (datetime.now()-last_visit_time).seconds>1:
        #increase the visits counter cookie
        visits = visits + 1
        #update the last visit cookie now that we've updated the last visit counter cookie
        #use the request.session dictionary to update
        request.session['last_visit'] = str(datetime.now())
    else:
        #set the last visit cookie
        #use the request.session dictionary to update
        request.session['last_visit'] = last_visit_cookie
    
    #update and set the visit cookie
    request.session['visits'] = visits






















































   









































































