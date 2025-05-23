from django.db import models
from home.models import CityOrState

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tour(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="tours")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price in USD or chosen currency
    duration = models.PositiveIntegerField(help_text="Duration in days")
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    available_slots = models.PositiveIntegerField(default=10)
    city_or_state = models.ForeignKey(CityOrState, on_delete=models.CASCADE, related_name="tours")  # Linking to City/State
    image = models.ImageField(upload_to='tours/', null=True, blank=True)  # Main image
    additional_images = models.ManyToManyField('TourImage', blank=True, related_name="tour_images")

    is_featured = models.BooleanField(default=False)  # Highlighted tours on homepage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to='tour_gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.tour.name}"
