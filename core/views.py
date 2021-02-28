from core.filters import CollectorFilter, ActivationFilter
from django_filters.views import FilterView
from core.tables import ActivationTable, CollectorTable
from core.models import Activation, Collector
from django_tables2.views import SingleTableMixin

# Create your views here.

# @login_required(login_url="/login/")
class CollectorTableView(SingleTableMixin, FilterView):
    model = Collector
    table_class = CollectorTable
    template_name = "collector.html"
    filterset_class = CollectorFilter

# @login_required(login_url="/login/")
class ActivationsTableView(SingleTableMixin, FilterView):
    model = Activation
    table_class = ActivationTable
    template_name = "activations.html"
    filterset_class = ActivationFilter