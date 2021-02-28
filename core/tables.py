import django_tables2 as tables
from .models import Collector, Activation
from django.utils.html import format_html

class CollectorTable(tables.Table):

    def render_frame(sefl, value, record):
        css_class = 'text-success' if record.is_valid_frame() else 'text-danger'
        return format_html('<b class="{}">{}</b>', css_class, value)

    class Meta:
        model = Collector
        template_name = "django_tables2/bootstrap-responsive.html"
        

class ActivationTable(tables.Table):
    uptime = tables.Column(accessor='uptime',
         verbose_name='Uptime')
    class Meta:
        model = Activation
        template_name = "django_tables2/bootstrap-responsive.html"
        exclude = ('collector_id', 'uptime_days', 'uptime_hours', 'uptime_minutes', 'uptime_seconds')