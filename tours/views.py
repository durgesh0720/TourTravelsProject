from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Tour

def tour_list(request):
    # Get filter values from the form submission
    location = request.GET.get("location", "")
    duration = request.GET.get("duration", "")
    tour_type = request.GET.get("tour_type", "")
    page_number = request.GET.get("page", 1)

    # Start with all tours
    tours = Tour.objects.all()

    # Apply filters based on user input
    if location and location.lower() != "all":
        tours = tours.filter(location__icontains=location)
    
    if duration and duration.lower() != "all":
        if duration == "1-3":
            tours = tours.filter(duration__gte=1, duration__lte=3)
        elif duration == "4-7":
            tours = tours.filter(duration__gte=4, duration__lte=7)
        elif duration == "8+":
            tours = tours.filter(duration__gte=8)

    if tour_type and tour_type.lower() != "all":
        tours = tours.filter(category__name__icontains=tour_type)

    # Apply pagination (9 tours per page)
    paginator = Paginator(tours, 9)
    try:
        page_obj = paginator.page(page_number)
    except Exception:
        page_obj = paginator.page(1)

    # Get distinct values for filters
    locations = Tour.objects.values_list('location', flat=True).distinct()
    travel_types = Tour.objects.values_list('category__name', flat=True).distinct()

    # Pass context to the template
    context = {
        "page_obj": page_obj,
        "locations": locations,
        "travel_types": travel_types,
    }
    return render(request, "tours/tour_list.html", context)
