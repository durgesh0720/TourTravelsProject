from django.shortcuts import render
from tours.models import Tour
from django.core.paginator import Paginator

def landingpage(request):
    locations = Tour.objects.values_list('location', flat=True).distinct()
    travel_types = Tour.objects.values_list('category__name', flat=True).distinct()  # Fetching unique travel categories

    tours = Tour.objects.all()  # Fetch all tours
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
    }
    return render(request,'home/landingPage.html',context)

