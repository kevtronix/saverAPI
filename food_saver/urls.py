from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RestaurantViewSet, TicketViewSet, UserRestaurantsViewSet, FoodInspectorViewSet, ShelterViewSet, ShelterRequestViewSet,  VolunteerViewSet, UserShelterViewSet, OrganizerViewSet, RestaurantSignupAPIView, FoodInspectorSignupAPIView,ShelterSignupAPIView, VolunteerSignupAPIView, OrganizerSignupAPIView 
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()

router.register(r'restaurants', RestaurantViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'user-restaurants', UserRestaurantsViewSet, basename='user-restaurants')
router.register(r'inspectors', FoodInspectorViewSet)
router.register(r'shelters', ShelterViewSet)
router.register(r'user-shelters', UserShelterViewSet, basename='user-shelters')
router.register(r'shelter-requests', ShelterRequestViewSet, basename='shelter-requests')
router.register(r'volunteers', VolunteerViewSet)
router.register(r'organizers', OrganizerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token),
    path('signup/restaurant/', RestaurantSignupAPIView.as_view(), name='restaurant_signup'),
    path('signup/inspector/', FoodInspectorSignupAPIView.as_view(), name='inspector_signup'),
    path('signup/shelter/', ShelterSignupAPIView.as_view(), name='shelter_signup'),
    path('signup/volunteer/', VolunteerSignupAPIView.as_view(), name='volunteer_signup'),
    path('signup/organizer/', OrganizerSignupAPIView.as_view(), name='organizer_signup'),

]