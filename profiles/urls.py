from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.profile, name='profile'),
    path('update/', views.UpdateProfile.as_view(), name='update_profile'),
]