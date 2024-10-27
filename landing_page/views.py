from django.shortcuts import render

def show_main(request):
    context = {
        'user': request.user
    }
    return render(request, "landing.html", context)

def about_us(request):
    team_members = [
        {"name": "Nevin Thang", "npm": "2306203204", "image": "img/foto nevin.jpg"},
        {"name": "Shaine Glorvina Mathea", "npm": "2306245573", "image": "img/foto shaine.jpg"},
        {"name": "Nabilah Roslita Utami", "npm": "2306223446", "image": "img/foto bilah.jpg"},
        {"name": "Shabrina Aulia Kinanti", "npm": "2306245472", "image": "img/foto kinan.jpg"},
        {"name": "Mawla Raditya Pambudi", "npm": "2306275323", "image": "img/foto mawla.jpg"},
    ]

    context = {"team_members": team_members}
    return render(request, 'aboutus.html', context)