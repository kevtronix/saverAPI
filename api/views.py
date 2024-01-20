from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Restaurant, Ticket
from .serializers import RestaurantSerializer, TicketSerializer
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
    permission_classes = [IsAuthenticated, IsSuperUser]


class UserRestaurantsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.filter(user=user)