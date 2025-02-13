from django.urls import path
from . import views

urlpatterns=[
    path('tours/',views.tour_list,name="tours"),
]