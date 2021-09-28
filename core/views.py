from core.filters import CollectorFilter, ActivationFilter, CollectorSensorsFilter, CollectorFramesFilter
from django_filters.views import FilterView
from core.tables import ActivationTable, CollectorActivationTable, CollectorSensorsTable, CollectorFramesTable
from core.models import Activation, CollectorActivation, CollectorSensors, CollectorFrames
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin

# Create your views here.

class CollectorTableView(ExportMixin, SingleTableMixin, FilterView):
    model = CollectorActivation
    table_class = CollectorActivationTable
    template_name = "collector.html"
    filterset_class = CollectorFilter

class CollectorSensorsTableView(ExportMixin, SingleTableMixin, FilterView):
    model = CollectorSensors
    table_class = CollectorSensorsTable
    template_name = "sensors.html"
    filterset_class = CollectorSensorsFilter

class CollectorFramesTableView(ExportMixin, SingleTableMixin, FilterView):
    model = CollectorFrames
    table_class = CollectorFramesTable
    template_name = "frames.html"
    filterset_class = CollectorFramesFilter

class ActivationsTableView(ExportMixin, SingleTableMixin, FilterView):
    model = Activation
    table_class = ActivationTable
    template_name = "activations.html"
    filterset_class = ActivationFilter