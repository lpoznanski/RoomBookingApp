from django.shortcuts import render, redirect
from django.views import View

from booking_app.models import Room


# Create your views here.
class AddNewRoomView(View):
    def get(self, request):
        return render(
            request,
            'add_new_room.html',
        )

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector_availability = request.POST.get('projector_availability') == "on"

        if not name:
            return render(request, 'add_new_room.html', context={'error': 'Room name not entered'})
        if capacity <= 0:
            return render(request, 'add_new_room.html', context={'error': 'Room capacity must be a positive number'})
        if Room.objects.filter(name=name).first():
            return render(request, 'add_new_room.html', context={'error': 'Room with the given name already exists.'})

        Room.objects.create(name=name, capacity=capacity, projector_availability=projector_availability)
        return redirect('')

