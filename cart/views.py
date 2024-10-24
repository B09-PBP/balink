import json
from django.shortcuts import render
from django.contrib.auth.models import User
import authentication
from .forms import CheckoutForm
from .models import History
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile
from product.models import Product
from django.shortcuts import get_object_or_404, redirect

@csrf_exempt
@login_required(login_url="authentication:login_user")
def show_cart(request):
    user = request.user
    
    # Cek apakah user memiliki UserProfile, jika tidak buat
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)  # Ini membuat UserProfile, bukan User

    cart = user.userprofile.cart.all()
    form = CheckoutForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        history = form.save(commit=False)
        history.user = request.user
        
        form.save()

        for car in request.user.userprofile.cart.all():
            history.buku.add(car)
            request.user.userprofile.owned_cars.add(car)
            request.user.userprofile.cart.remove(car)

        return HttpResponse(b"OK", status=200)

    context = {
        "cart": cart,
        "form": form,
    }

    return render(request, 'cart.html', context)

@login_required(login_url="authentication:login")
def checkout_cart_ajax(request):
    form = CheckoutForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        history = form.save(commit=False)
        history.user = request.user
        
        form.save()

        for car in request.user.userprofile.cart.all():
            history.buku.add(car)
            request.user.userprofile.owned_cars.add(car)
            request.user.userprofile.cart.remove(car)

        return HttpResponse(b"OK", status=200)
    
    return render(request, "cart.html", {"form": form})    

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Mengambil produk dengan id yang sesuai
    user_profile = request.user.userprofile  # Ambil UserProfile yang sesuai
    user_profile.cart.add(product)  # Tambahkan produk ke cart user

    return redirect('cart:show_cart')     

def get_cart_json(request):
    cart = request.user.userprofile.cart.all()
    return HttpResponse(serializers.serialize('json', cart), content_type="application/json")

def get_cart_json_by_user_id(request, id):
    user = User.objects.filter(id=id)[0]
    cart = user.userprofile.cart.all()

    return HttpResponse(serializers.serialize('json', cart), content_type="application/json")

@login_required(login_url="authentication:login")
def booking_cart(request):
    form = CheckoutForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        history = form.save(commit=False)
        history.user = request.user
        
        form.save()

        for car in request.user.userprofile.cart.all():
            history.car.add(car)
            request.user.userprofile.owned_cars.add(car)
            request.user.userprofile.cart.remove(car)

        return HttpResponseRedirect(reverse('cart:show_cart'))
    
    return render(request, "booking.html", {"form": form})

@login_required(login_url="authentication:login")
def show_history(request):
    history = History.objects.filter(user=request.user)

    context = {
        "history": history,
    }

    return render(request, "history.html", context)

def get_history_json(request):
    history = History.objects.all()

    return HttpResponse(serializers.serialize('json', history), content_type="application/json")

@login_required(login_url="authentication:login")
def show_owned(request):
    owned = request.user.userprofile.owned_cars.all()

    context = {
        "owned": owned,
    }

    return render(request, "display_owned.html", context)

def remove_car_from_cart(request, car_id):
    car = request.user.userprofile.cart.get(id=car_id)

    request.user.userprofile.cart.remove(car)

    return HttpResponseRedirect(reverse('cart:show_cart'))

@csrf_exempt
def remove_car_from_cart_flutter(request, user_id, car_id):
    user = User.objects.filter(id=user_id)[0]
    car = user.userprofile.cart.get(id=car_id)

    user.userprofile.cart.remove(car)

    return JsonResponse({"status": "success"}, status=200)

@csrf_exempt
def remove_car_from_cart_ajax(request, id):
    if request.method == "POST":
        car = request.user.userprofile.cart.get(id=id)

        request.user.userprofile.cart.remove(car)

        return HttpResponse(b"OK", status = 200)
    
    return HttpResponseNotFound()