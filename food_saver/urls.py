from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.views import RestaurantViewSet, TicketViewSet

router = SimpleRouter()

router.register(r'restaurants', RestaurantViewSet)
router.register(r'tickets', TicketViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]