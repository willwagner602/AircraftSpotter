from django.shortcuts import render, HttpResponseRedirect
from .models import Aircraft, AircraftType
from .forms import AircraftForm
from random import shuffle


def aircraft_display(request):
    # get the individual plane for display, and the necessary data to display it
    plane = Aircraft.objects.filter(aircraft__isnull=False)
    plane = plane.filter(redownload_flag__exact=0).order_by('?').first()
    plane_file = 'PlaneViewer/images/' + plane.location + '/' + plane.name

    # get information necessary to identify similar planes for challenging multiple choice options
    plane_model = plane.aircraft
    type_int = AircraftType.objects.filter(aircraft_name=plane_model).first().type_int

    # get selection for multiple choice options - must include the correct aircraft
    selection_options = AircraftType.objects.filter(type_int__exact=type_int).order_by('?').all()
    selection_options = selection_options.exclude(aircraft_name__in=plane_model)[:5]
    selection_options = [str(plane) for plane in selection_options]
    selection_options.append(plane_model)
    shuffle(selection_options)
    left_selections = selection_options[:3]
    right_selections = selection_options[3:]

    return render(request, 'PlaneViewer/plane_test.html', {'left_selections': left_selections,
                                                           "right_selections": right_selections,
                                                           'location': plane_file, 'author': plane.author,
                                                           'aircraft': plane.aircraft
                                                           })


def data_manager(request):
    if request.method == 'POST':
        data = Aircraft.objects.get(pk=request.POST['image_page'])
        plane = AircraftForm(request.POST, instance=data)
        location = 'PlaneViewer/images/' + data.location + '/' + data.name
        if plane.is_valid():
            # return the updated form instance of the same plane they were just looking at
            plane = plane.save()
            form = AircraftForm(initial=Aircraft.objects.get(pk=plane.image_page).data())
            return render(request, 'PlaneViewer/get_aircraft.html', {'form': form, 'image_location': location,
                                                                     'success': 'Plane saved!'})
        else:
            form = plane
            return render(request, 'PlaneViewer/get_aircraft.html', {'form': form, 'image_location': location,
                                                                     'success': 'Plane not saved.'})

    else:
        data = Aircraft.objects.filter(aircraft__isnull=True).filter(
                redownload_flag__exact=0).order_by('?').first()
        location = 'PlaneViewer/images/' + data.location + '/' + data.name
        redownload = data.redownload_flag
        form = AircraftForm(initial=data.data())

    return render(request, 'PlaneViewer/get_aircraft.html', {'form': form, 'image_location': location})