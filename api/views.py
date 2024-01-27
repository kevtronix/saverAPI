from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Restaurant, Ticket, FoodInspector, Volunteer
from .serializers import RestaurantSerializer, TicketSerializer, FoodInspectorSerializer, VolunteerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

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


class UserRestaurantsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.filter(user=user)

class FoodInspectorViewSet(viewsets.ModelViewSet):
    queryset = FoodInspector.objects.all()
    serializer_class = FoodInspectorSerializer


class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer