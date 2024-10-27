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
        {"name": "Name 4", "npm": "2100004", "image": "img/foto kinan.jpg"},
        {"name": "Name 5", "npm": "2100005", "image": "img/foto mawla.jpg"},
    ]

    context = {"team_members": team_members}
    return render(request, 'aboutus.html', context)