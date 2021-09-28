from django.contrib.auth.decorators import login_required
from core.views import ActivationsTableView, CollectorTableView, CollectorSensorsTableView, CollectorFramesTableView
from django.urls import path, re_path
from .views import login_view, register_user, index, pages
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    # path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # The home page
    path('', index, name='home'),

    path(
        'collector/', 
        login_required(login_url="/login/")(CollectorTableView.as_view()),
        name='collector'
    ),
    path(
        'sensors/', 
        login_required(login_url="/login/")(CollectorSensorsTableView.as_view()),
        name='sensors'
    ),
    path(
        'frames/', 
        login_required(login_url="/login/")(CollectorFramesTableView.as_view()),
        name='frames'
    ),
    path(
        'activations/', 
        login_required(login_url="/login/")(ActivationsTableView.as_view()),
        name='activations'
    ),

    # Matches any html file
    # re_path(r'^.*\.*', pages, name='pages')
]