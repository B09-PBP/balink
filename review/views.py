import json
import uuid
from django.urls import reverse
from product.models import Product
from review.models import Review
from review.forms import ReviewEntryForm
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# Create your views here.
@login_required(login_url="authentication:login")
def show_main(request):
    reviews = Review.objects.all().order_by('-id')
    user = request.user
    context = {
        'user' : user,
        'reviews': reviews,
    }
    return render(request, "review.html", context)

@login_required(login_url="authentication:login")
def ride_to_review(request):
    rides = Product.objects.all()
    form = ReviewEntryForm(request.POST or None)

    context = {
        'products': rides,
        'form': form,
    }

    return render(request, "ride_to_review.html", context)

@csrf_exempt
@require_POST
def add_review_entry_ajax(request):
    user = request.user
    ride = get_object_or_404(Product, id=request.POST.get("product_id"))
    rating = request.POST.get("rating")
    review_message = strip_tags(request.POST.get("review_message"))

    if rating and review_message:
        new_review = Review(
            user=user,
            ride=ride,
            rating=rating,
            review_message=review_message,
        )
        new_review.save()
        
        return redirect(reverse('review:show_main'))

    return render(request, 'review_form.html', {
        'error_message': "Invalid input. Please fill all fields.",
    })

@csrf_exempt
def add_review_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        id = uuid.UUID(data["id"])
        ride = Product.objects.get(id=data["id"])

        new_review = Review.objects.create(
            user=request.user,
            ride=ride,
            rating=int(data["rating"]),
            review_message=data["review_message"] 
        )

        new_review.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

def all_reviews_flutter(request):
    list_review = []
    reviews = Review.objects.all()

    for review in reviews:
        review_data = {
            "image": review.ride.image_url,
            "username": review.user.username,
            "rideName": review.ride.name,
            "rating": review.rating,
            "reviewMessage": review.review_message,
        }

        list_review.append(review_data)
        
    return HttpResponse(json.dumps(list_review), content_type="application/json")

def all_rides_flutter(request):
    list_ride = []
    rides = Product.objects.all().order_by('-id')

    for ride in rides:
        ride_data = {
            "id": str(ride.id),
            "image": ride.image_url,
            "rideName": ride.name,
        }

        list_ride.append(ride_data)
    return HttpResponse(json.dumps(list_ride), content_type="application/json")

@login_required(login_url="authentication:login")
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user.userprofile.privilege == "admin":
        review.delete()
    
    return redirect('review:show_main')

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
