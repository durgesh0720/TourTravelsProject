from django.urls import path
from . import views

urlpatterns=[
    path('',views.landingpage,name='landingpage'),
    path('destination/<str:cityName>/', views.Destinations, name='destination'),
    path('contact/', views.contact, name='contact')
]