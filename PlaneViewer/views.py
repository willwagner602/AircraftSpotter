from django.shortcuts import render
from .models import Aircraft
from .forms import AircraftForm


def aircraft_list(request):
    plane = Aircraft.objects.filter(aircraft__isnull=False).order_by('?').first()
    type = plane.aircraft_type
    plane_file = 'PlaneViewer/images/' + plane.location + '/' + plane.name
    plane_author = plane.author
    return render(request, 'PlaneViewer/plane_test.html', {'location': plane_file, 'author': plane_author,
                                                           'aircraft': plane.aircraft, 'type': type})


def data_manager(request):
    if request.method == 'POST':
        plane = AircraftForm(request.POST)
        if plane.is_valid():
            # return the updated form instance of the same plane they were just looking at
            form = AircraftForm(initial=plane)
    else:
        data = Aircraft.objects.filter(aircraft__isnull=True).filter(
                redownload_flag__exact=0).order_by('?').first()
        location = 'PlaneViewer/images/' + data.location + '/' + data.name
        redownload = data.redownload_flag
        form = AircraftForm(initial=data.data())

    return render(request, 'PlaneViewer/get_aircraft.html', {'form': form, 'image_location': location})