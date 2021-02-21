from django.db import models
from enum import Enum

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        abstract = True

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)        

class AreaType(ChoiceEnum):
    House, Location, Village, Town, City, State, Region, Country = range(8)


# Models
class Area(models.Model):
    name = models.CharField(max_length=200)
    area_type = models.CharField(max_length=16, choices=AreaType.choices())
    # TODO: polygon type

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['area_type'])
        ]

class DetectorType(ChoiceEnum):
    KissingBug, = range(1)

class Detector(Location):
    detector_type = models.CharField(max_length=16, choices=DetectorType.choices())
    identifier = models.CharField(max_length=16, null=False)

    class Meta:
        indexes = [
            models.Index(fields=['identifier']),
            models.Index(fields=['detector_type'])
        ]

class Activation(models.Model):
    timestamp = models.DateTimeField()
    detector_identifier = models.CharField(max_length=16, null=False)
    uptime_days = models.IntegerField()
    uptime_hours = models.IntegerField()
    uptime_minutes = models.IntegerField()
    uptime_seconds = models.IntegerField()
    sensor_1 = models.IntegerField()
    sensor_2 = models.IntegerField()
    sensor_3 = models.IntegerField()
    sensor_4 = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['detector_identifier']),
            models.Index(fields=['count']),
            models.Index(fields=['timestamp'])
        ]