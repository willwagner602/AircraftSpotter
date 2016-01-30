from django.shortcuts import render
from .models import Aircraft
from .forms import AircraftForm


def aircraft_list(request):
    aircraft = Aircraft.objects.exclude(aircraft__isnull=True).values('aircraft').distinct()
    planes = Aircraft.objects.exclude(aircraft__isnull=True, redownload_flag__exact=True).values().all()
    return render(request, 'PlaneViewer/plane_test.html', {'aircraft': aircraft, 'planes': planes})


def get_aircraft(request):
    if request.method == 'POST':
        pass
    else:
        data = Aircraft.objects.filter(aircraft__isnull=False).filter(
                redownload_flag__exact=0).order_by('?').first()
        location = data.location + '\\' + data.name
        redownload = data.redownload_flag
        form = AircraftForm(initial=data.data())

    return render(request, 'PlaneViewer/get_aircraft.html', {'form': form, 'image_location': location,
                                                             "redownload": redownload})