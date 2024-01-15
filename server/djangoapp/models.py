import json
from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50, default='CarMake')
    description = models.CharField(null=False, max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(null=False, max_length=50, default='CarModel')
    type = models.CharField(null=False, max_length=20,
                            choices=CAR_TYPES, default=SEDAN)
    year = models.DateField(null=False, default=now)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Type: " + self.type + "," + \
               "Year: " + str(self.year.year)


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name + "," + \
               "id: " + str(self.id)


class DealerReview:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Dealer name: " + self.dealership + "," + \
               "Name: " + self.name + "," + \
               "Purchase: " + self.purchase + "," + \
               "Review: " + self.review + "," + \
               "Purchase Date: " + self.purchase_date + "," + \
               "Car Make: " + self.car_make + "," + \
               "Car Model: " + self.car_model + "," + \
               "Car Year: " + self.car_year + "," + \
               "Sentiment: " + self.sentiment + "," + \
               "ID: " + self.id
