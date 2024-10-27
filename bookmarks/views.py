from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from product.models import Product
from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkForm
from django.core import serializers

# View all bookmarks for the logged-in user
@csrf_exempt
@login_required(login_url='authentication:login')
def show_main(request):
    user = request.user
    bookmarks = Bookmark.objects.filter(user=user)  # Filter bookmarks by logged-in user
    form = BookmarkForm()

    context = {
        'user': user,
        'bookmarks': bookmarks,
        'form': form,
    }

    return render(request, "bookmarks.html", context)

# Handle adding a new bookmark
@csrf_exempt
@login_required(login_url='authentication:login')
def create_bookmark(request):
    if request.method == "POST":
        user=request.user
        note = request.POST.get("note")
        priority = request.POST.get("priority")
        reminder = request.POST.get("reminder")
        product_id = request.POST.get("product_id")

        if note and priority and reminder:
            product = get_object_or_404(Product, pk=product_id)
            new_bookmark = Bookmark(
                user=user,
                product=product,
                note=note,
                priority=priority,
                reminder=reminder,
            )
            new_bookmark.save()
            return redirect(reverse("bookmarks:show_main"))  # Redirect after successful creation

    # Handle GET request
    products = Product.objects.all()
    form = BookmarkForm()
    context = {
        'products': products,
        'form': form,
    }
    return render(request, "create_bookmark.html", context)


# Handle updating (edit) an existing bookmark
@csrf_exempt
@login_required(login_url="authentication:login")
def update_bookmark(request, id):
    if request.method == "POST":
        bookmark = Bookmark.objects.get(pk=id, user=request.user) 

        # Only update fields if they are provided in the request
        if "note" in request.POST:
            bookmark.note = request.POST["note"]
        if "priority" in request.POST:
            bookmark.priority = request.POST["priority"]
        if "reminder" in request.POST:
            bookmark.reminder = request.POST["reminder"]

        bookmark.save()
        return HttpResponse(b"CREATED", status=201)

    return HttpResponse(b"FAILED", status=400)

# Handle deleting a bookmark
@login_required(login_url="authentication:login")
def delete_bookmark(request, id):
    bookmark = get_object_or_404(Bookmark, pk=id, user=request.user)  # Ensure only user's bookmark can be deleted
    bookmark.delete()
    return redirect("bookmarks:show_main")

def show_json(request):
    user = request.user
    data = Bookmark.objects.filter(user=user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    user = request.user
    data = Bookmark.objects.filter(pk=id, user=user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")