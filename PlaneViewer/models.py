from django.db import models


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
    image_license = models.CharField(max_length=100, null=True, blank=True)
    license_text = models.CharField(max_length=1000)
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
                "use_flag": self.use_flag,}

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('aircraft',)
        db_table = 'images'
        managed = False
