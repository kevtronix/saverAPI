from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RestaurantViewSet, TicketViewSet, UserRestaurantsViewSet, FoodInspectorViewSet, ShelterViewSet, VolunteerViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()

router.register(r'restaurants', RestaurantViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'user-restaurants', UserRestaurantsViewSet, basename='user-restaurants')
router.register(r'inspectors', FoodInspectorViewSet)
router.register(r'shelters', ShelterViewSet)
router.register(r'volunteers', VolunteerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token), 
]