from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    concept = models.TextField()
    
    def __str__(self):
        return self.name

class Ticket(models.Model):
    # Food Category Choices 
    FOOD_CATEGORY_CHOICES = [
        (0, 'Meats'),
        (1, 'Vegetables'),
        (2, 'Non-Perishables'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    # Type of food 
    food_category = models.IntegerField(choices=FOOD_CATEGORY_CHOICES, default=0)

    # Expiration date of the food 
    expiration_date = models.DateField(default=date.today)

    # Indicate if the food has been checked
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.restaurant.name + " " + self.get_food_category_display() + " " + self.expiration_date.strftime("%m/%d/%Y") + " " + str(self.checked)
    

    # Method to check fi the food is expired 
    def is_expired(self):
        return self.expiration_date < date.today()
    