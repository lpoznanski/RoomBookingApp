from django.urls import path

from booking_app import views

urlpatterns = [
    path('room/new/', views.AddNewRoomView.as_view()),
    path('', views.RoomListView.as_view()),
    path('room/delete/<int:id>/', views.DeleteRoomView.as_view()),
    path('room/edit/<int:id>/', views.EditRoomView.as_view()),
    path('room/book/<int:id>/', views.BookRoomView.as_view()),
    path('room/details/<int:id>/', views.RoomDetailsView.as_view()),
    path('search/', views.RoomSearchView.as_view())
    ]