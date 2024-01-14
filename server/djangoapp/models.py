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

# <HINT> Create a plain Python class `CarDealer` to hold dealer data

# <HINT> Create a plain Python class `DealerReview` to hold review data
