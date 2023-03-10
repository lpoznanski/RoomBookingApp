from django.shortcuts import render, redirect
from django.views import View

from datetime import datetime, date, timedelta

from booking_app.models import Room, RoomReservation


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
        return redirect('/')

class RoomListView(View):
    def get(self, request):
        rooms = Room.objects.all()
        for room in rooms:
            reservation_dates = [str(reservation.date) for reservation in room.roomreservation_set.all()]
            room.reserved = str(date.today()) in reservation_dates
        if rooms:
            return render(request, 'room_list.html', context={'rooms': rooms, 'date': date.today()})
        else:
            return render(request, 'room_list.html', context={'error': 'No rooms available'})

class DeleteRoomView(View):
    def get(self, request, id):
        Room.objects.get(id=id).delete()
        return redirect('/')

class EditRoomView(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, 'edit_room.html', context={'room': room})

    def post(self, request, id):
        room = Room.objects.get(id=id)
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector_availability = request.POST.get('projector_availability') == 'on'

        if not name:
            return render(request, 'edit_room.html', context={'room': room, 'error': 'Room name not entered'})
        if capacity <= 0:
            return render(request, 'edit_room.html', context={'room': room, 'error': 'Room capacity must be a positive number'})
        if Room.objects.filter(name=name).first() and name != room.name:
            return render(request, 'edit_room.html', context={'room': room, 'error': 'Room with the given name already exists.'})

        room.name = name
        room.capacity = capacity
        room.projector_availability = projector_availability
        room.save()

        return redirect('/')


class BookRoomView(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        reservations = RoomReservation.objects.filter(room=id)
        return render(
            request,
            'room_reservation.html',
            context = {
                'room': room,
                'reservations': reservations
            }
        )

    def post(self, request, id):
        room = Room.objects.get(id=id)
        date = request.POST.get('date')
        comment = request.POST.get('comment')

        if datetime.strptime(date, '%Y-%m-%d') < datetime.today() - timedelta(days=1):
            return render(request, 'room_reservation.html', context={'room': room, 'error': 'Unable to make reservations in the past'})
        if RoomReservation.objects.filter(room=room, date=date):
            return render(request, 'room_reservation.html', context={'room': room, 'error': 'Room already booked on this date'})

        RoomReservation.objects.create(room=room, date=date, comment=comment)

        return redirect('/')


class RoomDetailsView(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        reservations = RoomReservation.objects.filter(room=id)

        return render(
            request,
            'room_details.html',
            context={
                'room': room,
                'reservations': reservations
            }
        )

class RoomSearchView(View):
    def get(self, request):
        rooms = Room.objects.all()
        name = request.GET.get('name')
        capacity = request.GET.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector_availability = request.GET.get('projector_availability') == 'on'

        if name:
            rooms = rooms.filter(name__icontains=name)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if projector_availability:
            rooms = rooms.filter(projector_availability=projector_availability)

        for room in rooms:
            reservation_dates = [str(reservation.date) for reservation in room.roomreservation_set.all()]
            room.reserved = str(date.today()) in reservation_dates
            if room.reserved:
                rooms = rooms.exclude(id=room.id)

        if rooms:
            return render(request, 'room_list.html', context={'rooms': rooms, 'date': date.today()})
        else:
            return render(request, 'room_list.html', context={'error': 'No rooms matching your search'})