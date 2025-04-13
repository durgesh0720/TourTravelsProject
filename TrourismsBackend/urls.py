from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('tours/',include('tours.urls')),
    # path('payments/', include('payments.urls')),
    # path('booking/', include('bookings.urls'))
]
if settings.DEBUG:  # Serve images during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)