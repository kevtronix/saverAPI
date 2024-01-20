from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RestaurantViewSet, TicketViewSet

router = DefaultRouter()

router.register(r'restaurants', RestaurantViewSet)
router.register(r'tickets', TicketViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]