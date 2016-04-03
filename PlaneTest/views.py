from random import shuffle

from django.shortcuts import render
from django.contrib.staticfiles.templatetags.staticfiles import static

from .models import Aircraft, AircraftType
from .forms import AircraftForm, ErrorForm


def static_location(aircraft):
    return static('PlaneTest/images/' + aircraft.location + '/' + aircraft.name)


def aircraft_test(request):

    # get the individual plane for display, and the necessary data to display it
    plane = Aircraft.objects.filter(redownload_flag__exact=0, aircraft_type__isnull=False).order_by('?').first()

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
                 'location': static_location(plane),
                 'author': plane.author,
                 'aircraft_id': plane.image_id,
                 'error_url': 'error_report/' + str(plane.image_id)
                 }

    if request.method == 'POST':
        # get the plane's id and the guess
        current_plane = Aircraft.objects.get(image_id=request.POST['aircraft_id'])
        current_type = current_plane.aircraft

        # return a message about whether the guess was accurate
        if current_type == request.POST['answer']:
            page_vars['success'] = "Success!"
        else:
            page_vars['success'] = "Wrong! That plane was a " + current_type

    return render(request, 'PlaneViewer/aircraft_test.html', page_vars)


def error_report(request, current_image_id):

    if request.method == 'POST':
        print(request.POST)

        # store the error report, return to page with success and the error data

    # serve admins the data management page
    if request.user.is_superuser:
        return data_manager(request, current_image_id)

    # serve regular users the error page
    else:
        plane = Aircraft.objects.get(image_id=current_image_id)
        image_location = static('PlaneTest/images/' + plane.location + '/' + plane.name)
        form = ErrorForm()
        print(form)
        return render(request, 'PlaneViewer/error_report.html', {'image_id': current_image_id,
                                                                 'image_location': image_location,
                                                                 'plane': plane.aircraft,
                                                                 'form': form,
                                                                 'error_url': 'error_report/' + str(plane.image_id)})


def data_manager(request, current_image_id):

    aircraft = Aircraft.objects.get(image_id=current_image_id)
    aircraft_data = aircraft.data()
    data_url = current_image_id

    use_flag = False
    redownload_flag = False

    if aircraft_data['use_flag'] == 1:
        use_flag = True

    if aircraft_data['redownload_flag'] == 1:
        redownload_flag = True

    if request.method == 'POST':

        aircraft_form = AircraftForm(request.POST, instance=aircraft)

        if aircraft_form.is_valid():
            aircraft_form.save()

            # return the updated form instance of the same plane they were just looking at
            return render(request, 'PlaneViewer/data_manager.html', {
                'aircraft_data': aircraft_data,
                'success': 'Plane saved!',
                'data_url': data_url,
                'use_flag': use_flag,
                'redownload_flag': redownload_flag,
                'location': static_location(aircraft),
            })
        else:
            return render(request, 'PlaneViewer/data_manager.html', {
                'aircraft_data': aircraft_data,
                'success': 'Plane not saved.',
                'errors': aircraft_form.errors,
                'data_url': data_url,
                'use_flag': use_flag,
                'redownload_flag': redownload_flag,
                'location': static_location(aircraft),
            })

    return render(request, 'PlaneViewer/data_manager.html', {
        'aircraft_data': aircraft_data,
        'data_url': data_url,
        'use_flag': use_flag,
        'redownload_flag': redownload_flag,
        'location': static_location(aircraft),
    })
