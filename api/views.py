from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Restaurant, Ticket, FoodInspector, Volunteer, Shelter, ShelterRequest, Organizer
from .serializers import RestaurantSerializer, TicketSerializer, FoodInspectorSerializer, VolunteerSerializer, ShelterSerializer, ShelterRequestSerializer, OrganizerSerializer
from rest_framework import permissions
from .matching import match_checked_tickets_with_requests
from rest_framework import status
from datetime import date

from .permissions import IsRestaurant, IsShelter, IsFoodInspector, IsVolunteer, IsOrganizer 
    
class RestaurantSignupAPIView(APIView):
    # Allow any user (authenticated or not) to access this view
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurant]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsOrganizer]

    @action(detail=False, methods=['get'], permission_classes=[IsFoodInspector])
    # Show all unchecked tickets
    def list_unchecked_tickets(self, request):
        unchecked_tickets = Ticket.objects.filter(checked=False, quantity__gt=0, expiration_date__gte=date.today()).order_by('expiration_date')
        serializer = TicketSerializer(unchecked_tickets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    # Show all checked tickets 
    def list_checked_tickets(self, request):
        checked_tickets = Ticket.objects.filter(checked=True, quantity__gt=0, expiration_date__gte=date.today()).order_by('expiration_date')
        serializer = TicketSerializer(checked_tickets, many=True)
        return Response(serializer.data)
    
    # Show all expired tickets 
    @action(detail=False, methods=['get'])
    def list_expired_tickets(self, request):
        expired_tickets = Ticket.objects.filter(expiration_date__lt=date.today(), quantity__gt=0).order_by('expiration_date')
        serializer = TicketSerializer(expired_tickets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    # Delete expired tickets
    def delete_expired_tickets(self, request):
        expired_tickets = Ticket.objects.filter(expiration_date__lt=date.today(), quantity__gt=0)
        count = expired_tickets.count()
        expired_tickets.delete()
        return Response({'status': str(count) + ' expired tickets deleted'})
    
    # Check Ticket 
    @action(detail=True, methods=['post'], permission_classes=[IsFoodInspector])
    def check_ticket(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(id=pk)
            ticket.checked = True
            ticket.save()
            return Response({'status': 'Ticket checked'})
        except:
            return Response({'status': 'Ticket not found'})
    
    # Uncheck Ticket
    @action(detail=True, methods=['post'], permission_classes=[IsFoodInspector])
    def uncheck_ticket(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(id=pk)
            ticket.checked = False
            ticket.save()
            return Response({'status': 'Ticket unchecked'})
        except:
            return Response({'status': 'Ticket not found'})
    
    # Adjust quantity of food
    @action(detail=True, methods=['post'])
    def adjust_quantity(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(id=pk)
            quantity = request.data.get('quantity')
            ticket.quantity = quantity
            if quantity == 0:
                ticket.delete()
            else: 
                ticket.save()
            return Response({'status': 'Quantity adjusted'})
        except:
            return Response({'status': 'Ticket not found'})
    
    # Match Tickets with Shelter Requests
    @action(detail=False, methods=['post'], permission_classes=[IsOrganizer])
    def match_tickets(self, request):
        match_checked_tickets_with_requests()
        return Response({'status': 'Tickets matched with requests'})


class UserRestaurantsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurant]

    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.filter(user=user)



class UserShelterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ShelterSerializer
    permission_classes = [IsShelter]

    def get_queryset(self):
        user = self.request.user
        return Shelter.objects.filter(user=user)


class FoodInspectorSignupAPIView(APIView):
    # Allow any user (authenticated or not) to access this view
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = FoodInspectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodInspectorViewSet(viewsets.ModelViewSet):
    queryset = FoodInspector.objects.all()
    serializer_class = FoodInspectorSerializer
    permission_classes = [IsFoodInspector]

    # Get food inspector based on user token
    @action(detail=False, methods=['get'])
    def get_my_food_inspector(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            food_inspector = FoodInspector.objects.get(user=user)
            serializer = self.get_serializer(food_inspector)
            return Response(serializer.data)
        except FoodInspector.DoesNotExist:
            return Response({'error': 'Food inspector not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        except FoodInspector.MultipleObjectsReturned:
            return Response({'error': 'Multiple food inspectors found for this user'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class VolunteerSignupAPIView(APIView):
    # Allow any user (authenticated or not) to access this view
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [IsVolunteer]

    # Get volunteer based on user token
    @action(detail=False, methods=['get'])
    def get_my_volunteer(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            volunteer = Volunteer.objects.get(user=user)
            serializer = self.get_serializer(volunteer)
            return Response(serializer.data)
        except Volunteer.DoesNotExist:
            return Response({'error': 'Volunteer not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        except Volunteer.MultipleObjectsReturned:
            return Response({'error': 'Multiple volunteers found for this user'}, status=status.HTTP_400_BAD_REQUEST)


class ShelterSignupAPIView(APIView):
    # Allow any user (authenticated or not) to access this view
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ShelterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShelterViewSet(viewsets.ModelViewSet):
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [IsShelter]
 
    # Custom action to get shelter based on user token
    @action(detail=False, methods=['get'])
    def get_my_shelter(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            shelter = Shelter.objects.get(user=user)
            serializer = self.get_serializer(shelter)
            return Response(serializer.data)
        except Shelter.DoesNotExist:
            return Response({'error': 'Shelter not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        except Shelter.MultipleObjectsReturned:
            return Response({'error': 'Multiple shelters found for this user'}, status=status.HTTP_400_BAD_REQUEST)

class ShelterRequestViewSet(viewsets.ModelViewSet):
    queryset = ShelterRequest.objects.all()
    serializer_class = ShelterRequestSerializer
    permission_classes = [IsOrganizer]

    # Show all not fufilled requests
    @action(detail=False, methods=['get'])
    def list_not_fulfilled_requests(self, request):
        not_fulfilled_requests = ShelterRequest.objects.filter(fulfilled=False, delivered=False).order_by('quantity_requested')
        serializer = ShelterRequestSerializer(not_fulfilled_requests, many=True)
        return Response(serializer.data)

    # Show all not delivered requests
    @action(detail=False, methods=['get'], permission_classes=[IsVolunteer])
    def list_not_delivered_requests(self, request):
        not_delivered_requests = ShelterRequest.objects.filter(delivered=False, fulfilled=True).order_by('quantity_requested')
        serializer = ShelterRequestSerializer(not_delivered_requests, many=True)
        return Response(serializer.data)


    # Deliver request
    @action(detail=True, methods=['post'], permission_classes=[IsVolunteer])
    def deliver_request(self, request, pk=None):
        try:
            request = ShelterRequest.objects.get(id=pk)
            request.delivered = True
            request.save()
            return Response({'status': 'Request delivered'})
        except:
            return Response({'status': 'Request not found'})
        

class OrganizerSignupAPIView(APIView):
    # Allow any user (authenticated or not) to access this view
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OrganizerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [IsOrganizer]

    # Get organizer based on user token
    @action(detail=False, methods=['get'])
    def get_my_organizer(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            organizer = Organizer.objects.get(user=user)
            serializer = self.get_serializer(organizer)
            return Response(serializer.data)
        except Organizer.DoesNotExist:
            return Response({'error': 'Organizer not found for this user'}, status=status.HTTP_404_NOT_FOUND)
        except Organizer.MultipleObjectsReturned:
            return Response({'error': 'Multiple organizers found for this user'}, status=status.HTTP_400_BAD_REQUEST)


