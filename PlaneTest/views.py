from random import shuffle

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

from .models import Aircraft, AircraftType
from .forms import AircraftForm


def aircraft_test(request):

    # get the individual plane for display, and the necessary data to display it
    current_choices = ["Ilyushin Il-86",
                       "Ilyushin Il-96",
                       "Lockheed L-1011 TriStar",
                       "McDonnell Douglas DC-10",
                       "McDonnell Douglas MD-11"]

    plane = Aircraft.objects.filter(redownload_flag__exact=0, aircraft_type__isnull=False).order_by('?').first()
    print(Aircraft.objects.filter(redownload_flag__exact=0, aircraft_type__isnull=False).order_by('?'))
    plane_file = 'PlaneTest/images/' + plane.location + '/' + plane.name

    # get information necessary to identify similar planes for challenging multiple choice options
    plane_model = plane.aircraft
    type_int = AircraftType.objects.get(aircraft_name=plane_model).type_int

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

    page_vars = {'left_selections': left_selections,
                 'right_selections': right_selections,
                 'selections': selection_options,
                 'location': static(plane_file),
                 'author': plane.author,
                 'aircraft_id': plane.image_id,
                 }

    if request.method == 'POST':
        # get the plane's id and the guess
        current_plane = Aircraft.objects.get(image_id=request.POST['aircraft_id'])
        current_type = current_plane.aircraft
        if current_type == request.POST['answer']:
            page_vars['success'] = "Success!"
        else:
            page_vars['success'] = "Wrong! That plane was a " + current_type

        print(request.POST)

        # return a message about whether the guess was accurate

    return render(request, 'PlaneViewer/aircraft_test.html', page_vars)


def error_report(request):

    if request.method == 'POST':
        pass

        # store the error report, return to page with success and the error data

    # if the user is an admin, serve them the data page
    if request.user.is_superuser:
        return data_manager(request)
    # if the user is a regular user, serve them the error page
    else:
        return render(request, 'PlaneViewer/error_report.html', {})


def data_manager(request):
    if request.method == 'POST':
        data = Aircraft.objects.get(pk=request.POST['image_page'])
        plane = AircraftForm(request.POST, instance=data)
        location = 'PlaneTest/images/' + data.location + '/' + data.name
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
        location = 'PlaneTest/images/' + data.location + '/' + data.name
        redownload = data.redownload_flag
        form = AircraftForm(initial=data.data())

    return render(request, 'PlaneViewer/aircraft_data.html', {'form': form, 'image_location': location})
