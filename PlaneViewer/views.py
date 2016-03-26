from random import shuffle

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

from .models import Aircraft, AircraftType
from .forms import AircraftForm


def aircraft_test(request):
    if request.method == 'POST':
        # get the plane's id and the guess
        print(request.POST)
        # return a message about whether the guess was accurate
        pass
    # get the individual plane for display, and the necessary data to display it
    current_choices = ["Ilyushin Il-86",
                       "Ilyushin Il-96",
                       "Lockheed L-1011 TriStar",
                       "McDonnell Douglas DC-10",
                       "McDonnell Douglas MD-11"]

    plane = Aircraft.objects.filter(aircraft__in=current_choices)
    plane = plane.filter(redownload_flag__exact=0).order_by('?').first()
    plane_file = 'PlaneViewer/images/' + plane.location + '/' + plane.name

    # get information necessary to identify similar planes for challenging multiple choice options
    plane_model = plane.aircraft
    type_int = AircraftType.objects.filter(aircraft_name=plane_model).first().type_int

    # get selection for multiple choice options
    selection_options = AircraftType.objects.filter(type_int__exact=type_int).order_by('?').all()

    # exclude the correct answer
    selection_options = selection_options.exclude(aircraft_name__exact=plane_model)

    # get 5 aircraft names and create a list of them, then add the correct answer
    selection_options = [str(plane) for plane in selection_options[:5]]
    selection_options.append(plane_model)

    # randomize the selection and create the left and right lists for the final page
    shuffle(selection_options)
    left_selections = selection_options[:3]
    right_selections = selection_options[3:]

    return render(request, 'PlaneViewer/aircraft_test.html', {'left_selections': left_selections,
                                                              'right_selections': right_selections,
                                                              'selections': selection_options,
                                                              'location': static(plane_file),
                                                              'author': plane.author,
                                                              'aircraft': plane.aircraft,
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
            return render(request, 'PlaneViewer/aircraft_data.html', {'form': form, 'image_location': location,
                                                                     'success': 'Plane saved!'})
        else:
            form = plane
            return render(request, 'PlaneViewer/aircraft_data.html', {'form': form, 'image_location': location,
                                                                     'success': 'Plane not saved.'})

    else:
        data = Aircraft.objects.filter(aircraft__isnull=True).filter(
                redownload_flag__exact=0).order_by('?').first()
        location = 'PlaneViewer/images/' + data.location + '/' + data.name
        redownload = data.redownload_flag
        form = AircraftForm(initial=data.data())

    return render(request, 'PlaneViewer/aircraft_data.html', {'form': form, 'image_location': location})


def user(request):
    if request.method == 'POST':
        pass
    else:
        user = User.objects
    return render(request, 'PlaneViewer/aircraft_user.html', {})
