from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import CheckoutForm
from .models import History
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile
from product.models import Product
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

@csrf_exempt
@login_required(login_url="authentication:login")
def show_cart(request):
    user = request.user

    # Cek apakah user memiliki UserProfile, jika tidak buat
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)

    cart = user.userprofile.cart.all()

    # Hitung jumlah kendaraan di cart (total rides)
    total_items = cart.count()

    # Hitung total harga kendaraan di cart
    total_price = sum([car.price for car in cart])

    form = CheckoutForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        history = form.save(commit=False)
        history.user = request.user

        form.save()

        for car in cart:
            history.buku.add(car)
            request.user.userprofile.owned_cars.add(car)
            request.user.userprofile.cart.remove(car)

        return HttpResponse(b"OK", status=200)

    context = {
        "cart": cart,
        "form": form,
        "total_items": total_items,  # Tambahkan total rides ke context
        "total_price": total_price,  # Tambahkan total harga ke context
    }

    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Mengambil produk dengan id yang sesuai
    user_profile = request.user.userprofile  # Ambil UserProfile yang sesuai
    user_profile.cart.add(product)  # Tambahkan produk ke cart user

    return redirect('cart:show_cart') 

@csrf_exempt
@require_POST
@login_required(login_url="authentication:login")
def booking_cart_ajax(request):
    form = CheckoutForm(request.POST)

    cart_items = request.user.userprofile.cart.all()
    if not cart_items:
        return JsonResponse({'status': 'error', 'message': 'Booking failed. Cart is empty.'})

    if form.is_valid():
        history = form.save(commit=False)
        history.user = request.user
        history.save()  # Save the history entry first

        # Transfer items from the user's cart to the order history
        cart_items = request.user.userprofile.cart.all()
        
        for product in cart_items:
            history.car.add(product)  # Add each product to the history entry
            request.user.userprofile.cart.remove(product)  # Remove from the user's cart

        return JsonResponse({'status': 'success', 'message': 'Booking successful!'})

    # If form is invalid, return an error response
    return JsonResponse({'status': 'error', 'message': 'Booking failed. Please check your form data.'})

@login_required(login_url="authentication:login")
def show_history(request):
    history = History.objects.filter(user=request.user)

    context = {
        "history": history,
    }

    return render(request, "history.html", context)

def remove_car_from_cart(request, car_id):
    car = request.user.userprofile.cart.get(id=car_id)

    request.user.userprofile.cart.remove(car)

    return HttpResponseRedirect(reverse('cart:show_cart'))

@csrf_exempt
def remove_car_from_cart_ajax(request, id):
    if request.method == "POST":
        car = request.user.userprofile.cart.get(id=id)

        request.user.userprofile.cart.remove(car)

        return HttpResponse(b"OK", status = 200)
    
    return HttpResponseNotFound()


def show_json(request):
    data = History.objects.all()  # Use the correct model here
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = History.objects.filter(pk=id)  # Use the correct model here
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def add_product_to_cart_flutter(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
        
    product = get_object_or_404(Product, id=product_id)
    user_profile = request.user.userprofile  

    try:
        user_profile.cart.add(product) 
        return JsonResponse({'message': 'Product added to cart successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Error adding product to cart: {str(e)}'}, status=500)

# Mengambil produk dari cart pengguna
def get_user_cart(request, user_id):
    try:
        cart = History.objects.get(user=user_id)
        products = cart.car.all()
        product_list = [{"name": p.name, "price": str(p.price), "description": p.description} for p in products]
        return JsonResponse({"cart": product_list}, status=200)
    except History.DoesNotExist:
        return JsonResponse({"message": "Cart not found"}, status=404)

# Menghapus produk dari cart
def remove_product_from_cart(request, user_id, product_id):
    user = get_object_or_404(User, id=user_id)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = History.objects.get(user=user)
        cart.car.remove(product)
        cart.save()
        return JsonResponse({'message': 'Product removed from cart'}, status=200)
    except History.DoesNotExist:
        return JsonResponse({'message': 'Cart not found'}, status=404)