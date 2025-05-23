from django.shortcuts import render,get_object_or_404
from tours.models import Tour,TourImage
from django.core.paginator import Paginator
from .models import CityOrState,Article

def landingpage(request):
    locations = Tour.objects.values_list('location', flat=True).distinct()
    travel_types = Tour.objects.values_list('category__name', flat=True).distinct()  # Fetching unique travel categories
    Cities = CityOrState.objects.all()

    tours = Tour.objects.all().order_by("?")  # Fetch all tours
    page_number = request.GET.get("page", 1)  # Get the current page from the request
    paginator = Paginator(tours, 9) 
    try:
        page_obj = paginator.page(page_number)
    except Exception:
        page_obj = paginator.page(1)

    context={
        "page_obj": page_obj,
        "locations":locations,
        "travel_types": travel_types,
        "Cities":Cities,
    }
    return render(request,'home/landingPage.html',context)

def Destinations(request,cityName):
    city_obj = get_object_or_404(CityOrState, name=cityName)
    tours_obj = Tour.objects.filter(city_or_state=city_obj).order_by("?")[:9]
    city_articles = Article.objects.filter(city_or_state=city_obj)
    tour_images = TourImage.objects.filter(tour = tours_obj.first())
    context = {
        "city": city_obj,
        "tours": tours_obj,
        "articles": city_articles,
        "tour_images":tour_images
    }
    return render(request, "home/Destinations.html", context)

def contact(request):
    cities = CityOrState.objects.all()
    return render(request, "home/contact.html", {"cities": cities})
