import json
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from product.models import Product
from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkForm

# View all bookmarks for the logged-in user
@csrf_exempt
@login_required(login_url='authentication:login')
def show_main(request):
    form = BookmarkForm(request.POST or None)

    user = request.user
    bookmarks = Bookmark.objects.all()

    context = {
        'user': user,
        'form' : form,
    }

    if request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        bookmarks = Bookmark.objects.get(pk=data["pk"])

        bookmarks = {
            'note': bookmarks.note,
            'priority': bookmarks.priority,
            'reminder': bookmarks.reminder,
        }

        response = HttpResponse(json.dumps(
            bookmarks), content_type="application/json")
        response.set_cookie('bookmark_update', bookmarks.pk)
        return response

    return render(request, "bookmarks.html", context)

# Handle adding a new bookmark
@csrf_exempt
@login_required(login_url='authentication:login')
def create_bookmark(request):
    user = request.user

    context = {
        'user': user,
    }

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        product_id = data.get("product_id")
        note = data.get("note", "There's no note yet")  # Default note if not provided
        priority = data.get("priority", "M")  # Default priority to Medium (M)
        reminder = data.get("reminder")  # Reminder date, optional

        # Get the product instance
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"status": "Product not found"}, status=404)

        # Check if the product is already bookmarked by the user
        existing_bookmark = Bookmark.objects.filter(user=user, product=product)

        if not existing_bookmark.exists():
            # Create a new bookmark
            bookmark = Bookmark(
                user=user,
                product=product,
                note=note,
                priority=priority,
                reminder=reminder
            )
            bookmark.save()
            return HttpResponse("ADDED", status=201)
    return render(request, "create_bookmark.html", context)

# Update or modify an existing bookmark
@csrf_exempt
def update_bookmark(request):
    if request.method == "POST":
        form = BookmarkForm(request.POST)
        # Retrieve the bookmark ID from the cookie
        bookmark_id = request.COOKIES.get('bookmark_update')
        
        try:
            bookmark = Bookmark.objects.get(pk=bookmark_id, user=request.user)
        except Bookmark.DoesNotExist:
            return HttpResponseNotFound("Bookmark not found.")

        if form.is_valid():
            # Update the fields based on the form data
            bookmark.note = form.cleaned_data.get('note', bookmark.note)
            bookmark.priority = request.POST.get('priority', bookmark.priority)
            bookmark.reminder = form.cleaned_data.get('reminder', bookmark.reminder)
            bookmark.save()

            response = HttpResponse(status=200)
            response.delete_cookie('bookmark_update')
            return response
        else:
            return JsonResponse(form.errors, status=400)  # Send form validation errors if any

    return HttpResponseNotFound()

# Delete a bookmark
@login_required(login_url="authentication:login")
@csrf_exempt
def delete_bookmark(request, bookmark_id):
    bookmark = Bookmark.objects.get(pk = id)
    bookmark.delete()
    return HttpResponseRedirect(reverse('bookmarks:show_main'))

def show_json(request):
    data = Bookmark.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Bookmark.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")