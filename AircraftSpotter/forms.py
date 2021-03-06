from .models import Aircraft, ErrorReport
from django.forms import Form, ModelForm, Textarea, CheckboxInput, TextInput, URLField


# a test ModelForm class
class AircraftForm(ModelForm):

    class Meta:
        model = Aircraft
        fields = ("image_page", "image_url", "name", "description", "image_license", "license_text",
                  "location", "author", "aircraft", "aircraft_type", "redownload_flag", "use_flag")
        widgets = {"image_page": TextInput,
                   "image_url": TextInput,
                   "name": TextInput,
                   "description": Textarea(attrs={'cols': 80, 'rows': 10}),
                   "image_license": Textarea(attrs={'cols': 80, 'rows': 2}),
                   "license_text": Textarea(attrs={'cols': 80, 'rows': 10}),
                   "aircraft": TextInput,
                   "aircraft_type": TextInput,
                   "redownload_flag": CheckboxInput,
                   "use_flag": CheckboxInput,
                   }


class ErrorForm(ModelForm):

    class Meta:
        model = ErrorReport
        fields = {"open_response", "bad_picture", 'wrong_aircraft', 'image'}
        widgets = {"wrong_aircraft": CheckboxInput,
                   "bad_picture": CheckboxInput,
                   "open_response": TextInput,
                   }
