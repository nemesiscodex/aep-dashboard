from core.filters import CollectorFilter, ActivationFilter
from django_filters.views import FilterView
from core.tables import ActivationTable, CollectorTable
from core.models import Activation, Collector
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin

# Create your views here.

class CollectorTableView(ExportMixin, SingleTableMixin, FilterView):
    model = Collector
    table_class = CollectorTable
    template_name = "collector.html"
    filterset_class = CollectorFilter

class ActivationsTableView(ExportMixin, SingleTableMixin, FilterView):
    model = Activation
    table_class = ActivationTable
    template_name = "activations.html"
    filterset_class = ActivationFilter