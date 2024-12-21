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
from django.db.models import Q

# Create your views here.
# Method untuk show all reviews page
@login_required(login_url="authentication:login")
def show_main(request):
    rating_filter = request.GET.get('rating')
    if rating_filter:
        reviews = Review.objects.filter(rating=rating_filter).order_by('-id')
    else:
        reviews = Review.objects.all().order_by('-id')

    user = request.user
    context = {
        'user': user,
        'reviews': reviews,
    }
    return render(request, "review.html", context)

# Method untuk show all rides to review
@login_required(login_url="authentication:login")
def ride_to_review(request):
    search_key = request.GET.get('search', '')
    
    if search_key:
        rides = Product.objects.filter(name__icontains=search_key)
    else:
        rides = Product.objects.all()
    
    form = ReviewEntryForm(request.POST or None)
    context = {
        'products': rides,
        'form': form,
    }

    return render(request, "ride_to_review.html", context)

# Method untuk ajax add review
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

# Method untuk delete review for admin
@login_required(login_url="authentication:login")
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user.userprofile.privilege == "admin":
        review.delete()
    
    return redirect('review:show_main')

# Method untuk add review in flutter
@csrf_exempt
@login_required
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

# Method edit review di flutter
@csrf_exempt
@login_required
def edit_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        review_id = data["id"]
        rating = int(data["rating"])
        review_message = data["review_message"]

        try:
            review = Review.objects.get(id=review_id, user=request.user)
        except Review.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found or you don't have permission to edit it"}, status=400)

        review.rating = rating
        review.review_message = review_message

        review.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=401)

# Method untuk data json all reviews di flutter
@login_required
def all_reviews_flutter(request):
    reviews = Review.objects.all().order_by('-id')

    list_review = []
    for review in reviews:
        review_data = {
            "id": str(review.id),
            "image": review.ride.image_url,
            "username": review.user.username,
            "rideName": review.ride.name,
            "rating": review.rating,
            "reviewMessage": review.review_message,
        }

        list_review.append(review_data)
        
    return HttpResponse(json.dumps(list_review), content_type="application/json")

@login_required
def user_review_flutter(request):
    user_reviews = Review.objects.filter(user=request.user).order_by('-id')

    list_user_review = []
    for review in user_reviews:
        review_data = {
            "id": str(review.id),
            "image": review.ride.image_url,
            "username": review.user.username,
            "rideName": review.ride.name,
            "rating": review.rating,
            "reviewMessage": review.review_message,
        }

        list_user_review.append(review_data)

    return HttpResponse(json.dumps(list_user_review), content_type="application/json")

# Method untuk data json all rides to review di flutter
@login_required
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

# Method untuk delete review for admin di flutter
@login_required
@csrf_exempt
def delete_review_flutter(request, review_id):
    if request.user.userprofile.privilege != "admin":
        return JsonResponse({'status': 'error', 'message': 'You do not have permission'}, status=403)

    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return JsonResponse({'status': 'success', 'message': 'Review deleted successfully'})

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")