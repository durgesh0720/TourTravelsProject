import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TrourismsBackend.settings")
django.setup()

import requests
import random
from decimal import Decimal
from faker import Faker
from tours.models import Category, Tour, TourImage
from home.models import CityOrState, Article

# ✅ Unsplash API Keys & Setup
UNSPLASH_ACCESS_KEYS = [
    "MDmgwAYutTaQTFgsdkEQYOHD-qW1gva112LTCeIP-b4",
    "01pyMBWSPPUyV4SqgN4bCkDPc4aDslz7QrNuZ2AWp-g",
    "IuaE3wPSiEJUK24VDGkGTgmF0EQk1H5hQGWRXumqfG4",
    "P8yZjayDPwy0lD6IuWbvQFJWNt8SmRxNWV8WenykENc",
    "THdDAoRtgMddbgNix5GAoXRyRW1RCmgb5NaIzR_Bms4",
    "Ug3do_SP1K_GREuhUwwXjz3De3x4iXdimo-qQphXhQM",
]
UNSPLASH_URL = "https://api.unsplash.com/photos/random"

fake = Faker()
current_api_index = 0  # Track which API key is in use

# ✅ Cities and Tours Data
CITIES = {
    "Rajasthan": ["Heritage Tour", "Cultural Journey", "Desert Safari", "Royal Palaces Tour"],
    "Kerala": ["Beach Holiday", "Wildlife Safari", "Backwater Cruise", "Ayurvedic Retreat"],
    "Goa": ["Beach Holiday", "Adventure Trip", "Party Tour", "Water Sports Experience"],
    "Himachal Pradesh": ["Adventure Trip", "Nature Retreat", "Skiing & Snowboarding", "Hiking & Trekking"],
    "Agra": ["Heritage Tour", "City Tour", "Historical Tour", "Architectural Wonders"],
    "Jaipur": ["Cultural Journey", "Heritage Tour", "Royal Palaces Tour", "Shopping & Handicrafts"],
    "Delhi": ["City Tour", "Cultural Journey", "Historical Tour", "Food & Street Markets"],
    "Manali": ["Adventure Trip", "Winter Wonderland", "Camping & Bonfire", "River Rafting"],
    "Varanasi": ["Religious Tour", "Cultural Journey", "Spiritual Retreat", "Ganga Aarti Experience"],
    "Mumbai": ["City Tour", "Beach Holiday", "Bollywood Tour", "Nightlife Experience"],
    "Kolkata": ["Cultural Journey", "City Tour", "Literary & Art Walk", "Food & Street Markets"],
    "Udaipur": ["Heritage Tour", "Lake & Palace Tour", "Romantic Getaway", "Photography Tour"],
    "Amritsar": ["Religious Tour", "Golden Temple Visit", "Food & Culinary Tour", "Historical Monuments"],
    "Shimla": ["Winter Wonderland", "Hiking & Trekking", "Scenic Hill Station Tour", "Heritage Walk"],
    "Rishikesh": ["Adventure Trip", "Spiritual Retreat", "Yoga & Meditation", "River Rafting"],
    "Haridwar": ["Religious Tour", "Ganga Aarti Experience", "Ayurvedic Retreat", "Temple Tour"],
    "Darjeeling": ["Tea Plantation Tour", "Toy Train Experience", "Scenic Hill Station Tour", "Hiking & Trekking"],
    "Jaisalmer": ["Desert Safari", "Camel Ride Adventure", "Historical Fort Tour", "Cultural Folk Music & Dance"],
    "Leh Ladakh": ["Adventure Trip", "Biking Expedition", "Nature Retreat", "Camping & Stargazing"],
    "Srinagar": ["Houseboat Stay", "Scenic Valley Tour", "Shikara Ride", "Garden & Mughal Heritage"],
    "Andaman & Nicobar": ["Beach Holiday", "Scuba Diving & Snorkeling", "Island Hopping", "Marine Life Tour"],
    "Mysore": ["Heritage Tour", "Palace & Temples Visit", "Cultural Festival Tour", "Yoga & Wellness Retreat"],
    "Ooty": ["Hill Station Tour", "Tea Plantation Walk", "Botanical Garden Visit", "Scenic Train Ride"],
    "Coorg": ["Coffee Plantation Tour", "Nature Retreat", "Waterfalls & Trekking", "Luxury Resort Stay"],
    "Chennai": ["City Tour", "Cultural Journey", "Temples & Heritage", "Food & Coastal Cuisine"],
    "Hyderabad": ["City Tour", "Heritage & Forts", "Food & Biryani Tour", "Shopping & Handicrafts"],
    "Pondicherry": ["Beach Holiday", "French Heritage Walk", "Yoga & Meditation Retreat", "Scenic Cafés & Street Art"],
    "Lonavala": ["Hill Station Tour", "Adventure & Trekking", "Waterfalls & Nature Trails", "Resort & Relaxation"],
    "Mahabaleshwar": ["Strawberry Farm Tour", "Scenic Valley View", "Boating & Nature Walk", "Hill Station Tour"],
    "Kutch": ["Rann of Kutch Festival", "White Desert Safari", "Handicraft & Culture Tour", "Wildlife Safari"],
    "Munnar": ["Tea Garden Walk", "Hill Station Tour", "Trekking & Nature Trails", "Waterfalls & Wildlife Safari"],
    "Chandigarh": ["City Tour", "Rock Garden & Rose Garden", "Luxury Resorts", "Heritage & Architecture"],
    "Bangalore": ["City Tour", "Tech Hub Exploration", "Cafés & Nightlife", "Food & Brewery Tour"],
    "Ajmer": ["Religious Tour", "Ajmer Sharif Dargah Visit", "Cultural & Heritage Tour", "Shopping & Street Markets"],
    "Guwahati": ["Wildlife Safari", "Tea Plantation Visit", "Brahmaputra River Cruise", "Spiritual Temple Tour"],
    "Shillong": ["Scenic Hill Station Tour", "Living Root Bridges Tour", "Waterfalls & Nature Walks", "Music & Cultural Festival"],
    "Kaziranga": ["Wildlife Safari", "One-Horned Rhino Tour", "Eco Tourism Experience", "Photography Tour"],
    "Kodaikanal": ["Hill Station Tour", "Lake & Waterfalls Visit", "Scenic Nature Walk", "Camping & Trekking"],
    "Bhubaneswar": ["Temple & Heritage Tour", "Konark Sun Temple Visit", "Tribal & Handicraft Culture", "Food & Street Cuisine"],
    "Sikkim": ["Monastery & Buddhist Tour", "Scenic Hill Station Tour", "Adventure & Trekking", "Lakes & Snow Capped Mountains"]
}

# ✅ Rotate API Key if limit is reached
def get_active_api_key():
    """Get the next available API key."""
    global current_api_index
    for _ in range(len(UNSPLASH_ACCESS_KEYS)):  # Loop through all API keys
        api_key = UNSPLASH_ACCESS_KEYS[current_api_index]
        current_api_index = (current_api_index + 1) % len(UNSPLASH_ACCESS_KEYS)
        return api_key  # Return a key from the list
    return None  # No available API key

# ✅ Fetch Multiple Images from Unsplash
def get_multiple_images(query="india tourism", count=5):
    """Fetch multiple images using Unsplash API with automatic API key switching."""
    images = []
    
    while len(images) < count:
        api_key = get_active_api_key()
        if not api_key:
            print("❌ No available API keys. Stopping image fetching.")
            break  # Stop if all keys are exhausted

        params = {"query": query, "client_id": api_key, "count": min(count - len(images), 10)}
        
        try:
            response = requests.get(UNSPLASH_URL, params=params)
            data = response.json()

            # ✅ Handle Rate Limit Exceeded
            if response.status_code == 403 and "Rate Limit Exceeded" in str(data):
                print(f"⚠️ API Key {api_key} has reached the limit. Switching...")
                continue  # Switch to the next API key

            # ✅ Handle Too Many Requests
            if response.status_code == 429:
                print(f"⚠️ Too many requests with API Key {api_key}. Switching...")
                continue  # Switch to the next API key

            # ✅ Process Successful Response
            if response.status_code == 200 and isinstance(data, list):
                images.extend([img["urls"]["regular"] for img in data])
            else:
                print(f"⚠️ Unexpected Error: {response.status_code} - {data}")

        except Exception as e:
            print(f"⚠️ Error fetching images: {e}")

    return images


# ✅ Generate an article description for a city
def generate_article_description(city):
    return f"""
    *Discover the Beauty of {city}*
    {fake.paragraph(nb_sentences=6)}

    *Why Visit {city}?*
    {fake.paragraph(nb_sentences=4)}

    *Top Attractions in {city}*
    - {fake.sentence(nb_words=8)}
    - {fake.sentence(nb_words=8)}
    - {fake.sentence(nb_words=8)}

    *Travel Tips for {city}*
    {fake.paragraph(nb_sentences=3)}

    *Best Time to Visit:* {fake.month()} - {fake.month()}  
    📍 Local Delicacies: {fake.word().title()}, {fake.word().title()}, {fake.word().title()}  
    """
# ✅ Seed database with cities, articles, and tours
def seed_data(num_tours_per_city=10):
    """Generate and save random cities, articles, and tours."""
    
    for city, tour_types in CITIES.items():
        # ✅ Ensure the city exists
        city_obj, created = CityOrState.objects.get_or_create(
            name=city,
            defaults={
                "description": fake.paragraph(nb_sentences=6),
                "attractions": ", ".join([fake.word().title() for _ in range(5)]),
                "travel_tips": fake.paragraph(nb_sentences=3),
            }
        )

        # ✅ Fetch multiple images for the city
        city_images = get_multiple_images(query=f"{city} tourism", count=5)
        if city_images:
            city_obj.image = city_images[0]  # ✅ Save the first image
            city_obj.save()

        # ✅ Create an article for the city
        article = Article.objects.create(
            city_or_state=city_obj,
            title=f"Explore {city}: A Travel Guide",
            content=generate_article_description(city),
            image=city_images[1] if len(city_images) > 1 else None
        )

        print(f"✅ Created City: {city_obj.name} - Article: {article.title}")

        # ✅ Generate tours for the city
        for _ in range(num_tours_per_city):
            tour_type = random.choice(tour_types)
            category, _ = Category.objects.get_or_create(name=tour_type.split()[0])

            price = Decimal(random.randint(2000, 50000))
            description = generate_article_description(city)
            tour = Tour.objects.create(
                name=f"{city} {tour_type}",
                category=category,
                city_or_state=city_obj,  # ✅ Assign city to tour
                location = city,
                description=description,
                price=price,
                duration=random.randint(2, 15),
                start_date=fake.date_between(start_date="-30d", end_date="+30d"),
                end_date=fake.date_between(start_date="+31d", end_date="+90d"),
                available_slots=random.randint(5, 20),
                is_featured=random.choice([True, False])
            )

            # ✅ Fetch images for the tour
            tour_images = get_multiple_images(query=f"{city} {tour_type}", count=4)
            if tour_images:
                tour.image = tour_images[0]  # ✅ Set main tour image
                for img_url in tour_images[1:]:  # ✅ Store additional images
                    TourImage.objects.create(tour=tour, image=img_url)

            tour.save()
            print(f"✅ Created Tour: {tour.name} - {tour.city_or_state.name} - Price: {price}")

def run():
    """Run the seeding process."""
    print("🚀 Seeding cities, articles, and tours...")
    seed_data(num_tours_per_city=10)
    print("✅ Seeding completed!")