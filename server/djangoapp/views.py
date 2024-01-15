import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from djangoapp.restapis import analyze_review_sentiments, get_dealer_reviews_from_cf, get_dealers_from_cf, post_request
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    return render(request, "djangoapp/about.html")


def contact(request):
    return render(request, "djangoapp/contact.html")


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


def login_request(request):
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        # If user is valid, call login method to login current user
        if user is not None:
            # Login the user
            login(request, user)
            # Redirect the user to the index page
            return redirect('djangoapp:index')
        # The user was not valid
        else:
            # Redirect the user to the index page
            return redirect('djangoapp:index')
    # The request is not a POST request
    else:
        # Redirect the user to the index page
        return redirect('djangoapp:index')


def logout_request(request):
   # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/eb0a5bcd-0bd6-4a41-aec7-4a5442418a7f/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    else:
        return HttpResponse("Request method is not a GET")


def get_dealer_details(request, dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/eb0a5bcd-0bd6-4a41-aec7-4a5442418a7f/dealership-package/get-review.json"
    # Get dealer details from the Cloud Function
    reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
    return HttpResponse(json.dumps(reviews))


def add_review(request, dealer_id):
    # See if user is authenticated
    if(request.user):
        if request.method == "POST":
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/eb0a5bcd-0bd6-4a41-aec7-4a5442418a7f/dealership-package/create-review"
            json_data = {}
            json_data["name"] = request.user.first_name + " " + request.user.last_name
            json_data["dealership"] = dealer_id
            json_data["review"] = request.POST["review"]        
            json_data["purchase"] = ""
            json_data["purchase_date"] = ""
            json_data["car_make"] = ""
            json_data["car_model"] = ""
            json_data["car_year"] = ""
            response = post_request(url, json_data)
            return HttpResponse(json.dumps(response))
    else:
        return HttpResponse("You need to login first")
