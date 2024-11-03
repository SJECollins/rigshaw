from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:journey>/<int:reviewee>/', views.CreateReview.as_view(), name='create_review'),
    path('update/<int:pk>/', views.UpdateReview.as_view(), name='update_review'),
]