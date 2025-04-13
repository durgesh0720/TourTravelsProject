from django.contrib import admin
from .models import Tour, Category, TourImage

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'available_slots', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'location')
    inlines = [TourImageInline]

admin.site.register(Category)
admin.site.register(TourImage)
