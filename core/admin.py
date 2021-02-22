from django.contrib.gis import admin
from .models import Detector, Area

admin.site.register(Detector, admin.GeoModelAdmin)
admin.site.register(Area, admin.GeoModelAdmin)