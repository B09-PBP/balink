from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from product.models import Product
from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkForm
from django.core import serializers
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from product.models import Product

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
@csrf_exempt
@login_required(login_url="authentication:login")
def delete_bookmark(request, id):
    bookmark = get_object_or_404(Bookmark, pk=id, user=request.user)  # Ensure only user's bookmark can be deleted
    bookmark.delete()
    return redirect("bookmarks:show_main")

def get_user_bookmarks(request):
    user = request.user
    user_bookmarks =list(Bookmark.objects.filter(user=user))
    data = []

    for bookmark in user_bookmarks:
        product_asli = Product.objects.get(pk=bookmark.product.pk)

        each_data = {
            'pk': bookmark.pk,
            'note': bookmark.note,
            'priority': 'High' if bookmark.priority == 'H' else 'Medium' if bookmark.priority == 'M' else 'Low',
            'reminder': bookmark.reminder.strftime("%Y-%m-%d") if bookmark.reminder else '',
            'product': {
                'name': product_asli.name,
                'image_url': product_asli.image_url,
                }
        }
        data.append(each_data)

    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def show_json(request):
    user = request.user
    bookmarks = Bookmark.objects.filter(user=user)
    data = []
    for bookmark in bookmarks:
        data.append({
            'id': bookmark.id,
            'note': bookmark.note,
            'priority': bookmark.priority,
            'reminder': bookmark.reminder.strftime("%Y-%m-%d") if bookmark.reminder else None,
            'product': {
                'name': bookmark.product.name,
                'image_url': bookmark.product.image_url,
            },
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def show_json_by_id(request, id):
    user = request.user
    bookmark = get_object_or_404(Bookmark, pk=id, user=user)
    data = {
        'id': bookmark.id,
        'note': bookmark.note,
        'priority': bookmark.priority,
        'reminder': bookmark.reminder.strftime("%Y-%m-%d") if bookmark.reminder else None,
        'product': {
            'name': bookmark.product.name,
            'image_url': bookmark.product.image_url,
        },
    }
    return JsonResponse(data)

@csrf_exempt
@login_required(login_url="authentication:login")
def update_bookmark_flutter(request, id):
    if request.method == "POST":
        bookmark = Bookmark.objects.get(pk=id, user=request.user)
        if "note" in request.POST:
            bookmark.note = request.POST["note"]
        if "priority" in request.POST:
            bookmark.priority = request.POST["priority"]
        if "reminder" in request.POST:
            bookmark.reminder = request.POST["reminder"]

        bookmark.save()
        # Kembalikan JSON
        return JsonResponse({"status": "success"}, status=200)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@csrf_exempt
@login_required(login_url="authentication:login")
def delete_bookmark_flutter(request, id):
    if request.method == "POST":
        bookmark = get_object_or_404(Bookmark, pk=id, user=request.user)
        bookmark.delete()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
