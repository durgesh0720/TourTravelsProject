import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TrourismsBackend.settings")
django.setup()

import requests
import random
from decimal import Decimal
from faker import Faker
from tours.models import Category, Tour

# Unsplash API Configuration
UNSPLASH_ACCESS_KEY = "UoBWgUMtzIgbrUcJNR94-mYTi7ly6UMhdhFXO8g52Z4"
UNSPLASH_URL = "https://api.unsplash.com/photos/random"

# Faker for random data generation
fake = Faker()

# Tour Categories
TOUR_TYPES = ["Heritage Tour", "Adventure Trip", "Cultural Journey", "Wildlife Safari", "Beach Holiday", "Religious Tour"]
LOCATIONS = ["Rajasthan", "Kerala", "Goa", "Himachal Pradesh", "Agra", "Jaipur", "Delhi", "Manali", "Varanasi", "Mumbai", "Kolkata"]

def get_random_image(query="india tourism"):
    """Fetch a random image from Unsplash API."""
    params = {"query": query, "client_id": UNSPLASH_ACCESS_KEY, "count": 1}
    try:
        response = requests.get(UNSPLASH_URL, params=params)
        data = response.json()
        if response.status_code == 200 and data:
            return data[0]["urls"]["regular"]
    except Exception as e:
        print(f"Error fetching image: {e}")
    return None  

def format_price(amount):
    """Convert Decimal amount to formatted INR string."""
    return f"₹{amount:,.2f}"

def seed_tours(num_tours=30):
    """Generate and save random tours."""
    for _ in range(num_tours):
        location = random.choice(LOCATIONS)
        tour_type = random.choice(TOUR_TYPES)
        category, _ = Category.objects.get_or_create(name=tour_type.split()[0])

        price = Decimal(random.randint(5000, 50000))
        tour = Tour.objects.create(
            name = (f"{location} {tour_type}")[:255],
            category=category,
            description=fake.paragraph(nb_sentences=3),
            price=price,
            duration=random.randint(2, 15),
            location=location,
            start_date=fake.date_between(start_date="-30d", end_date="+30d"),
            end_date=fake.date_between(start_date="+31d", end_date="+90d"),
            available_slots=random.randint(5, 20),
            is_featured=random.choice([True, False])
        )

        image_url = get_random_image(query=f"{location} tourism")
        if image_url:
            tour.image = image_url  

        tour.save()
        print(f"Created tour: {tour.name} - {tour.location} - Price: {format_price(price)}")


def run():
    """This is the required function for runscript to work."""
    print("Seeding tours...")
    seed_tours(30)
    print("Seeding completed!")
