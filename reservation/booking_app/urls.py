from django.urls import path

from booking_app import views

urlpatterns = [
    path('room/new/', views.AddNewRoomView.as_view()),
    path('', views.RoomListView.as_view()),
    path('room/delete/<int:id>/', views.DeleteRoomView.as_view()),

    ]