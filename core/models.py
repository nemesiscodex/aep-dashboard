from django.contrib.gis.db import models
from enum import Enum

class Collector(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    frame = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'collector'

class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    geom = models.PointField()

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

    geom = models.PolygonField()

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
    collector_id = models.IntegerField(unique=True, null=True)
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