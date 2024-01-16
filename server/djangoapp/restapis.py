import json
import os
import requests

from .models import CarDealer, DealerReview


def get_request(url, **kwargs):
    """Sends a get request to the specified url with the specified json data"""
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    """Sends a post request to the specified url with the specified json data"""
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(
            url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request_with_headers(url, headers, json_data):
    """Sends a post request to the specified url with the specified json data"""
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, headers=headers, json=json_data)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    """Returns all dealers from a cloud function"""
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    """Gets reviews by dealer id from a cloud function"""
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Load Sentiment
            sentiment = analyze_review_sentiments(review["review"])
            setiment_image = "neutral.png"
            if sentiment == "positive":
                setiment_image = "positive.png"
            elif sentiment == "negative":
                setiment_image = "negative.png"
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                      review=review["review"], purchase_date=review["purchase_date"],
                                      car_make=review["car_make"], car_model=review["car_model"],
                                      car_year=review["car_year"], sentiment=sentiment, setiment_image=setiment_image,
                                      id=review["id"])
            results.append(json.loads(review_obj.toJSON()))
        return results


def get_dealers_by_state_from_cf(url, state):
    """Gets a dealers by state from a cloud function"""
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            if (dealer_obj.state == state):
                results.append(dealer_obj)
            return results


def get_dealer_by_id_from_cf(url, dealerId):
    """Gets a dealer by id from a cloud function"""
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
            if (dealer_obj.id == dealerId):
                return dealer_obj


def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/3e5029bb-dd4b-4310-ab44-fa8f244bbdcb/v1/analyze?version=2019-07-12"
    headers = {'Content-Type': 'application/json',
               'Authorization': os.getenv("IBM_IAM_KEY")}
    request = {
        "text": text,
        "features": {
            "sentiment": {}
        }
    }
    # Call post method of requests library with URL and parameters
    response = post_request_with_headers(
        url=url, headers=headers, json_data=request)
    if response:
        return response["sentiment"]["document"]["label"]
    else:
        return "unknwon"
