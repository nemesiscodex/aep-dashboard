import django_tables2 as tables
from .models import Collector, Activation
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

class CollectorTable(tables.Table):
    created_at = tables.DateTimeColumn(accessor='created_at_localtime', verbose_name=_("Created at"))
    frame = tables.Column(verbose_name=_("Frame"))

    def render_frame(sefl, value, record):
        css_class = 'text-success' if record.is_valid_frame() else 'text-danger'
        return format_html('<b class="{}">{}</b>', css_class, value)

    class Meta:
        model = Collector
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