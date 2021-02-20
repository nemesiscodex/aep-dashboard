from django.db import models
from enum import Enum

class Location(models.Model):
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)

    class Meta:
        abstract = True

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)        

class AreaType(ChoiceEnum):
    House, Location, Village, Town, City, State, Region, Country = range(8)


# Models
class Area(Location):
    name = models.CharField(max_length=200)
    area_type = models.CharField(max_length=16, choices=AreaType.choices())
    parent_area = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True
    )

class SensorType(ChoiceEnum):
    KissingBug, = range(1)

class Sensor(Location):
    sensor_type = models.CharField(max_length=16, choices=SensorType.choices())
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True
    )