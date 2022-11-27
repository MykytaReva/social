from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import my_profile_view

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
]