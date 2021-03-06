from django.contrib.gis.db import models
from django.utils.timezone import make_aware
import pytz
from enum import Enum
import re

class CollectorActivation(models.Model):
    pattern = r'^@(\d{3})-(\d{2}):(\d{2}):(\d{2})\*(\d{2})-(\d{4})(\d{4})(\d{4})(\d{4})=(\d{3});$'
    created_at = models.DateTimeField(blank=True, null=True)
    frame = models.CharField(max_length=64)

    def created_at_localtime(self):
        return make_aware(self.created_at, timezone=pytz.timezone('UTC'))

    def match_frame(self):
        return re.search(CollectorActivation.pattern, self.frame)

    def is_valid_frame(self):
        return bool(self.match_frame())

    class Meta:
        managed = False
        db_table = 'collector_activation'

class CollectorSensors(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    precipitation = models.FloatField()
    wind_velocity = models.FloatField()
    wind_direction = models.FloatField()
    humidity = models.FloatField()
    exterior_temperature = models.FloatField()
    interior_temperature = models.FloatField()
    pressure = models.FloatField()
    
    def created_at_localtime(self):
        return make_aware(self.created_at, timezone=pytz.timezone('UTC'))

    class Meta:
        managed = False
        db_table = 'collector_sensors'

class CollectorFrames(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    satellite = models.CharField(max_length=64)

    def created_at_localtime(self):
        return make_aware(self.created_at, timezone=pytz.timezone('UTC'))

    class Meta:
        managed = False
        db_table = 'collector_frames'

class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    geom = models.PointField()

    def save(self, *args, **kwargs):
        self.longitude = self.geom.x
        self.latitude  = self.geom.y
        super(Location, self).save(*args, **kwargs)  

    class Meta:
        abstract = True

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.name) for i in cls)        

class AreaType(ChoiceEnum):
    House, Location, Village, Town, City, State, Region, Country = range(8)


# Models
class Area(models.Model):
    name = models.CharField(max_length=200)
    area_type = models.CharField(max_length=16, choices=AreaType.choices())

    geom = models.PolygonField()

    def __str__(self):
        return "{} - ({})".format(self.name, self.area_type)

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

    def __str__(self):
        return "{} - ({})".format(self.identifier, self.detector_type)

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

    def format_uptime_hms(self):
        return '{:02d}:{:02d}:{:02d}'.format(
            self.uptime_hours,
            self.uptime_minutes,
            self.uptime_seconds
        )

    def format_uptime_days(self):
        return '{:04d}'.format(
            self.uptime_days
        )

    class Meta:
        indexes = [
            models.Index(fields=['detector_identifier']),
            models.Index(fields=['count']),
            models.Index(fields=['timestamp'])
        ]