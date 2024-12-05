from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<int:userid>/', profileView, name='profile'),
    # path('profile/', profileView, name='profile')
    path('edit-profile/<int:userid>/', editProfileView, name='editProfile'),
    path('alluser/', allUserView, name="alluser"),
    path('de-activate/<int:userid>/', deactivateUserView, name= 'deactivate')
    
]
