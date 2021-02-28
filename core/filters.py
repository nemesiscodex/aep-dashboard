from django_filters import FilterSet
from django_filters.filters import DateTimeFromToRangeFilter
from django_filters.widgets import DateRangeWidget
from django.forms import DateTimeField
from .models import Activation, Collector

class CollectorFilter(FilterSet):
    created_at = DateTimeFromToRangeFilter(
        widget=DateRangeWidget(
            attrs={'type': 'datetime-local'}
        )
        
    )
    class Meta:
        model = Collector
        fields = ['created_at']

class ActivationFilter(FilterSet):
    timestamp = DateTimeFromToRangeFilter(
        widget=DateRangeWidget(
            attrs={'type': 'datetime-local'}
        )
        
    )
    class Meta:
        model = Activation
        fields = ['timestamp', 'detector_identifier']