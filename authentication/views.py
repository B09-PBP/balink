from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from authentication.forms import RegisterForm
from authentication.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_page = request.GET.get("next")
            if next_page is None:
                response = redirect("landing_page:show_main")
            else:
                response = redirect(next_page)
            response.set_cookie("user_logged_in", user)
            return response
        else:
            messages.info(
                request, "Sorry, incorrect username or password. Please try again.")
    context = {}
    if request.user.is_authenticated:
        return redirect('landing_page:show_main')
    else:
        return render(request, "login.html", context)

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been successfully created!')
            return redirect('authentication:login')
    context = {"form": form}
    if request.user.is_authenticated:
        return redirect('landing_page:show_main')
    else:
        return render(request, "register.html", context)

def logout_user(request):
    logout(request)
    response = redirect("landing_page:show_main")
    response.delete_cookie('user_logged_in')
    return response

@csrf_exempt
def login_mobile(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            # Get user profile details
            user_profile = user.userprofile
            return JsonResponse({
                "username": user.username,
                "name": user_profile.name,
                "privilege": user_profile.privilege,
                "status": True,
                "message": "Login successful!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed. Account is deactivated."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed. Try again."
        }, status=401)

@csrf_exempt
def logout_mobile(request):
    username = request.user.username
    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout successful!"
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)

@csrf_exempt
def register_mobile(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            form = RegisterForm(data)

            if form.is_valid():
                user = form.save()  # Save the user

                # Check if a UserProfile for this user already exists
                user_profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        "name": form.cleaned_data["name"].strip(),
                        "privilege": form.cleaned_data.get("privilege", "customer").strip().lower(),
                    }
                )

                if created:
                    user_profile.save()

                return JsonResponse({
                    "status": True,
                    "message": "Your account has been successfully created!"
                }, status=201)

            else:
                # Handle detailed errors including password validation
                errors = {}
                for field, field_errors in form.errors.get_json_data().items():
                    errors[field] = [error["message"] for error in field_errors]

                return JsonResponse({
                    "status": False,
                    "message": "Registration failed.",
                    "errors": errors
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON format."
            }, status=400)

    return JsonResponse({
        "status": False,
        "message": "Use POST method to register."
    }, status=4
    )

def check_login(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'is_logged_in': True,
            'username': request.user.username,
            'privilege': UserProfile.objects.get(user=request.user).privilege
        })
    else:
        return JsonResponse({
            'is_logged_in': False,
            'username': None,
            'privilege': None
        })

@csrf_exempt
def get_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        profile_data = {
            'id': profile.id,
            'username': profile.user.username,
            'name': profile.name,
            'email': profile.user.email,
            'privilege': profile.privilege,
            'cart_items': list(profile.cart.values('id', 'name', 'price'))  
        }
        
        return JsonResponse(profile_data, safe=True)
    
    except UserProfile.DoesNotExist:
        return JsonResponse({
            'error': 'User profile not found'
        }, status=404)