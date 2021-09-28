from django_filters import FilterSet
from django_filters.filters import DateTimeFromToRangeFilter, CharFilter, OrderingFilter
from django_filters.widgets import DateRangeWidget
from django.forms import DateTimeField
from .models import Activation, CollectorActivation, CollectorSensors, CollectorFrames
from django.utils.translation import gettext_lazy as _

class CollectorFilter(FilterSet):
    created_at = DateTimeFromToRangeFilter(
        label=_("Created at"),
        widget=DateRangeWidget(
            attrs={'type': 'datetime-local'}
        )   
    )

    class Meta:
        model = CollectorActivation
        fields = ['created_at']

class CollectorSensorsFilter(FilterSet):
    created_at = DateTimeFromToRangeFilter(
        label=_("Created at"),
        widget=DateRangeWidget(
            attrs={'type': 'datetime-local'}
        )   
    )

    class Meta:
        model = CollectorSensors
        fields = ['created_at']

class CollectorFramesFilter(FilterSet):
    created_at = DateTimeFromToRangeFilter(
        label=_("Created at"),
        widget=DateRangeWidget(
            attrs={'type': 'datetime-local'}
        )   
    )

    class Meta:
        model = CollectorFrames
        fields = ['created_at']

class ActivationFilter(FilterSet):
    timestamp = DateTimeFromToRangeFilter(
        label=_("Timestamp"),
        widget=DateRangeWidget(
            attrs={'type': 'datetime-local'}
        )
    )
    detector_identifier = CharFilter(label=_("Detector identifier"))

    class Meta:
        model = Activation
        fields = ['timestamp', 'detector_identifier']