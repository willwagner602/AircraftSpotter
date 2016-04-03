from django.contrib import admin
from .models import Aircraft, ErrorReport, UserHistory

# Register your models here.

admin.site.register(Aircraft)
admin.site.register(ErrorReport)
admin.site.register(UserHistory)