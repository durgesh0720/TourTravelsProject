from django.contrib import admin
from .models import CityOrState
# admin.site.site_header = "Tour and Travels Dashboard"
# admin.site.site_title = "Dashboard"
# admin.site.index_title = "Tour and Travels Dashboard"
admin.site.register(CityOrState)