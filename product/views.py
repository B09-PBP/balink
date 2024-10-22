from django.http import JsonResponse
from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from django.core import serializers

def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)[:5]  # Limit to 5 results
    results = [{'name': product.name} for product in products]
    return JsonResponse(results, safe=False)

def show_product_page(request):
    # Get the search query from the request
    search_query = request.GET.get("search", "")
    
    # Initialize products variable
    products = Product.objects.all()  # Ensure products is initialized

    # Filter products based on the search query
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter by price
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    
    if min_price is not None and min_price != '':
        products = products.filter(price__gte=min_price)
    
    if max_price is not None and max_price != '':
        products = products.filter(price__lte=max_price)

    # Filter by year
    min_year = request.GET.get('min_year', None)
    max_year = request.GET.get('max_year', None)
    
    if min_year is not None and min_year != '':
        products = products.filter(year__gte=min_year)
    
    if max_year is not None and max_year != '':
        products = products.filter(year__lte=max_year)

    # Filter by km driven
    min_km = request.GET.get('min_km', None)
    max_km = request.GET.get('max_km', None)
    
    if min_km is not None and min_km != '':
        products = products.filter(km_driven__gte=min_km)
    
    if max_km is not None and max_km != '':
        products = products.filter(km_driven__lte=max_km)

    # Render the template with the products and search query
    return render(request, "product_page.html", {
        "products": products,
        "search_query": search_query,
    })

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")