import datetime
import json
from venv import logger
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
from datetime import datetime

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
    history = History.objects.filter(user=request.user).select_related('user')

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

# views.py
@csrf_exempt
def get_user_cart(request):
    try:
        user_profile = request.user.userprofile
        cart_items = user_profile.cart.all()

        print(f"Found {len(cart_items)} items in cart")  # Debug print

        cart_data = []
        for product in cart_items:
            cart_data.append({
                "model": "cart.cartentry",
                "pk": str(product.id),
                "fields": {
                    "name": product.name,
                    "price": float(product.price),
                    "car": [str(product.id)],
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "address": "",
                    "user": request.user.id,
                    "imageUrl": product.image_url
                }
            })
        print(f"Response data: {cart_data}")  # Debug print
        return JsonResponse(cart_data, safe=False)
    except Exception as e:
        print(f"Error in get_user_cart: {e}")  # Debug print
        return JsonResponse({"error": str(e)}, status=500)
    
# Menghapus produk dari cart
@csrf_exempt
@login_required(login_url="authentication:login")
def remove_product_from_cart_flutter(request):
    if request.method == "POST":
        try:
            # Ambil nama produk dari request POST
            product_name = request.POST.get("product_name")
            if not product_name:
                return JsonResponse({'message': 'Product name is missing'}, status=400)

            # Ambil profil pengguna dan produk yang ingin dihapus
            user_profile = request.user.userprofile
            product = user_profile.cart.filter(name=product_name).first()

            if not product:
                return JsonResponse({'message': 'Product not found in cart'}, status=404)

            user_profile.cart.remove(product)  # Hapus produk dari keranjang pengguna

            return JsonResponse({'message': 'Product removed from cart'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error removing product: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

# views.py
@csrf_exempt
def booking_cart_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create history entry
            new_history = History.objects.create(
                user=request.user,
                name=data["name"],
                address=data["address"]
            )
            
            # Get user's cart items
            user_profile = request.user.userprofile
            cart_items = user_profile.cart.all()
            
            # Move all items from cart to history
            for car in cart_items:
                new_history.car.add(car)
                user_profile.cart.remove(car)
            
            return JsonResponse({
                "status": "success",
                "message": "Checkout successful!"
            }, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON format"
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
    
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)

@csrf_exempt
def get_history_flutter(request):
    try:
        history_items = History.objects.filter(user=request.user)
        
        data = []
        for history in history_items:
            cars = history.car.all()
            for car in cars:
                data.append({
                    "username": request.user.username,
                    "name": history.name,
                    "address": history.address,
                    "date": history.date.strftime("%Y-%m-%d"),
                    "product_name": car.name,
                    "price": float(car.price),
                    "image_url": car.image_url if hasattr(car, 'image_url') else None,
                })
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)