from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")

# Create a `register` view to return a static contact page
def register(request):
    # Handles GET request
    if request.method == "GET":
        return render(request, "djangoapp/registration.html")
    # Handles POST request
    if request.method == "POST":
        context = {}
        # Get user information from request.POST
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(
                username=username, first_name=firstname, last_name=lastname, password=password)
            if user is not None:
                # Login the user
                user = authenticate(username=username, password=password)
                if user is not None:
                    # redirect to course list page
                    return redirect("djangoapp:index")
                else:
                    # Return register page with error message
                    context = {"message": "User is not logged in"}
                    return render(request, 'djangoapp/registration.html', context)
            else:
                # Return register page with error message
                context = {"message": "User could not registered"}
                return render(request, 'djangoapp/registration.html', context)
        else:
            context = {"message": "User already exists!"}
            return render(request, 'djangoapp/registration.html', context)
    else:
        return redirect("djangoapp:index")

# Create a `login_request` view to handle sign in request
def login_request(request):
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            print("User logged in")
            login(request, user)
            return redirect('djangoapp:index')
        else:
            print("User is not valid")
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
   # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
