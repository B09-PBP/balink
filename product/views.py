from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product
from authentication.models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)[:5] 
    results = [{'name': product.name} for product in products]
    return JsonResponse(results, safe=False)

@login_required(login_url='authentication:login')
def show_product_page(request):
    search_query = request.GET.get("search", "")
    
    products = Product.objects.all()  
    current_user = request.user  
    user_profile = UserProfile.objects.get(user=current_user)

    if search_query:
        products = products.filter(name__icontains=search_query)

    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    
    if min_price is not None and min_price != '':
        products = products.filter(price__gte=min_price)
    
    if max_price is not None and max_price != '':
        products = products.filter(price__lte=max_price)

    min_year = request.GET.get('min_year', None)
    max_year = request.GET.get('max_year', None)
    
    if min_year is not None and min_year != '':
        products = products.filter(year__gte=min_year)
    
    if max_year is not None and max_year != '':
        products = products.filter(year__lte=max_year)

    min_km = request.GET.get('min_km', None)
    max_km = request.GET.get('max_km', None)
    
    if min_km is not None and min_km != '':
        products = products.filter(km_driven__gte=min_km)
    
    if max_km is not None and max_km != '':
        products = products.filter(km_driven__lte=max_km)

    return render(request, "product_page.html", {
        "products": products,
        "search_query": search_query,
        "user" : user_profile,
    })

@login_required(login_url='authentication:login')
def show_product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(dealer=product.dealer).exclude(id=product.id)[:2] 

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)

@csrf_exempt
@require_POST
def add_product(request):
    product_image_url = request.POST.get('image_url')
    product_name = request.POST.get('name')
    product_price = request.POST.get('price')
    product_year = request.POST.get('year')
    product_km = request.POST.get('km_driven')
    dealer = request.POST.get('dealer')
    
    new_product = Product(
        name=product_name,
        price=product_price,
        year=product_year,
        km_driven=product_km,
        image_url = product_image_url,
        dealer=dealer,
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

def delete_product(request, id):
    product = Product.objects.get(pk = id)
    product.delete()
    return HttpResponseRedirect(reverse('product:show_product_page'))

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