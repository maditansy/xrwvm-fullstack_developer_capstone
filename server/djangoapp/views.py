from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


@csrf_exempt
def login_user(request):
    """
    Handle user login requests.
    """
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data.update({"status": "Authenticated"})

    return JsonResponse(response_data)


def logout_request(request):
    """
    Handle user logout requests.
    """
    logout(request)
    response_data = {"userName": ""}
    return JsonResponse(response_data)


@csrf_exempt
def registration(request):
    """
    Handle user registration requests.
    """
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False

    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        # If not, log that this is a new user
        logger.debug(f"{username} is a new user")

    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        # Login the user and return response
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(response_data)
    else:
        response_data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(response_data)


def get_dealerships(request, state="All"):
    """
    Retrieve a list of dealerships. Optionally filter by state.
    """
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """
    Retrieve reviews for a specific dealer.
    """
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)  # For debugging purposes

            if response and 'sentiment' in response:
                review_detail['sentiment'] = response['sentiment']
            else:
                review_detail['sentiment'] = 'Unavailable'  # Default value if sentiment analysis fails

        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    """
    Retrieve details for a specific dealer.
    """
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    """
    Add a review for a dealer.
    """
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as err:
            logger.error(f"Error in posting review: {err}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


def get_cars(request):
    """
    Retrieve a list of car models. Initialize data if none exist.
    """
    car_count = CarMake.objects.count()
    print(car_count)

    if car_count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]

    return JsonResponse({"CarModels": cars})
