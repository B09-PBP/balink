from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from authentication.models import UserProfile
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import ProductEntryForm
from django.contrib import messages
from django.utils.html import strip_tags

def show_product_page(request):
    # Get the search query from the request
    search_query = request.GET.get("search", "")
    
    # Get all products and current user information
    products = Product.objects.all()  

    # Filter products based on the search query if provided
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter products by price range if specified
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    
    if min_price is not None and min_price != '':
        products = products.filter(price__gte=min_price)
    
    if max_price is not None and max_price != '':
        products = products.filter(price__lte=max_price)

    # Filter products by year range if specified
    min_year = request.GET.get('min_year', None)
    max_year = request.GET.get('max_year', None)
    
    if min_year is not None and min_year != '':
        products = products.filter(year__gte=min_year)
    
    if max_year is not None and max_year != '':
        products = products.filter(year__lte=max_year)

    # Filter products by kilometers driven if specified
    min_km = request.GET.get('min_km', None)
    max_km = request.GET.get('max_km', None)
    
    if min_km is not None and min_km != '':
        products = products.filter(km_driven__gte=min_km)
    
    if max_km is not None and max_km != '':
        products = products.filter(km_driven__lte=max_km)

    # Render the product page with the filtered product list
    return render(request, "product_page.html", {
        "products": products,
        "search_query": search_query,
        "user": UserProfile,
    })

def show_product_detail(request, id):
    # Get the product by ID or return a 404 error if not found
    product = get_object_or_404(Product, id=id)
    # Get related products from the same dealer, excluding the current product
    related_products = Product.objects.filter(dealer=product.dealer).exclude(id=product.id)[:2] 

    # Render the product detail page with product and related products
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)

@login_required
def edit_product(request, id):
    # Get the product to be edited
    product = Product.objects.get(id=id)
    
    if request.method == 'POST':
        # Create a form instance with POST data and the current product instance
        form = ProductEntryForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save the updated product
            return redirect('product:show_product_detail', id=id)  # Redirect to product detail page
    else:
        form = ProductEntryForm(instance=product)  # Populate form with current product data

    # Render the edit product page with the form
    return render(request, 'product_edit.html', {'form': form, 'product': product})

@csrf_exempt
@require_POST
@login_required
def add_product(request):
    # Get product details from the request
    product_image_url = strip_tags(request.POST.get('image_url'))
    product_name = strip_tags(request.POST.get('name'))
    product_price = request.POST.get('price')
    product_year = request.POST.get('year')
    product_km = request.POST.get('km_driven')
    dealer = strip_tags(request.POST.get('dealer'))
    
    # Create a new Product instance
    new_product = Product(
        name=product_name,
        price=product_price,
        year=product_year,
        km_driven=product_km,
        image_url=product_image_url,
        dealer=dealer,
    )
    new_product.save()  # Save the new product to the database

    return HttpResponse(b"CREATED", status=201)  # Return a success response

@login_required
def delete_product(request, id):
    # Get the product by ID and delete it
    product = Product.objects.get(pk=id)
    product.delete()  # Delete the product
    return HttpResponseRedirect(reverse('product:show_product_page'))  # Redirect to product page

@login_required
def show_xml(request):
    # Get all products and serialize them to XML format
    products = Product.objects.all()

    # Filtering based on query parameters
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    min_price = request.GET.get('min_price', None)
    if min_price is not None and min_price != '':
        products = products.filter(price__gte=min_price)

    max_price = request.GET.get('max_price', None)
    if max_price is not None and max_price != '':
        products = products.filter(price__lte=max_price)

    min_year = request.GET.get('min_year', None)
    if min_year is not None and min_year != '':
        products = products.filter(year__gte=min_year)

    max_year = request.GET.get('max_year', None)
    if max_year is not None and max_year != '':
        products = products.filter(year__lte=max_year)

    min_km = request.GET.get('min_km', None)
    if min_km is not None and min_km != '':
        products = products.filter(km_driven__gte=min_km)

    max_km = request.GET.get('max_km', None)
    if max_km is not None and max_km != '':
        products = products.filter(km_driven__lte=max_km)

    data = products
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required
def show_json(request):
    # Get all products and serialize them to JSON format
    products = Product.objects.all()

    # Filtering based on query parameters
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    min_price = request.GET.get('min_price', None)
    if min_price is not None and min_price != '':
        products = products.filter(price__gte=min_price)

    max_price = request.GET.get('max_price', None)
    if max_price is not None and max_price != '':
        products = products.filter(price__lte=max_price)

    min_year = request.GET.get('min_year', None)
    if min_year is not None and min_year != '':
        products = products.filter(year__gte=min_year)

    max_year = request.GET.get('max_year', None)
    if max_year is not None and max_year != '':
        products = products.filter(year__lte=max_year)

    min_km = request.GET.get('min_km', None)
    if min_km is not None and min_km != '':
        products = products.filter(km_driven__gte=min_km)

    max_km = request.GET.get('max_km', None)
    if max_km is not None and max_km != '':
        products = products.filter(km_driven__lte=max_km)

    data = products
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required
def show_xml_by_id(request, id):
    # Get a product by ID and serialize it to XML format
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required
def show_json_by_id(request, id):
    # Get a product by ID and serialize it to JSON format
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")