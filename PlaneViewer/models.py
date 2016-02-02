from django.db import models


class Types(models.Model):
    aircraft_type_id = models.IntegerField()
    aircraft_type = models.CharField(max_length=100)

    def _str__(self):
        return self.aircraft_type

    class Meta:
        ordering = ('aircraft_type_id',)
        db_table = 'types'


class AircraftType(models.Model):
    aircraft_name = models.CharField(max_length=100)
    aircraft_type_id = models.ForeignKey(Types)

    def data(self):
        return {'name': self.aircraft_name,
                'id': self.type_id}

    def __str__(self):
        return self.type_id


class Aircraft(models.Model):
    image_page = models.CharField(max_length=200, primary_key=True)
    image_url = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    image_license = models.CharField(max_length=100)
    license_text = models.CharField(max_length=1000)
    location = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    aircraft = models.CharField(max_length=100)
    aircraft_type = models.CharField(max_length=100)
    redownload_flag = models.BooleanField()

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
                "redownload_flag": self.redownload_flag}

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('aircraft',)
        db_table = 'images'
