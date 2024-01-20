from rest_framework import serializers
from .models import Restaurant, Ticket



class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'concept']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'restaurant', 'food_category', 'expiration_date', 'checked']