from django.shortcuts import render

def show_product_page(request):
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }

    return render(request, "product_page.html", context)


