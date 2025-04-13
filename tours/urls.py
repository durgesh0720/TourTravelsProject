from django.urls import path
from . import views

urlpatterns=[
    path('tours/',views.tour_list,name="tours"),
    path('tour-details/<int:tour_id>/',views.viewDetails, name="tour_details")
]