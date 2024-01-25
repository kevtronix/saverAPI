from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Restaurant, Ticket


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RestaurantSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = Restaurant
        fields = ['id', 'user', 'name', 'address', 'concept']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        restaurant = Restaurant.objects.create(user=user, **validated_data)
        return restaurant

class TicketSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'restaurant', 'food_category', 'expiration_date', 'checked']

    def create(self, validated_data):
        # Extract the restaurant ID from the incoming data
        restaurant_id = self.context['request'].data.get('restaurant')
        # Find the restaurant instance associated with the provided ID
        restaurant = Restaurant.objects.get(id=restaurant_id)
        # Create a new Ticket instance
        ticket = Ticket.objects.create(restaurant=restaurant, **validated_data)
        return ticket