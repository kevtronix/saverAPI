from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from rest_framework import serializers
from .models import Restaurant, Ticket, FoodInspector, Volunteer, Shelter, ShelterRequest, Organizer


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
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        restaurant = Restaurant.objects.create(user=user, **validated_data)

        # Assign the user as the owner of the restaurant
        assign_perm('view_restaurant', user, restaurant)
        assign_perm('change_restaurant', user, restaurant)
        assign_perm('delete_restaurant', user, restaurant)

        # Assign the organizer control over the restaurant
        for organizer in Organizer.objects.all():
            assign_perm('view_restaurant', organizer.user, restaurant)
            assign_perm('change_restaurant', organizer.user, restaurant)
            assign_perm('delete_restaurant', organizer.user, restaurant)
        
        return restaurant

class TicketSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    food_category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = '__all__' 

    def create(self, validated_data):
        # Extract the restaurant ID from the incoming data
        restaurant_id = self.context['request'].data.get('restaurant')
        # Find the restaurant instance associated with the provided ID
        restaurant = Restaurant.objects.get(id=restaurant_id)
        # Create a new Ticket instance
        ticket = Ticket.objects.create(restaurant=restaurant, **validated_data)

        # Assign the user as the owner of the ticket
        assign_perm('view_ticket', ticket.restaurant.user, ticket)
        assign_perm('change_ticket', ticket.restaurant.user, ticket)
        assign_perm('delete_ticket', ticket.restaurant.user, ticket)

        # Assign the organizer control over the ticket
        for organizer in Organizer.objects.all():
            assign_perm('view_ticket', organizer.user, ticket)
            assign_perm('change_ticket', organizer.user, ticket)
            assign_perm('delete_ticket', organizer.user, ticket)
        
        # Allow the food inspector to view the ticket and mark it as checked
        
        return ticket
    
    def get_food_category_display(self, obj):
        return obj.get_food_category_display()



class FoodInspectorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = FoodInspector
        fields = '__all__' 

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        food_inspector = FoodInspector.objects.create(user=user, **validated_data)


        # Assign the user as the owner of the food inspector
        assign_perm('view_foodinspector', user, food_inspector)
        assign_perm('change_foodinspector', user, food_inspector)
        assign_perm('delete_foodinspector', user, food_inspector)


        # Assign the organizer control over the food inspector
        for organizer in Organizer.objects.all():
            assign_perm('view_foodinspector', organizer.user, food_inspector)
            assign_perm('change_foodinspector', organizer.user, food_inspector)
            assign_perm('delete_foodinspector', organizer.user, food_inspector)

        return food_inspector

class VolunteerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = Volunteer
        fields = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'email']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        volunteer = Volunteer.objects.create(user=user, **validated_data)


        # Assign the user as the owner of the volunteer
        assign_perm('view_volunteer', user, volunteer)
        assign_perm('change_volunteer', user, volunteer)
        assign_perm('delete_volunteer', user, volunteer)

        # Assign the organizer control over the volunteer
        for organizer in Organizer.objects.all():
            assign_perm('view_volunteer', organizer.user, volunteer)
            assign_perm('change_volunteer', organizer.user, volunteer)
            assign_perm('delete_volunteer', organizer.user, volunteer)
        
        return volunteer

class ShelterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Shelter
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        shelter = Shelter.objects.create(user=user, **validated_data)

        # Assign the user as the owner of the shelter
        assign_perm('view_shelter', user, shelter)
        assign_perm('change_shelter', user, shelter)
        assign_perm('delete_shelter', user, shelter)

        # Assign the organizer control over the shelter
        for organizer in Organizer.objects.all():
            assign_perm('view_shelter', organizer.user, shelter)
            assign_perm('change_shelter', organizer.user, shelter)
            assign_perm('delete_shelter', organizer.user, shelter)
        return shelter
     


class ShelterRequestSerializer(serializers.ModelSerializer):
    shelter = ShelterSerializer(read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)
    food_category_display = serializers.SerializerMethodField()

    class Meta:
        model = ShelterRequest
        fields = '__all__'
    

    def create(self, validated_data):
        # Extract the shelter ID from the incoming data
        shelter_id = self.context['request'].data.get('shelter')
        # Find the shelter instance associated with the provided ID
        shelter = Shelter.objects.get(id=shelter_id)
        # Create a new ShelterRequest instance
        shelter_request = ShelterRequest.objects.create(shelter=shelter, **validated_data)

        # Assign the user as the owner of the shelter request
        assign_perm('view_shelterrequest', shelter.user, shelter_request)
        assign_perm('change_shelterrequest', shelter.user, shelter_request)
        assign_perm('delete_shelterrequest', shelter.user, shelter_request)

        # Assign the organizer control over the shelter request
        for organizer in Organizer.objects.all():
            assign_perm('view_shelterrequest', organizer.user, shelter_request)
            assign_perm('change_shelterrequest', organizer.user, shelter_request)
            assign_perm('delete_shelterrequest', organizer.user, shelter_request)
        
        
        return shelter_request
    
    def get_food_category_display(self, obj):
        print(obj.get_food_category_display())
        return obj.get_food_category_display()


class OrganizerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Organizer
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        organizer = Organizer.objects.create(user=user, **validated_data)
        return organizer