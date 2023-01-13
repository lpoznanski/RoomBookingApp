from django.urls import path

from booking_app import views

urlpatterns = [
    path('room/new/', views.AddNewRoomView.as_view()),
    ]