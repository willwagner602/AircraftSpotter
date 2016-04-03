from django.db import models
from django.contrib.auth.models import User
import json


class Types(models.Model):
    type_id = models.IntegerField()
    aircraft_type = models.CharField(max_length=100)

    def _str__(self):
        return self.aircraft_type

    class Meta:
        ordering = ('type_id',)
        db_table = 'types'
        managed = False


class AircraftType(models.Model):
    aircraft_name = models.CharField(max_length=100)
    type_int = models.IntegerField()

    def data(self):
        return {'name': self.aircraft_name,
                'type_int': self.type_int}

    def __str__(self):
        return self.aircraft_name

    class Meta:
        db_table = 'aircraft_type'
        managed = False


class Aircraft(models.Model):
    image_id = models.IntegerField(primary_key=True)
    image_page = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    image_license = models.CharField(max_length=2000, null=True, blank=True)
    license_text = models.CharField(max_length=3000)
    location = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    aircraft = models.CharField(max_length=100, null=True, blank=True)
    aircraft_type = models.CharField(max_length=100, null=True, blank=True)
    redownload_flag = models.BooleanField()
    use_flag = models.BooleanField()
    description = models.CharField(max_length=1000, null=True, blank=True)

    def data(self):
        return {"image_page": self.image_page,
                "image_url": self.image_url,
                "name": self.name,
                "image_license": self.image_license,
                "license_text": self.license_text,
                "location": self.location,
                "author": self.author,
                "aircraft": self.aircraft,
                "aircraft_type": self.aircraft_type,
                "redownload_flag": self.redownload_flag,
                "description": self.description,
                "use_flag": self.use_flag,
                }

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('aircraft',)
        db_table = 'images'
        managed = False


class ErrorReport(models.Model):
    error_id = models.IntegerField(primary_key=True)
    image = models.ForeignKey(Aircraft)
    wrong_aircraft = models.BooleanField(default=False)
    bad_picture = models.BooleanField(default=False)
    open_response = models.CharField(max_length=200, null=False, blank=True)


class UserHistory(models.Model):
    user_id = models.ForeignKey(User)
    user_history = models.TextField()

    def get_history(self):
        return json.loads(self.user_history)

    def add_history(self, aircraft_id, status):
        current_history = self.get_history()
        print(type(current_history))
        current_history.append((aircraft_id, status))
        print(current_history)
        self.user_history = json.dumps(current_history)
        self.save()

    def get_plane_history(self):
        # return the plane id for each entry in the user's history
        return [x[0] for x in self.get_history()]

    @classmethod
    def create(cls, user_id):
        user_history = cls(user_id=User.objects.get(pk=user_id), user_history=json.dumps([]))
        return user_history
