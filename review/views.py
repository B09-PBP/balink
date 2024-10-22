from product.models import Product
from review.models import Review
from review.forms import ReviewEntryForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_main(request):
    context = {
        'review' : 'review',
    }
    return render(request, "review.html", context)

def ride_to_review(request):
    rides = Product.objects.all()
    form = ReviewEntryForm(request.POST or None)

    context = {
        'products' : rides,
        'form' : form,
    }

    return render(request, "ride_to_review.html", context)

def form_review(request, uuid):
    product = get_object_or_404(Product,id=uuid)
    form = ReviewEntryForm(request.POST or None)
    print(product)
    context = {
        'product': product,
        'form' : form,
    }

    return render(request, 'create_review_form.html', context)

@csrf_exempt
def create_review(request):
    if request.method == "POST":
        user = request.user
        ride = Product.objects.get(pk=request.POST.get("id"))
        rating = request.POST.get("rating")
        review_message = request.POST.get("review_message")

        new_review = Review(user=user, ride=ride, rating=rating, review_message=review_message)
        new_review.save()

        return redirect('review')
    return HttpResponseNotFound()

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Review.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")