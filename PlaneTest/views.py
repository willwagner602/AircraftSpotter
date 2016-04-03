from random import shuffle

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static


from .models import Aircraft, AircraftType, UserHistory
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

        success = 'Wrong! That plane was a ' + current_type

        # return a message about whether the guess was accurate
        if current_type == request.POST['answer']:
            success = "Success!"

        page_vars['success'] = success

        # for authenticated users, add this aircraft to their history
        if request.user.is_authenticated():
            try:
                user_history = UserHistory.objects.get(user_id=request.user.pk)
            except UserHistory.DoesNotExist:
                user_history = UserHistory.create(request.user.pk)
                user_history.save()

            user_history.add_history(plane.pk, success)

    return render(request, 'PlaneViewer/aircraft_test.html', page_vars)


def error_report(request, current_image_id):

    plane = Aircraft.objects.get(image_id=current_image_id)
    image_location = static('PlaneTest/images/' + plane.location + '/' + plane.name)

    if request.method == 'POST':

        error_form = ErrorForm(request.POST)

        print(request.POST)

        if error_form.is_valid():
            error_form.save()

            return render(request, 'PlaneViewer/error_report.html', {
                'image_id': current_image_id,
                'image_location': image_location,
                'plane': plane.aircraft,
                'error_url': str(plane.image_id),
                'form': error_form,
                'success': 'Form Saved'
            })
        else:
            return render(request, 'PlaneViewer/error_report.html', {
                'image_id': current_image_id,
                'image_location': image_location,
                'plane': plane.aircraft,
                'error_url': str(plane.image_id),
                'form': error_form,
                'errors': error_form.errors
            })

        # store the error report, return to page with success and the error data

    # serve admins the data management page
    if request.user.is_superuser:
        return HttpResponseRedirect('/data/' + current_image_id)

    # serve regular users the error page
    else:
        return render(request, 'PlaneViewer/error_report.html', {
            'image_id': current_image_id,
            'image_location': image_location,
            'plane': plane.aircraft,
            'error_url': str(plane.image_id)
        })


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


def convert_user_history_to_rows(user_history, row_length=6):
    history_in_rows = []
    current_row = []
    image_count = 0

    print("Length of user history is ", len(user_history))

    for image in user_history:

        if image_count < row_length:
            current_row.append(image)
            image_count += 1
        else:
            history_in_rows.append(current_row)
            current_row = [image,]
            image_count = 1

    history_in_rows.append(current_row)

    return history_in_rows


def history(request):

    page_vars = {}

    if request.user.is_authenticated():
        try:
            user_history = UserHistory.objects.get(user_id=request.user.pk).get_aircraft_history()

            # transform the plane IDs into the full images to display in the template
            user_history = [Aircraft.objects.get(pk=image) for image in user_history]
            user_history = [static_location(image) for image in user_history]
            user_history = convert_user_history_to_rows(user_history)
            page_vars['user_history'] = user_history

        except UserHistory.DoesNotExist:
            page_vars['error'] = 'You have no history.  Try testing a few planes!'
    else:
        page_vars['error'] = 'You must be logged in to view your history.'

    return render(request, 'PlaneViewer/test_history.html', page_vars)
