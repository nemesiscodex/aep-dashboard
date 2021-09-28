import django_tables2 as tables
from .models import CollectorActivation, CollectorFrames, CollectorSensors, Activation
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

class CollectorActivationTable(tables.Table):
    created_at = tables.DateTimeColumn(accessor='created_at_localtime', verbose_name=_("Created at"))
    frame = tables.Column(verbose_name=_("Frame"))

    def render_frame(self, value, record):
        css_class = 'text-success' if record.is_valid_frame() else 'text-danger'
        return format_html('<b class="{}">{}</b>', css_class, value)

    class Meta:
        model = CollectorActivation
        template_name = "tables/bootstrap4-responsive.html"
        order_by = ('-id', )

class CollectorSensorsTable(tables.Table):
    created_at = tables.DateTimeColumn(accessor='created_at_localtime', verbose_name=_("Created at"))
    precipitation = tables.Column(verbose_name=_("Precipitation (mm)"))
    wind_velocity = tables.Column(verbose_name=_("Wind Velocity (km/h)"))
    wind_direction = tables.Column(verbose_name=_("Wind Direction (°)"))
    humidity = tables.Column(verbose_name=_("Humidity (%)"))
    exterior_temperature = tables.Column(verbose_name=_("Exterior Temperature (°C)"))
    interior_temperature = tables.Column(verbose_name=_("Interior Temperature (°C)"))
    pressure = tables.Column(verbose_name=_("Pressure (mbar)"))

    
    class Meta:
        model = CollectorSensors
        template_name = "tables/bootstrap4-responsive.html"
        order_by = ('-id', )

class CollectorFramesTable(tables.Table):
    created_at = tables.DateTimeColumn(accessor='created_at_localtime', verbose_name=_("Created at"))
    satellite = tables.Column(verbose_name=_("Satellite Frame"))


    class Meta:
        model = CollectorFrames
        template_name = "tables/bootstrap4-responsive.html"
        order_by = ('-id', )
        

class ActivationTable(tables.Table):
    timestamp = tables.DateTimeColumn(verbose_name=_('Timestamp'))
    format_uptime_days = tables.Column(accessor='format_uptime_days', verbose_name=_('Uptime (Days)'))
    format_uptime_hms = tables.Column(accessor='format_uptime_hms', verbose_name=_('Uptime (hh:mm:ss)'))
    count = tables.Column(verbose_name=_('Counter'))
    detector_identifier = tables.Column(verbose_name=_('Detector identifier'))

    class Meta:
        model = Activation
        template_name = "tables/bootstrap4-responsive.html"
        exclude = ('collector_id', 'uptime_hours', 'uptime_days', 'uptime_minutes', 'uptime_seconds')
        order_by = ('-id', )