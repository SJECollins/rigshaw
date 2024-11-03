from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_journey, name='journey_create'),
    path('journey/<int:pk>/', views.journey_detail, name='journey_detail'),
    path('user-journeys/', views.my_journeys, name='user_journeys'),
    path('journey/<int:pk>/update/', views.update_journey, name='update_journey'),
    path('journey/<int:pk>/cancel/', views.cancel_journey, name='cancel_journey'),
    path('request/<int:pk>/', views.create_request, name='create_request'),
    path('request/<int:pk>/update/', views.update_request, name='update_request'),
    path('request/<int:pk>/withdraw/', views.withdraw_request, name='withdraw_request'),
    path('request/<int:pk>/accept/', views.accept_request, name='accept_request'),
    path('request/<int:pk>/reject/', views.reject_request, name='reject_request'),
    path('meeting/<int:pk>/', views.create_meeting, name='create_meeting'),
    path('meeting/<int:pk>/update/', views.update_meeting, name='update_meeting'),
    path('meeting/<int:pk>/accept/', views.accept_meeting, name='accept_meeting'),
    path('meeting/<int:pk>/reject/', views.reject_meeting, name='reject_meeting'),
]