from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    my_profile_view,
    invites_received_view,\
    ProfileListView,
    # profile_list_view,
    invite_profile_list_view
)

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('all-profiles/', ProfileListView.as_view(), name='all-profiles-view'),
    path('to-invite/', invite_profile_list_view, name='invite-profiles-view'),
]