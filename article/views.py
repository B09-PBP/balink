from django.shortcuts import render, redirect, get_object_or_404  
from article.forms import ArticleForms
from article.models import Article
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from authentication.models import UserProfile
from .models import Product



@login_required(login_url='authentication:login')
def show_article_page(request):
    show_article = Article.objects.all()
    current_user = request.user
    user = UserProfile.objects.get(user = current_user)

    other_articles = [
        {"title": "Food Court Mampau Belitung", "url": "https://example.com/food-court-mampau"},
        {"title": "Bong Li Piang", "url": "https://example.com/bong-li-piang"},
        {"title": "5 Tempat Belanja Oleh-oleh khas Bangka", "url": "https://example.com/tempat-belanja-oleh-oleh"},
        {"title": "Martabak Bangka", "url": "https://example.com/martabak-bangka"},
        {"title": "Pulau Lengkuas", "url": "https://example.com/pulau-lengkuas"},
        {"title": "Jembatan Emas", "url": "https://example.com/jembatan-emas"}
    ]

    context = {
        'show_article': show_article,
        'other_articles': other_articles,  
        'user': user,
    }

    return render(request, "article_page.html", context)



@login_required(login_url='authentication:login')
def MakeArticleForm(request):
    if request.method == 'POST':
        form = ArticleForms(request.POST)
        if form.is_valid():
            article = form.save(commit=False) 
            article.user = request.user      
            article.save()                   
            return redirect('article:show_article_page')    
    else:
        form = ArticleForms()
    return render(request, 'make_article_forms.html', {'form': form})



@login_required(login_url='authentication:login')
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        article.delete()
        return redirect('article:show_article_page')
    return redirect('article:show_article_page')



@login_required(login_url='authentication:login')
def inside_article(request, id):
    article = get_object_or_404(Article, id=id)
    product = Product.objects.all()[:3]
    paragraphs = article.content.split('\n\n')

    context = {
        'article': article,
        'paragraphs': paragraphs, 
        'comments': article.comments,  
        'products': product
    }
    return render(request, "inside_article.html", context)



@login_required(login_url='authentication:login')
@csrf_exempt  
@require_POST
def add_comment(request, article_id):
    try:
        comment_text = request.POST.get('comment_text', '').strip()
        
        if comment_text:
            article = get_object_or_404(Article, id=article_id)
            article.add_comment(request.user, comment_text)
            
            return JsonResponse({'success': True, 'user': request.user.username, 'comment': comment_text})
        else:
            return JsonResponse({'success': False, 'error': 'Empty comment text'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



@login_required(login_url='authentication:login')
@csrf_exempt  # Allow CSRF exemption for the view
def delete_comment(request, article_id, comment_index):
    article = get_object_or_404(Article, id=article_id)
    
    # Check if the user is authorized to delete the comment
    if article.user != request.user and not request.user.userprofile.privilege == "admin":
        return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)
    
    if request.method == "POST":
        try:
            article.delete_comment(comment_index)  # Remove the comment at the specified index
            return JsonResponse({'success': True})
        except IndexError:
            return JsonResponse({'success': False, 'error': 'Invalid comment index'}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)



@login_required(login_url='authentication:login')
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == 'POST':
        form = ArticleForms(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article:show_article_page')
    else:
        form = ArticleForms(instance=article)

    return render(request, 'edit_article_form.html', {'form': form, 'article': article})


