from django.urls import reverse
from product.models import Product
from review.models import Review
from review.forms import ReviewEntryForm
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# Create your views here.
def show_main(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, "review.html", context)

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

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")