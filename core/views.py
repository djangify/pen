# core/views.py
from django.shortcuts import render
from django.utils import timezone
from blog.models import Post

def home_view(request):
    # Get the latest 3 published blog posts
    latest_posts = Post.objects.filter(
        status="published", 
        publish_date__lte=timezone.now()
    ).order_by("-publish_date")[:3]
    
    context = {
        'latest_posts': latest_posts,
    }
    
    return render(request, 'index.html', context)