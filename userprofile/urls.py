from django.urls import path
from userprofile.views import UserCreationView, UserProfileView


urlpatterns = [
    path('userregister/', UserCreationView.as_view(), name='userregister'),
    path('userprofile/', UserProfileView.as_view(), name='userprofile'),
]