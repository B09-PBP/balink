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
        {"title": "15 Destinasi Instagrammable di Bali ", "url": "https://www.indonesia.travel/id/id/ide-liburan/15-destinasi-instagrammable-di-bali-yang-harus-sobat-pesona-kunjungi.html"},
        {"title": "10 Objek Wisata Terbaik di Bali", "url": "https://www.tripadvisor.co.id/Attractions-g294226-Activities-Bali.html"},
        {"title": "15+ Rekomendasi Tempat Liburan Seru di Pulau Bali", "url": "https://www.cimbniaga.co.id/id/inspirasi/gayahidup/rekomendasi-tempat-wisata-alam-dan-budaya-di-pulau-bali"},
        {"title": "Top 30 Tempat Wisata di Bali yang Tak Boleh Dilewatkan", "url": "https://id.trip.com/guide/activity/tempat-wisata-di-bali.html"},
        {"title": "10 Best Things to Do and More in Bali", "url": "https://www.getyourguide.com/-l347/?cmp=ga&ps_theme=ttd&cq_src=google_ads&cq_cmp=15508255885&cq_con=132581187524&cq_term=bali%20top10&cq_med=&cq_plac=&cq_net=g&cq_pos=&cq_plt=gp&campaign_id=15508255885&adgroup_id=132581187524&target_id=kwd-1432321165848&loc_physical_ms=9072593&match_type=b&ad_id=574899113022&keyword=bali%20top10&ad_position=&feed_item_id=&placement=&device=c&partner_id=CD951&gad_source=1&gbraid=0AAAAADmzJCMfR3TgRU8a7SFt9CREmRFNL&gclid=CjwKCAjwyfe4BhAWEiwAkIL8sLqdQBcLdYQWsDByJsrgU5ib8Sn5VPY7EhAqrD0Fr0XwEVS7lcTo7xoCXgsQAvD_BwE"},
        {"title": "Fun Activities In Bali", "url": "https://www.booking.com/region/id/bali.en.html?aid=377400;label=bali-5VmtKJTi*Vx6LCdfGQXLFAS388490388182:pl:ta:p1:p2:ac:ap:neg:fi:tikwd-308609428065:lp9072593:li:dec:dm:ppccp=UmFuZG9tSVYkc2RlIyh9YdbYVqXDN8zp7PNDFvT66M8;ws=&gbraid=0AAAAAD_Ls1JX1u4e669AzBLVbhxfozgwr&gclid=CjwKCAjwyfe4BhAWEiwAkIL8sGlIzFJWfwqJFv9X1GKTiXl14W24xGclMXaIQ12MsVlM7i3DEzVZ-xoCUXAQAvD_BwE"}
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


