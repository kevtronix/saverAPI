from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Restaurant, Ticket, FoodInspector, Volunteer, Shelter, ShelterRequest
from .serializers import RestaurantSerializer, TicketSerializer, FoodInspectorSerializer, VolunteerSerializer, ShelterSerializer, ShelterRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .matching import match_checked_tickets_with_requests

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


    @action(detail=False, methods=['get'])
    # Show all unchecked tickets
    def list_unchecked_tickets(self, request):
        unchecked_tickets = Ticket.objects.filter(checked=False)
        serializer = TicketSerializer(unchecked_tickets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    # Show all checked tickets 
    def list_checked_tickets(self, request):
        checked_tickets = Ticket.objects.filter(checked=True)
        serializer = TicketSerializer(checked_tickets, many=True)
        return Response(serializer.data)
    
    # Show all expired tickets 
    @action(detail=False, methods=['get'])
    def list_expired_tickets(self, request):
        expired_tickets = Ticket.objects.filter(expiration_date__lt=date.today())
        serializer = TicketSerializer(expired_tickets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    # Delete expired tickets
    def delete_expired_tickets(self, request):
        expired_tickets = Ticket.objects.filter(expiration_date__lt=date.today())
        count = expired_tickets.count()
        expired_tickets.delete()
        return Response({'status': str(count) + ' expired tickets deleted'})
    
    # Check Ticket 
    @action(detail=True, methods=['post'])
    def check_ticket(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(id=pk)
            ticket.checked = True
            ticket.save()
            return Response({'status': 'Ticket checked'})
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
    @action(detail=False, methods=['post'])
    def match_tickets(self, request):
        match_checked_tickets_with_requests()
        return Response({'status': 'Tickets matched with requests'})


class UserRestaurantsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.filter(user=user)


class UserShelterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ShelterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Shelter.objects.filter(user=user)

class FoodInspectorViewSet(viewsets.ModelViewSet):
    queryset = FoodInspector.objects.all()
    serializer_class = FoodInspectorSerializer


class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class ShelterViewSet(viewsets.ModelViewSet):
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer

class ShelterRequestViewSet(viewsets.ModelViewSet):
    queryset = ShelterRequest.objects.all()
    serializer_class = ShelterRequestSerializer

    # Show all not delivered requests
    @action(detail=False, methods=['get'])
    def list_not_delivered_requests(self, request):
        not_delivered_requests = ShelterRequest.objects.filter(delivered=False, fulfilled=True)
        serializer = ShelterRequestSerializer(not_delivered_requests, many=True)
        return Response(serializer.data)


    # Deliver request
    @action(detail=True, methods=['post'])
    def deliver_request(self, request, pk=None):
        try:
            request = ShelterRequest.objects.get(id=pk)
            request.delivered = True
            request.save()
            return Response({'status': 'Request delivered'})
        except:
            return Response({'status': 'Request not found'})