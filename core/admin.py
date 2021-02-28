from django.contrib.gis import admin
from .models import Detector, Area

class DetectorAdmin(admin.OSMGeoAdmin):
    default_lon = -23
    default_lat = -57
    default_zoom = 11
    readonly_fields = ('latitude','longitude')

admin.site.register(Detector, DetectorAdmin)
admin.site.register(Area, admin.OSMGeoAdmin)