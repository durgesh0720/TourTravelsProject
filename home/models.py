from django.db import models

# Create your models here.
class CityOrState(models.Model):
    """Model to store a specific city or state, along with related tour articles and attractions."""
    name = models.CharField(max_length=255, unique=True)  # City/State name
    description = models.TextField()  # General description
    image = models.ImageField(upload_to='cities/', null=True, blank=True)  # Cover image
    attractions = models.TextField(blank=True)  # List of major attractions (comma-separated)
    travel_tips = models.TextField(blank=True)  # Travel tips or advice

    def __str__(self):
        return self.name
    
class Article(models.Model):
    """Articles about a specific city or state."""
    city_or_state = models.ForeignKey(CityOrState, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.city_or_state.name}"